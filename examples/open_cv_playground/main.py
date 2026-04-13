"""
OpenCV playground with a camera-only webcam widget and Donkey worker pipeline.
"""

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
    max_captures=5,
)

opencv_webcam = Webcam(
    photo_output="preview",
    max_captures=5,
)

opencv_output = Image(
    width="100%",
)

opencv_status = Label(
    text="Donkey idle. Press 'Start Donkey' to initialize the worker.",
)

opencv_worker = None


async def ensure_worker():
    """Start the Donkey worker and bootstrap OpenCV when needed."""
    global opencv_worker
    if opencv_worker is not None and opencv_worker.ready:
        opencv_status.text = "Donkey ready."
        return
    opencv_status.text = "Starting Donkey worker..."
    try:
        opencv_worker = await create_opencv_donkey(
            result_key="opencv.worker.status"
        )
        opencv_status.text = (
            "Donkey ready. Capture a photo and choose an action."
        )
    except Exception as exc:
        opencv_status.text = f"Failed to start donkey worker: {exc}"


def _latest_capture_data_url():
    capture = opencv_webcam.latest_capture(media_type="photo")
    if capture is None:
        return None
    return capture.get("data_url")


async def run_worker_action(action):
    if opencv_worker is None or not opencv_worker.ready:
        opencv_status.text = "Donkey is not ready. Press 'Start Donkey' first."
        return

    data_url = _latest_capture_data_url()
    if not data_url:
        opencv_status.text = "Capture a photo first, then run an action."
        return

    opencv_status.text = f"Running {action}..."
    try:
        result = await opencv_worker.run(action, data_url)
    except Exception as exc:
        opencv_status.text = f"Worker error: {exc}"
        return

    if isinstance(result, dict) and result.get("ok"):
        processed_data_url = result.get("data_url")
        if processed_data_url:
            opencv_output.image = processed_data_url
        if action == "find_face":
            face_count = result.get("count", 0)
            opencv_status.text = f"Done. Faces found: {face_count}."
        else:
            opencv_status.text = "Done. Outline generated."
        return

    opencv_status.text = "Worker returned no displayable result."


async def handle_opencv_controls(message):
    button_name = getattr(message.source, "name", "")

    if button_name == "start_donkey_button":
        await ensure_worker()
        return

    if button_name == "find_face_button":
        await run_worker_action("find_face")
        return

    if button_name == "outline_button":
        await run_worker_action("outline")


invent.subscribe(
    handle_opencv_controls,
    to_channel="opencv-controls",
    when_subject=["press"],
)


# Lazy boot so the first interaction is still explicit via Start Donkey.
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
                        "The webcam remains lightweight and only captures images. "
                        "OpenCV runs in a Donkey worker. "
                        "Press **Start Donkey**, capture a photo, then run **Find Face** "
                        "or **Outline**."
                    )
                ),
                opencv_webcam,
                Button(
                    text="Start Donkey",
                    name="start_donkey_button",
                    purpose="PRIMARY",
                    channel="opencv-controls",
                ),
                Button(
                    text="Find Face",
                    name="find_face_button",
                    channel="opencv-controls",
                ),
                Button(
                    text="Outline",
                    name="outline_button",
                    channel="opencv-controls",
                ),
                opencv_status,
                Label(text="Processed output"),
                opencv_output,
            ],
        ),
    ],
)

# GO! ##################################################################################

invent.go()
