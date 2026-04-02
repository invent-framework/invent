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
import time
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
    """

    mode = ChoiceProperty(
        _("Webcam mode: photo, video, or both."),
        default_value="both",
        choices=["photo", "video", "both"],
        group="style",
    )

    show_mode_indicator = BooleanProperty(
        _("Whether to show the mode/status indicators."),
        default_value=True,
        group="style",
    )

    photo_captured = Event(
        _("Sent when a photo is captured."),
        webcam=_("The Webcam widget that captured the photo."),
    )

    video_recorded = Event(
        _("Sent when a video is recorded."),
        webcam=_("The Webcam widget that recorded the video."),
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
        Set the active webcam mode when switching is enabled.
        """
        if self.mode != "both":
            return
        if mode in ["photo", "video"]:
            self._active_mode = mode
            if hasattr(self, "_mode_buttons"):
                self._update_mode_buttons()
            if hasattr(self, "_mode_indicator"):
                self._mode_indicator._dom_element.textContent = (
                    self._mode_label()
                )
            if hasattr(self, "_shutter_btn"):
                self._set_shutter_text()

    def _current_mode(self):
        """
        Return the active mode used for behavior and UI labels.
        """
        if self.mode == "both":
            return getattr(self, "_active_mode", "photo")
        return self.mode

    def capture_photo(self):
        """
        Capture a photo from the current video stream.
        """
        if hasattr(self, "_canvas") and hasattr(self, "_video_elem"):
            video_el = self._video_elem._dom_element
            canvas_el = self._canvas._dom_element

            width = video_el.videoWidth or 1280
            height = video_el.videoHeight or 720
            canvas_el.width = width
            canvas_el.height = height

            ctx = canvas_el.getContext("2d")
            ctx.drawImage(
                video_el,
                0,
                0,
                width,
                height,
            )
            # Trigger download
            self._download_canvas_as_image()
            self.publish(self.photo_captured, webcam=self)

    def _set_status(self, text):
        """
        Update the status indicator text.
        """
        if not hasattr(self, "_status_elem"):
            return
        self._status_elem._dom_element.textContent = text

    def _timestamp(self):
        """
        Return a millisecond timestamp for generated filenames.
        """
        return int(time.time() * 1000)

    def start_recording(self):
        """
        Start recording video from the webcam.
        """
        if hasattr(self, "_recorder"):
            if not self._recording and self._recorder.state == "inactive":
                self._recorded_chunks = []
                self._recording = True
                self._recorder.start()
                self._shutter_btn.classes.add("recording")
                self._set_shutter_text()
                self._set_status("Recording...")

    def stop_recording(self):
        """
        Stop recording and trigger download of the video file.
        """
        if (
            hasattr(self, "_recorder")
            and self._recording
            and self._recorder.state == "recording"
        ):
            self._recording = False
            self._recorder.stop()
            self._shutter_btn.classes.remove("recording")
            self._set_shutter_text()
            self._set_status("Saving video...")

    def on_mode_changed(self):
        """
        Apply all mode-dependent configuration to the already-rendered DOM.
        The framework calls this after the widget's properties are set,
        so self.mode is reliable here (unlike during render()).
        """
        if not hasattr(self, "_controls"):
            # render() hasn't run yet; nothing to configure
            return

        # Set active mode
        self._active_mode = "photo" if self.mode == "both" else self.mode

        # Rebuild controls: remove any existing modes container, then
        # prepend one only when mode='both'.
        controls_el = self._controls._dom_element
        # Remove any previously inserted modes container
        if hasattr(self, "_modes_container"):
            try:
                controls_el.removeChild(self._modes_container._dom_element)
            except Exception:
                pass
            self._modes_container = None
            self._mode_buttons = []

        if self.mode == "both":
            self._modes_container = self._build_mode_buttons()
            controls_el.insertBefore(
                self._modes_container._dom_element,
                self._shutter_container._dom_element,
            )
        else:
            self._mode_buttons = []

        # Update shutter label and mode indicator text
        self._set_shutter_text()
        if hasattr(self, "_mode_indicator"):
            self._mode_indicator._dom_element.textContent = self._mode_label()

        # Apply show_mode_indicator
        if hasattr(self, "_indicators"):
            if self.show_mode_indicator:
                self._indicators.classes.remove("hidden")
            else:
                self._indicators.classes.add("hidden")

    def _mode_label(self):
        """
        Return the display label for the current mode.
        """
        if self._current_mode() == "video":
            return "Video Mode"
        return "Photo Mode"

    def _update_mode_buttons(self):
        """
        Update the visual state of mode buttons based on current mode.
        """
        for btn_info in self._mode_buttons:
            btn = btn_info["element"]
            btn_mode = btn_info["mode"]
            if btn_mode == self._current_mode():
                btn.classes.add("invent-webcam-mode-active")
                btn.classes.add("active")
            else:
                btn.classes.remove("invent-webcam-mode-active")
                btn.classes.remove("active")

    def _set_shutter_text(self):
        """
        Keep shutter text aligned with current mode and recording state.
        """
        if not hasattr(self, "_shutter_btn"):
            return
        is_recording = getattr(self, "_recording", False)
        if self._current_mode() == "video":
            text = "Stop" if is_recording else "Record"
        else:
            text = "Take"
        self._shutter_btn._dom_element.textContent = text

    def _download_canvas_as_image(self):
        """
        Download the canvas content as an image file.
        """
        try:
            from pyscript import window

            link = window.document.createElement("a")
            link.href = self._canvas._dom_element.toDataURL("image/jpeg")
            link.download = f"photo-{self._timestamp()}.jpg"
            link.click()
        except Exception as e:
            print(f"Error downloading photo: {e}")

    def _on_shutter_click(self, event):
        """
        Handle shutter button clicks.
        """
        if self._current_mode() == "photo":
            self.capture_photo()
        else:
            if self._recording:
                self.stop_recording()
            else:
                self.start_recording()

    def _setup_webcam_stream(self):
        try:
            from pyscript import window

            navigator = window.navigator
            if not navigator.mediaDevices:
                print("Camera not supported in this browser")
                return

            viewport_width = max(
                320, min(int(window.innerWidth or 1280), 1280)
            )
            viewport_height = max(240, int(viewport_width * 9 / 16))

            constraints = {
                "video": {
                    "width": {"ideal": viewport_width},
                    "height": {"ideal": viewport_height},
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
                    self._set_status("Webcam ready")
                    if self.mode in ("video", "both"):
                        self._setup_recorder(stream)
                except Exception as e:
                    print(f"Camera access denied or error: {e}")
                    self._set_status("Camera access denied")

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

            def on_dataavailable(event):
                if event.data.size > 0:
                    self._recorded_chunks.append(event.data)

            def on_stop(event):
                if not self._recorded_chunks:
                    self._set_status("No video captured")
                    return

                blob = window.Blob.new(
                    self._recorded_chunks, {"type": "video/webm"}
                )
                link = window.document.createElement("a")
                url = window.URL.createObjectURL(blob)
                link.href = url
                link.download = f"video-{self._timestamp()}.webm"
                link.click()
                window.URL.revokeObjectURL(url)
                self.publish(self.video_recorded, webcam=self)
                self._set_status("Video saved")

            recorder = window.MediaRecorder.new(stream)
            recorder.addEventListener(
                "dataavailable", create_proxy(on_dataavailable)
            )
            recorder.addEventListener("stop", create_proxy(on_stop))

            self._recorder = recorder
            self._recording = False
            self._recorded_chunks = []
        except Exception as e:
            print(f"Error setting up recorder: {e}")

    def _build_mode_buttons(self):
        """
        Build and return the mode toggle container for mode='both'.
        Populates self._mode_buttons as a side effect.
        """
        self._mode_buttons = []

        def build_mode_button(mode_name):
            label = "Photo" if mode_name == "photo" else "Video"
            btn = button(label)
            btn.id = f"{self.id}-{mode_name}-btn"
            btn.classes.add("invent-webcam-mode-btn")
            btn.classes.add("mode-btn")
            btn._dom_element.addEventListener(
                "click",
                create_proxy(lambda e, m=mode_name: self.set_mode(m)),
            )
            return btn

        mode_buttons = []
        for mode_name in ["photo", "video"]:
            btn = build_mode_button(mode_name)
            mode_buttons.append(btn)
            self._mode_buttons.append({"element": btn, "mode": mode_name})

        modes_container = div(*mode_buttons)
        modes_container.classes.add("invent-webcam-modes")
        modes_container.classes.add("modes")
        self._update_mode_buttons()
        return modes_container

    def render(self):
        """
        Render the webcam widget with controls.
        Mode-dependent configuration is applied in on_mode_changed,
        which the framework calls after properties are set.
        """
        # Hidden canvas for photo capture
        self._canvas = canvas()
        self._canvas.classes.add("invent-webcam-canvas-hidden")

        # Video element for preview
        self._video_elem = video()
        self._video_elem.id = f"{self.id}-video"
        self._video_elem.autoplay = True
        self._video_elem.muted = True
        self._video_elem.classes.add("invent-webcam-video")

        def on_video_ready(event):
            video_el = self._video_elem._dom_element
            canvas_el = self._canvas._dom_element
            width = video_el.videoWidth or 1280
            height = video_el.videoHeight or 720
            canvas_el.width = width
            canvas_el.height = height

        self._video_elem._dom_element.addEventListener(
            "loadedmetadata", create_proxy(on_video_ready)
        )

        video_container = div(self._video_elem)
        video_container.classes.add("invent-webcam-box")
        video_container.classes.add("webcam-box")

        # Shutter button
        self._shutter_btn = button("Take")
        self._shutter_btn.id = f"{self.id}-shutter"
        self._shutter_btn.classes.add("invent-webcam-shutter")
        self._shutter_btn.classes.add("shutter")
        self._shutter_btn._dom_element.addEventListener(
            "click", create_proxy(self._on_shutter_click)
        )

        shutter_container = div(self._shutter_btn)
        shutter_container.classes.add("invent-webcam-shutter-container")
        shutter_container.classes.add("shutter-container")

        # Controls container: starts with just the shutter;
        # on_mode_changed inserts mode toggle buttons when mode='both'.
        self._controls = div(shutter_container)
        self._controls.classes.add("invent-webcam-actions")
        self._controls.classes.add("actions")
        self._shutter_container = shutter_container

        # Status indicators
        self._status_elem = div("Initializing camera...")
        self._status_elem.id = f"{self.id}-status"
        self._status_elem.classes.add("invent-webcam-status")

        self._mode_indicator = div("")
        self._mode_indicator.id = f"{self.id}-mode-indicator"
        self._mode_indicator.classes.add("mode-selection")
        self._mode_indicator.classes.add("invent-webcam-mode-indicator")

        self._indicators = div(self._status_elem, self._mode_indicator)
        self._indicators.classes.add("invent-webcam-indicators")
        self._indicators.classes.add("indicators")

        # Main container
        element = div(
            self._canvas,
            video_container,
            self._controls,
            self._indicators,
            id=self.id,
        )
        element.classes.add("invent-webcam")
        element.classes.add("webcam-container")

        # Initialize the webcam stream
        self._setup_webcam_stream()

        return element
