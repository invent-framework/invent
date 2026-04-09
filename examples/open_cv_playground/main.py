"""
This app is a simple test card for the theme system. We ensure all the various
UI aspects of the Invent framework are shown in a page, and allow the user to
select different "themes" to see how they affect the appearance of the page.
"""

import base64
import html as html_lib
import io
import random

import cv2
import numpy as np
from PIL import Image as PILImage

import invent
from invent.ui import *

# Datastore ############################################################################

await invent.setup(
    richtext="This is a **rich text editor**. It supports _formatting_, [links](https://inventframework.org/), and more!"
)

# Code #################################################################################

# Create some sample appointments for the calendar widget based upon today's month and
# year, so that the calendar will show some appointments when it is rendered. Needs to
# include both just plain dates, and datetimes with times, to show how both are rendered.
from datetime import date, datetime


def navigate(message):
    """
    Handle navigation between pages based on button clicks / names.
    """
    # Extract the page name from the button name. The button names are in the format
    # "pagename_button", so we split on "_button" and take the first part to get the page
    # name.
    page_name = message.source.name.split("_button")[0]
    invent.show_page(page_name)


invent.subscribe(navigate, to_channel="navigate", when_subject=["press"])


# Some random funky backgrounds for page 4. It's just boring CSS.
backgrounds = [
    "linear-gradient(to bottom, #ff7e5f, #feb47b)",  # Linear gradient.
    "#3498db",  # A solid single colour.
    f"linear-gradient(var(--bg-image-overlay), var(--bg-image-overlay)), url('{invent.media.images.repeat_image.png}') repeat",  # A repeated image.
    f"linear-gradient(var(--bg-image-overlay), var(--bg-image-overlay)), url('{invent.media.images.random.png}') center / cover no-repeat",  # A centered, cover image.
]


# Pre-define some webcam variations
preview_webcam = Webcam(
    photo_output="download",
    max_captures=5,
)

opencv_webcam = Webcam(
    opencv_mode=True,
    photo_output="preview",
    max_captures=5,
)


# Keep the webcam's code in sync whenever the editor changes.
def _on_code_changed(message):
    opencv_webcam._opencv_code = message.code

opencv_code_editor = CodeEditor(
    theme="light",
    code=opencv_webcam._DEFAULT_OPENCV_CODE,
)

invent.subscribe(
    _on_code_changed,
    to_channel=opencv_code_editor.channel,
    when_subject="changed",
)


def run_opencv_from_button(message):
    """Run OpenCV using the current code in the editor."""
    opencv_webcam.run_opencv()


invent.subscribe(
    run_opencv_from_button,
    to_channel="opencv-controls",
    when_subject=["press"],
)

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
                        "Snap a photo above, edit the snippet, then press "
                        "**Run OpenCV (channel button)**. Available names: `capture`, `image`, "
                        "`array_of_rgb`, `array_of_bgr`, `grey`, `cv2`, `np`, "
                        "`PILImage`. Assign any of `result_image`, "
                        "`processed_image`, `output_image`, or `result` to "
                        "display the output."
                    )
                ),
                opencv_webcam,
                Button(
                    text="Run OpenCV",
                    purpose="PRIMARY",
                    channel="opencv-controls",
                ),
                opencv_code_editor,
            ],
        ),
    ],
)

# GO! ##################################################################################

invent.go()