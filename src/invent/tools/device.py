import invent
import asyncio
import json
from pyscript import document, js_import, window
from pyscript.ffi import to_js

# Datastore flags for Donkey worker status.
DONKEY_CREATING = "_DEVICE_DONKEY_CREATING"
DONKEY_READY = "_DEVICE_DONKEY_READY"
DONKEY_BUSY = "_DEVICE_DONKEY_BUSY"
DONKEY_ERROR = "_DEVICE_DONKEY_ERROR"
DONKEY_KILLED = "_DEVICE_DONKEY_KILLED"


"""
NOTE: I am using execute("from _opencv_worker import *") which
pulls everything into the worker's global scope, which is the only
reliable way to define persistent callables in a donkey worker that I 
could find. Both
  - process() feeds large multiline strings line-by-line which 
              prevents this sort of data from using it, and
  - execute() alone seems to scope defs locally and discard them
              after the call returns.
"""

# The OpenCV worker code written to the worker's virtual filesystem as a
# proper Python module.
_OPENCV_WORKER_MODULE = r"""
import base64
import cv2
import numpy as np


def _decode_data_url(data_url):
    if not data_url or "," not in data_url:
        raise ValueError("Expected an image data URL")
    payload = data_url.split(",", 1)[1]
    binary = base64.b64decode(payload)
    buf = np.frombuffer(binary, dtype=np.uint8)
    image = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Could not decode input image")
    return image


def _encode_png_data_url(image):
    ok, encoded = cv2.imencode(".png", image)
    if not ok:
        raise ValueError("Could not encode processed image")
    payload = base64.b64encode(encoded.tobytes()).decode("ascii")
    return "data:image/png;base64," + payload


def worker_run_user_code(user_code, data_url):
    image_bgr = _decode_data_url(data_url)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    grey = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    namespace = {
        "cv2": cv2,
        "np": np,
        "image_bgr": image_bgr,
        "image_rgb": image_rgb,
        "grey": grey,
        "result_image": None,
        "result": None,
    }

    exec(user_code, namespace, namespace)

    result = namespace.get("result_image")
    if result is None:
        result = namespace.get("result")
    if result is None:
        result = image_bgr

    if not isinstance(result, np.ndarray):
        raise ValueError(
            "Your code must assign a numpy ndarray to result_image or result"
        )

    if result.ndim == 2:
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
    elif result.ndim == 3 and result.shape[2] == 3:
        pass
    else:
        raise ValueError("Unsupported result_image shape")

    return {
        "ok": True,
        "kind": "user_code",
        "data_url": _encode_png_data_url(result),
    }
"""

_DONKEY_RUNTIME_MODULE = r"""
import json


def invent_run_code(code, context_json):
    namespace = {}
    if context_json:
        context = json.loads(context_json)
        if not isinstance(context, dict):
            raise ValueError("context must decode to a dict")
        namespace.update(context)
    exec(code, namespace, namespace)
    if "result" not in namespace:
        raise ValueError("Your code must assign a value to `result`")
    return namespace["result"]
"""

_PYSCRIPT_CORE = "https://pyscript.net/releases/2026.3.1/core.js"


def _ensure_terminal_div(terminal_id="donkey-terminal"):
    """
    Create a hidden terminal container in the DOM if needed.
    """
    if document.getElementById(terminal_id) is None:
        div = document.createElement("div")
        div.id = terminal_id
        div.style.display = "none"
        document.body.appendChild(div)
    return f"#{terminal_id}"


