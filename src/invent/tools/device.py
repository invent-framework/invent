"""
Device related helpers.

This module contains helpers for running heavyweight device processing in a
PyScript Donkey worker whilst keeping UI widgets lightweight.
"""

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


# The OpenCV worker code written to the worker's virtual filesystem as a
# proper Python module. Using execute("from _opencv_worker import *") then
# pulls everything into the worker's global scope, which is the only
# reliable way to define persistent callables in a donkey worker —
# process() chokes on large multiline strings via xterm-readline, and
# execute() alone scopes defs locally and discards them.
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

    exec(user_code, namespace, namespace)  # noqa: S102

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


_PYSCRIPT_CORE = "https://pyscript.net/releases/2026.3.1/core.js"


def _ensure_terminal_div(terminal_id="donkey-terminal"):
    """Create a hidden terminal container in the DOM if it doesn't exist yet."""
    if document.getElementById(terminal_id) is None:
        div = document.createElement("div")
        div.id = terminal_id
        div.style.display = "none"
        document.body.appendChild(div)
    return f"#{terminal_id}"


class OpenCVDonkey:
    """Thin wrapper around a PyScript donkey used for OpenCV processing."""

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
        # Write the module to the worker's virtual filesystem as a proper
        # .py file, then import it into global scope with execute().
        # This sidesteps two known donkey limitations:
        #   - process() feeds code through xterm-readline line-by-line,
        #     which breaks on large multiline strings.
        #   - execute() uses exec() which scopes `def` statements locally
        #     and discards them after the call returns.
        # Writing a file and importing it is the correct pattern.
        await self._donkey.execute(
            f"open('_opencv_worker.py', 'w').write({_OPENCV_WORKER_MODULE!r})"
        )
        await self._donkey.execute("from _opencv_worker import *")
        self._ready = True
        self._set_status(DONKEY_READY)

    async def run_code(self, code, data_url):
        if not self._ready:
            raise RuntimeError("Donkey is not ready yet")
        self._set_status(DONKEY_BUSY)
        try:
            payload = await self._donkey.evaluate(
                "__import__('json').dumps(worker_run_user_code("
                f"{code!r}, {data_url!r}"
                "))"
            )
            result = json.loads(payload)
            self._set_status(DONKEY_READY)
            return result
        except Exception as exc:
            self._set_status(f"{DONKEY_ERROR}: {exc}")
            raise

    async def kill(self):
        await self._donkey.kill()
        self._ready = False
        self._set_status(DONKEY_KILLED)


async def create_opencv_donkey(result_key=None, *, packages=None):
    """
    Create and initialise an OpenCV donkey worker.

    Parameters
    ----------
    result_key : str | None
        Datastore key for status updates, e.g. "opencv.worker.status".
    packages : list[str] | None
        Extra packages to install in the worker (opencv-python and numpy
        are always included).
    """
    if packages is None:
        packages = []

    base_packages = ["opencv-python", "numpy"]
    all_packages = base_packages + [
        p for p in packages if p not in base_packages
    ]

    if result_key:
        invent.datastore[result_key] = DONKEY_CREATING

    # Import donkey directly from the PyScript ES module — no HTML bridge needed.
    (core,) = await js_import(_PYSCRIPT_CORE)
    # Create the hidden terminal div programmatically so index.html stays clean.
    terminal_selector = _ensure_terminal_div()

    options = to_js(
        {
            "type": "py",
            "persistent": True,
            "terminal": terminal_selector,
            "config": {"packages": all_packages},
        }
    )

    donkey = await core.donkey(options)

    worker = OpenCVDonkey(donkey, result_key=result_key)
    await worker.initialize()
    return worker
