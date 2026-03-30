"""
A webcam widget for the Invent framework.

Enables photo capture and video recording with automatic downloads.
Supports live video preview from the user's webcam.

Copyright (c) 2019-present Invent contributors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from invent.i18n import _
from invent.ui.core import (
    Widget,
    ChoiceProperty,
    BooleanProperty,
    Event,
)
from pyscript.web import div, video, button, canvas
from pyscript.ffi import create_proxy


class Webcam(Widget):
    """
    A webcam widget with photo capture and video recording capabilities.

    Allows users to toggle between photo and video modes, capture images,
    and record videos. Captured files are automatically downloaded.
    Supports event callbacks for when photos or videos are captured.
    """

    mode = ChoiceProperty(
        _("The current webcam mode (photo or video)."),
        default_value="photo",
        choices=["photo", "video"],
        group="style",
    )

    show_gallery = BooleanProperty(
        _("Whether to show the gallery button."),
        default_value=True,
        group="style",
    )

    show_mode_indicator = BooleanProperty(
        _("Whether to show the mode/status indicators."),
        default_value=True,
        group="style",
    )

    photo_captured = Event(
        _("Sent when a photo is captured."),
        widget=_("The Webcam widget that captured the photo."),
    )

    video_recorded = Event(
        _("Sent when a video is recorded."),
        widget=_("The Webcam widget that recorded the video."),
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><circle cx="128" cy="128" r="32" fill="currentColor" opacity="0.2"/><path fill="currentColor" d="M208 56H48a16 16 0 0 0-16 16v112a16 16 0 0 0 16 16h160a16 16 0 0 0 16-16V72a16 16 0 0 0-16-16m0 128H48V72h160zM128 96a32 32 0 1 0 32 32a32 32 0 0 0-32-32m0 48a16 16 0 1 1 16-16a16 16 0 0 1-16 16"/></svg>'  # noqa

    def trigger(self):
        """
        Trigger the current action (capture photo or start/stop recording).
        """
        if hasattr(self, "_shutter_btn"):
            self._shutter_btn.click()

    def set_mode(self, mode):
        """
        Set the webcam mode to 'photo' or 'video'.
        """
        if mode in ["photo", "video"]:
            self.mode = mode
            if hasattr(self, "_mode_buttons"):
                self._update_mode_buttons()

    def capture_photo(self):
        """
        Capture a photo from the current video stream.
        """
        if hasattr(self, "_canvas") and hasattr(self, "_video_elem"):
            ctx = self._canvas.getContext("2d")
            ctx.drawImage(
                self._video_elem,
                0,
                0,
                self._canvas.width,
                self._canvas.height,
            )
            # Trigger download
            self._download_canvas_as_image()
            self.publish("photo_captured", widget=self)

    def start_recording(self):
        """
        Start recording video from the webcam.
        """
        if hasattr(self, "_recorder"):
            if not self._recording:
                self._recording = True
                self._recorder.start()

    def stop_recording(self):
        """
        Stop recording and trigger download of the video file.
        """
        if hasattr(self, "_recorder") and self._recording:
            self._recording = False
            self._recorder.stop()
            self.publish("video_recorded", widget=self)

    def on_mode_changed(self):
        """
        Handle mode change by updating button states.
        """
        if hasattr(self, "_mode_buttons"):
            self._update_mode_buttons()
        if hasattr(self, "_mode_indicator"):
            self._mode_indicator.textContent = self._mode_label()

    def _mode_label(self):
        """
        Return the display label for the current mode.
        """
        if self.mode == "video":
            return "Video Mode"
        return "Photo Mode"

    def _update_mode_buttons(self):
        """
        Update the visual state of mode buttons based on current mode.
        """
        for btn_info in self._mode_buttons:
            btn = btn_info["element"]
            btn_mode = btn_info["mode"]
            if btn_mode == self.mode:
                btn.classes.add("invent-webcam-mode-active")
            else:
                btn.classes.remove("invent-webcam-mode-active")

    def _download_canvas_as_image(self):
        """
        Download the canvas content as an image file.
        """
        try:
            from pyscript import window

            link = window.document.createElement("a")
            link.href = self._canvas.toDataURL("image/jpeg")
            link.download = f"photo-{window.Date().now()}.jpg"
            window.document.body.appendChild(link)
            link.click()
            window.document.body.removeChild(link)
        except Exception as e:
            print(f"Error downloading photo: {e}")

    def _on_shutter_click(self, event):
        """
        Handle shutter button clicks.
        """
        if self.mode == "photo":
            self.capture_photo()
        else:
            if self._recording:
                self.stop_recording()
            else:
                self.start_recording()

    def _setup_webcam_stream(self):
        """
        Initialize the webcam stream with proper error handling.
        """
        try:
            from pyscript import window

            navigator = window.navigator
            if not navigator.mediaDevices:
                print("Camera not supported in this browser")
                return

            constraints = {
                "video": {
                    "width": {"ideal": 1280},
                    "height": {"ideal": 720},
                    "facingMode": "user",
                },
                "audio": True,
            }

            async def get_stream():
                try:
                    stream = await navigator.mediaDevices.getUserMedia(
                        constraints
                    )
                    self._video_elem.srcObject = stream
                    self._setup_recorder(stream)
                    if self.show_mode_indicator:
                        self._status_elem.textContent = "Webcam ready"
                except Exception as e:
                    print(f"Camera access denied or error: {e}")
                    if self.show_mode_indicator:
                        self._status_elem.textContent = "Camera access denied"

            # Handle promise
            import asyncio

            asyncio.create_task(get_stream())

        except Exception as e:
            print(f"Error setting up webcam: {e}")

    def _setup_recorder(self, stream):
        """
        Set up the MediaRecorder for video recording.
        """
        try:
            from pyscript import window

            chunks = []

            def on_dataavailable(event):
                if event.data.size > 0:
                    chunks.append(event.data)

            def on_stop():
                blob = window.Blob(chunks, {"type": "video/webm"})
                link = window.document.createElement("a")
                url = window.URL.createObjectURL(blob)
                link.href = url
                link.download = f"video-{window.Date().now()}.webm"
                link.click()
                window.URL.revokeObjectURL(url)

            recorder = window.MediaRecorder(stream)
            recorder.addEventListener(
                "dataavailable", create_proxy(on_dataavailable)
            )
            recorder.addEventListener("stop", create_proxy(on_stop))

            self._recorder = recorder
            self._recording = False
        except Exception as e:
            print(f"Error setting up recorder: {e}")

    def render(self):
        """
        Render the webcam widget with controls.
        """
        # Hidden canvas for photo capture
        self._canvas = canvas()
        self._canvas.width = 1280
        self._canvas.height = 720
        self._canvas.style.display = "none"

        # Video element for preview
        self._video_elem = video()
        self._video_elem.id = f"{self.id}-video"
        self._video_elem.autoplay = True
        self._video_elem.muted = True
        self._video_elem.classes.add("invent-webcam-video")

        video_container = div(self._video_elem)
        video_container.classes.add("invent-webcam-box")

        # Mode buttons
        photo_btn = button("Photo")
        photo_btn.id = f"{self.id}-photo-btn"
        photo_btn.classes.add("invent-webcam-mode-btn")
        photo_btn.classes.add("invent-webcam-mode-active")
        photo_btn._dom_element.addEventListener(
            "click",
            create_proxy(lambda e: self.set_mode("photo")),
        )

        video_btn = button("Video")
        video_btn.id = f"{self.id}-video-btn"
        video_btn.classes.add("invent-webcam-mode-btn")
        video_btn._dom_element.addEventListener(
            "click",
            create_proxy(lambda e: self.set_mode("video")),
        )

        self._mode_buttons = [
            {"element": photo_btn, "mode": "photo"},
            {"element": video_btn, "mode": "video"},
        ]

        modes_container = div(photo_btn, video_btn)
        modes_container.classes.add("invent-webcam-modes")

        # Shutter button
        self._shutter_btn = button("Take")
        self._shutter_btn.id = f"{self.id}-shutter"
        self._shutter_btn.classes.add("invent-webcam-shutter")
        self._shutter_btn._dom_element.addEventListener(
            "click", create_proxy(self._on_shutter_click)
        )

        shutter_container = div(self._shutter_btn)
        shutter_container.classes.add("invent-webcam-shutter-container")

        # Gallery button
        gallery_btn = button("Gallery")
        gallery_btn.id = f"{self.id}-gallery-btn"
        gallery_btn.classes.add("invent-webcam-gallery-btn")

        gallery_container = div(gallery_btn) if self.show_gallery else div()
        gallery_container.classes.add("invent-webcam-gallery")

        # Controls container
        controls = div(modes_container, shutter_container, gallery_container)
        controls.classes.add("invent-webcam-actions")

        # Status indicators
        self._status_elem = div("Initializing camera...")
        self._status_elem.id = f"{self.id}-status"
        self._status_elem.classes.add("invent-webcam-status")

        self._mode_indicator = div(self._mode_label())
        self._mode_indicator.id = f"{self.id}-mode-indicator"
        self._mode_indicator.classes.add("invent-webcam-mode-indicator")

        indicators = div(self._status_elem, self._mode_indicator)
        indicators.classes.add("invent-webcam-indicators")
        if not self.show_mode_indicator:
            indicators.style.display = "none"

        # Main container
        element = div(
            self._canvas,
            video_container,
            controls,
            indicators,
            id=self.id,
        )
        element.classes.add("invent-webcam")

        # Initialize the webcam stream
        self._setup_webcam_stream()

        return element
