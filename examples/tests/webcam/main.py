import asyncio

import invent
from invent.tools import create_opencv_donkey
from invent.ui import *

# Datastore ############################################################################

await invent.setup()

# Code #################################################################################

# Pre-define some webcam variations
preview_webcam = Webcam(
    photo_output="download",
)

opencv_webcam = Webcam(
    photo_output="preview",
    preview_layout="side-by-side",
    mode="photo",
)


opencv_status = Label(text="Donkey starting...")


def _set_opencv_status(text):
    """Set the on-page label and publish a status message.

    Publishing to the `opencv` channel with subject `status` lets test
    harnesses subscribe for assertions.
    """
    opencv_status.text = text
    invent.publish(
        invent.Message("status", status=text), to_channel="opencv"
    )

default_code = (
    "# Available variables: image_bgr, image_rgb, grey, cv2, np\n"
    "# Set result_image (or result) to a numpy ndarray.\n"
    "# Example: start with the current frame and modify it however you like.\n\n"
    "result_image = image_bgr.copy()\n"
)

opencv_code_editor = CodeEditor(
    code=default_code,
    language="python",
    min_height="280px",
)

opencv_worker = None


async def ensure_worker():
    """Start the Donkey worker and bootstrap OpenCV when needed."""
    global opencv_worker
    if opencv_worker is not None and opencv_worker.ready:
        _set_opencv_status("Donkey ready.")
        return
    _set_opencv_status("Starting Donkey worker...")
    try:
        opencv_worker = await create_opencv_donkey(
            result_key="opencv.worker.status"
        )
        _set_opencv_status(
            "Donkey ready. Capture a photo and run your code."
        )
    except Exception as exc:
        _set_opencv_status(f"Failed to start donkey worker: {exc}")


def _latest_capture_data_url():
    capture = opencv_webcam.latest_capture(media_type="photo")
    if capture is None:
        return None
    return capture.get("data_url")


async def run_worker_code():
    if opencv_worker is None or not opencv_worker.ready:
        _set_opencv_status(
            "Donkey is not ready. Press 'Start Donkey' first."
        )
        return

    data_url = _latest_capture_data_url()
    if not data_url:
        _set_opencv_status(
            "Capture a photo first, then run an action."
        )
        return

    code = opencv_code_editor.code or ""
    if not code.strip():
        _set_opencv_status("Write some OpenCV code first.")
        return
    _set_opencv_status("Running code...")
    try:
        result = await opencv_worker.run_code(code, data_url)
    except Exception as exc:
        _set_opencv_status(f"Worker error: {exc}")
        return

    if result is None:
        opencv_status.text = "Worker returned no result."
        return

    getter = getattr(result, "get", None)
    if callable(getter):
        ok = getter("ok")
        processed_data_url = getter("data_url")
    else:
        ok = False
        processed_data_url = None

    if ok:
        if processed_data_url:
            opencv_webcam.show_image(processed_data_url)
        _set_opencv_status("Done. Custom OpenCV code executed.")
        return
    _set_opencv_status(
        f"Worker returned no displayable result ({type(result).__name__})."
    )


async def handle_opencv_controls(message):
    button_name = getattr(message.source, "name", "")

    if button_name == "run_code_button":
        await run_worker_code()


invent.subscribe(
    handle_opencv_controls,
    to_channel="opencv-controls",
    when_subject=["press"],
)


# Lazy boot so the worker starts automatically when the page loads.
asyncio.create_task(ensure_worker())

# User Interface #######################################################################

app = invent.App(
    name="Theme Testcard",
    pages=[
        Page(
            id="testcard",
            children=[
                Label(text="# Invent Test Card"),
                Label(
                    text="This is a test card for the Invent framework. It includes all the different widgets and components in the framework, so that we can see how they look with different themes applied."
                ),
                Label(text="## Standard webcam"),
                preview_webcam,
                Label(text="## OpenCV webcam playground"),
                Label(
                    text=(
                        "Take a photo, write your OpenCV code, and then press **Run Code**."
                    )
                ),
                opencv_webcam,
                Button(
                    text="Run Code",
                    name="run_code_button",
                    channel="opencv-controls",
                ),
                opencv_code_editor,
                opencv_status,
            ],
        ),
    ],
)

# GO! ##################################################################################

invent.go()
