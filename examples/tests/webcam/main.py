import asyncio

import invent
from invent.tools import (
    StatusProxy,
    WebcamDonkeyAdapter,
    fail_html,
    make_assertion_callbacks,
    make_plugin_runner,
    pass_html,
    wait_html,
)
from invent.ui import *

await invent.setup()

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
status = StatusProxy(opencv_status, "opencv")


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


adapter = WebcamDonkeyAdapter(
    webcam_widget=opencv_webcam,
    status_key="opencv.worker.status",
    result_key="opencv.worker.result",
)

# Assertions and plugin runner wiring
assert_worker = Html(html=wait_html("Worker not started."))
assert_run = Html(html=wait_html("Code not run."))
callbacks = make_assertion_callbacks(
    worker_assert_widget=assert_worker,
    run_assert_widget=assert_run,
    pass_html=pass_html,
    fail_html=fail_html,
)

flow, ensure_worker, run_plugin_code = make_plugin_runner(
    adapter=adapter,
    status_widget=status,
    code_getter=lambda: opencv_code_editor.code or "",
    success_text="Done. Custom OpenCV code executed.",
    **callbacks,
)


async def handle_opencv_controls(message):
    if getattr(message.source, "name", "") == "run_code_button":
        await run_plugin_code()


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
