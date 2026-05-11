import invent
import sys
import os
from pathlib import Path
from invent.tools import make_helper
from invent.ui import *

from invent.tools.common_ui import (
    fail_html,
    make_status_setter,
    pass_html,
    publish_run,
    wait_html,
)

await invent.setup()

preview_webcam = Webcam(
    photo_output="download",
)

opencv_webcam = Webcam(
    photo_output="preview",
    preview_layout="side-by-side",
    mode="photo",
)

opencv_status = Label(text="Donkey starting...")
_set_opencv_status = make_status_setter(
    invent, opencv_status, channel="opencv"
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

assert_worker = Html(html=wait_html("Worker not started."))
assert_run = Html(html=wait_html("Code not run."))

HELPER_CHANNEL = "opencv-helper"

make_helper(
    src="opencv_helper.py",
    channel=HELPER_CHANNEL,
    config={"packages": ["opencv-python", "numpy"]},
)


def handle_helper_status(msg):
    state = getattr(msg, "state", None)
    detail = getattr(msg, "detail", None)
    if state == "starting":
        _set_opencv_status("Starting Donkey worker...")
    elif state == "ready":
        _set_opencv_status("Donkey ready. Capture a photo and run your code.")
        assert_worker.html = pass_html("Donkey worker ready.")
    elif state == "busy":
        _set_opencv_status("Running code...")
    elif state == "error":
        _set_opencv_status(f"Failed to start donkey worker: {detail}")
        assert_worker.html = fail_html(f"Donkey worker failed: {detail}")


def handle_helper_result(msg):
    if msg.function != "process":
        return
    if msg.error:
        _set_opencv_status(f"Worker error: {msg.error}")
        assert_run.html = fail_html(f"Code run failed: {msg.error}")
        return
    result = msg.result
    getter = getattr(result, "get", None)
    if callable(getter) and getter("ok"):
        processed = getter("data_url")
        if processed:
            opencv_webcam.show_image(processed)
        assert_run.html = pass_html("Code run succeeded.")
        _set_opencv_status("Done. Custom OpenCV code executed.")
        return
    assert_run.html = fail_html("Worker result did not include ok/data_url.")
    _set_opencv_status(
        f"Worker returned no displayable result ({type(result).__name__})."
    )


invent.subscribe(handle_helper_status, HELPER_CHANNEL, "status")
invent.subscribe(handle_helper_result, HELPER_CHANNEL, "result")


def _latest_capture_data_url():
    capture = opencv_webcam.latest_capture(media_type="photo")
    if capture is None:
        return None
    return capture.get("data_url")


async def handle_opencv_controls(message):
    button_name = getattr(message.source, "name", "")

    if button_name != "run_code_button":
        return

    data_url = _latest_capture_data_url()
    if not data_url:
        _set_opencv_status("Capture a photo first, then run an action.")
        return

    code = opencv_code_editor.code or ""
    if not code.strip():
        _set_opencv_status("Write some OpenCV code first.")
        return

    publish_run(
        invent,
        channel=HELPER_CHANNEL,
        function="process",
        args=[code, data_url],
    )


invent.subscribe(
    handle_opencv_controls,
    to_channel="opencv-controls",
    when_subject=["press"],
)

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
                Label(text="## Assertions"),
                assert_worker,
                assert_run,
            ],
        ),
    ],
)

invent.go()