class DonkeyConnection:
    """General donkey wrapper with datastore-oriented execution."""

    def __init__(self, donkey, result_key=None):
        self._donkey = donkey
        self._result_key = result_key
        self._ready = False

    @property
    def ready(self):
        return self._ready

    def _set_status(self, status):
        if self._result_key:
            invent.datastore[self._result_key] = status

    async def initialize(self):
        self._set_status(DONKEY_BUSY)
        await self.execute(
            "open('_invent_runtime.py', 'w').write("
            f"{_DONKEY_RUNTIME_MODULE!r})"
        )
        await self.execute("from _invent_runtime import *")
        self._ready = True
        self._set_status(DONKEY_READY)

    async def execute(self, code):
        if not self._ready and "from _invent_runtime import *" not in code:
            self._set_status(DONKEY_BUSY)
        try:
            result = await self._donkey.execute(code)
            if self._ready:
                self._set_status(DONKEY_READY)
            return result
        except Exception as exc:
            self._set_status(f"{DONKEY_ERROR}: {exc}")
            raise

    async def evaluate(self, expression):
        if not self._ready:
            raise RuntimeError("Donkey is not ready yet")
        self._set_status(DONKEY_BUSY)
        try:
            result = await self._donkey.evaluate(expression)
            self._set_status(DONKEY_READY)
            return result
        except Exception as exc:
            self._set_status(f"{DONKEY_ERROR}: {exc}")
            raise

    async def run_code(self, code, result_key, context=None):
        """Execute code and store structured result in datastore."""
        context_json = json.dumps(context or {})
        expression = (
            "__import__('json').dumps({"
            "'ok': True, "
            "'result': invent_run_code("
            f"{code!r}, {context_json!r}"
            ")})"
        )
        try:
            payload = await self.evaluate(expression)
            invent.datastore[result_key] = json.loads(payload)
        except Exception as exc:
            invent.datastore[result_key] = {
                "ok": False,
                "error": f"{DONKEY_ERROR}: {exc}",
            }

    async def kill(self):
        await self._donkey.kill()
        self._ready = False
        self._set_status(DONKEY_KILLED)


class WidgetDonkeyAdapter:
    """
    Base adapter for attaching donkey logic to a widget-like target.

    Subclasses must implement:
    - _context()
    - _apply_result(payload)
    """

    def __init__(self, status_key, result_key):
        self._status_key = status_key
        self._result_key = result_key
        self._connection = None

    @property
    def ready(self):
        return self._connection is not None and self._connection.ready

    async def initialize(self):
        # Allow subclasses to request extra packages by defining
        # `self._packages` prior to initialize() being called.
        packages = getattr(self, "_packages", None)
        self._connection = await create_donkey_connection(
            result_key=self._status_key, packages=packages
        )
        # Give subclasses a chance to prepare the worker (write
        # modules, import helpers, etc.). Default is no-op.
        await self._prepare_worker(self._connection)

    def _context(self):
        raise NotImplementedError()

    def _apply_result(self, payload):
        raise NotImplementedError()

    async def run(self, code):
        if not self.ready:
            raise RuntimeError("Donkey is not ready yet")
        await self._connection.run_code(
            code=code,
            result_key=self._result_key,
            context=self._context(),
        )
        payload = invent.datastore.get(self._result_key)
        try:
            return self._apply_result(payload)
        except Exception as exc:
            result = {
                "ok": False,
                "error": f"{DONKEY_ERROR}: {exc}",
            }
            invent.datastore[self._result_key] = result
            return result

    async def _prepare_worker(self, connection):
        """Optional hook called after the connection is created.

        Subclasses may override to write files into the worker and
        import helper modules. The default implementation does
        nothing.
        """
        return None

    async def kill(self):
        if self._connection is not None:
            await self._connection.kill()


class ChartDonkeyAdapter(WidgetDonkeyAdapter):
    """
    Attach donkey-driven Python logic to a Chart widget.

    The adapter expects plugin code to assign `result` as a dictionary
    containing optional `data` and `options` keys for chart updates.
    """

    def __init__(self, chart_widget, status_key, result_key):
        super().__init__(status_key=status_key, result_key=result_key)
        self._chart = chart_widget

    def _context(self):
        return {
            "chart_type": self._chart.chart_type,
            "data": self._chart.data,
            "options": self._chart.options,
        }

    def _apply_result(self, payload):
        if not isinstance(payload, dict):
            raise ValueError("Result payload must be a dict.")
        if not payload.get("ok"):
            return payload
        result = payload.get("result")
        if not isinstance(result, dict):
            raise ValueError("Result value must be a dict.")
        if "data" in result:
            self._chart.data = result["data"]
        if "options" in result:
            self._chart.options = result["options"]
        return payload


class CodeEditorDonkeyAdapter(WidgetDonkeyAdapter):
    """
    Run donkey logic from a CodeEditor and update an output target.

    The output target must provide a writable `text` attribute.
    """

    def __init__(
        self,
        code_editor_widget,
        output_widget,
        status_key,
        result_key,
    ):
        super().__init__(status_key=status_key, result_key=result_key)
        self._code_editor = code_editor_widget
        self._output = output_widget

    def _context(self):
        return {
            "editor_code": self._code_editor.code or "",
        }

    def _apply_result(self, payload):
        if not isinstance(payload, dict):
            raise ValueError("Result payload must be a dict.")
        if not payload.get("ok"):
            return payload
        result = payload.get("result")
        if not isinstance(result, dict):
            raise ValueError("Result value must be a dict.")
        message = result.get("output")
        if message is None:
            raise ValueError("Result must include an `output` value.")
        self._output.text = str(message)
        return payload


class WebcamDonkeyAdapter(WidgetDonkeyAdapter):
    """
    Attach OpenCV donkey logic to a Webcam widget.

    The worker executes user code with a pre-built image namespace
    (image_bgr, image_rgb, grey, cv2, np). User code must assign a
    numpy ndarray to `result_image` or `result`. The processed frame
    is displayed via the webcam widget's `show_image()` method.
    """

    def __init__(self, webcam_widget, status_key, result_key):
        super().__init__(status_key=status_key, result_key=result_key)
        self._webcam = webcam_widget
        # Request OpenCV and numpy packages when creating the worker.
        self._packages = ["opencv-python", "numpy"]

    async def _prepare_worker(self, connection):
        # Write the OpenCV helper module into the worker and import it.
        await connection.execute(
            f"open('_opencv_worker.py', 'w').write({_OPENCV_WORKER_MODULE!r})"
        )
        await connection.execute("from _opencv_worker import *")

    def _context(self):
        # Not used; OpenCV worker uses its own entrypoint.
        return {}

    def _apply_result(self, payload):
        if not isinstance(payload, dict):
            raise ValueError("Result payload must be a dict.")
        if not payload.get("ok"):
            return payload
        data_url = payload.get("data_url")
        if not data_url:
            raise ValueError("Result must include a data_url value.")
        self._webcam.show_image(data_url)
        return payload

    async def run(self, code):
        if not self.ready:
            raise RuntimeError("Donkey is not ready yet")

        capture = self._webcam.latest_capture(media_type="photo")
        if capture is None:
            raise ValueError("No photo captured yet. Take a photo first.")
        data_url = capture.get("data_url")
        if not data_url:
            raise ValueError("Latest capture has no data_url.")

        expression = (
            "__import__('json').dumps(worker_run_user_code("
            f"{code!r}, {data_url!r}"
            "))"
        )
        try:
            payload_str = await self._connection.evaluate(expression)
            payload = json.loads(payload_str)
            invent.datastore[self._result_key] = payload
        except Exception as exc:
            payload = {"ok": False, "error": f"{DONKEY_ERROR}: {exc}"}
            invent.datastore[self._result_key] = payload

        try:
            return self._apply_result(payload)
        except Exception as exc:
            result = {"ok": False, "error": f"{DONKEY_ERROR}: {exc}"}
            invent.datastore[self._result_key] = result
            return result


async def create_donkey_connection(result_key=None, packages=None):
    """
    Create a donkey connection for Python code execution.

    Each call creates a new worker instance. The framework manages
    worker options internally.
    """
    if result_key:
        invent.datastore[result_key] = DONKEY_CREATING

    (core,) = await js_import(_PYSCRIPT_CORE)
    terminal_selector = _ensure_terminal_div()
    options = to_js(
        {
            "type": "py",
            "persistent": True,
            "terminal": terminal_selector,
            "config": {"packages": packages or []},
        }
    )
    donkey = await core.donkey(options)
    connection = DonkeyConnection(donkey, result_key=result_key)
    await connection.initialize()
    return connection
