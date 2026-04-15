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
from pyscript.web import div, video, button, canvas, img
from pyscript.ffi import create_proxy


class Webcam(Widget):
    """
    A webcam widget with photo capture and video recording.
    """

    photo_output = ChoiceProperty(
        _("How captured photos are handled: downloaded, previewed, or both."),
        default_value="download",
        choices=["download", "preview", "both"],
        group="behavior",
    )

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

    preview_layout = ChoiceProperty(
        _("Layout of the capture preview relative to the live video feed."),
        default_value="stacked",
        choices=["stacked", "side-by-side"],
        group="style",
    )

    photo_captured = Event(
        _("Sent when a photo is captured."),
        webcam=_("The Webcam widget that captured the photo."),
        capture=_("The captured photo metadata."),
    )

    video_recorded = Event(
        _("Sent when a video is recorded."),
        webcam=_("The Webcam widget that recorded the video."),
    )

    def __init__(self, *args, **kwargs):
        self._captures = []
        self._capture_counter = 0
        super().__init__(*args, **kwargs)

    # Capture management
    def _store_capture(self, capture):
        capture = dict(capture)
        capture.setdefault("type", "photo")
        capture.setdefault("timestamp", self._timestamp())
        self._capture_counter += 1
        capture.setdefault(
            "id",
            f"{capture['type']}-{self._timestamp()}-{self._capture_counter}",
        )
        self._captures.append(capture)

        preview_enabled = self.photo_output in ("preview", "both")

        if capture["type"] == "photo" and preview_enabled:
            self._show_capture_preview(capture)

        return capture

    def captures(self, media_type=None):
        if media_type is None:
            return list(self._captures)
        return [c for c in self._captures if c.get("type") == media_type]

    def latest_capture(self, media_type=None):
        captures = self.captures(media_type=media_type)
        return captures[-1] if captures else None

    # Preview helpers
    def _show_capture_preview(self, capture):
        if not hasattr(self, "_capture_preview"):
            return
        data_url = capture.get("data_url")
        if not data_url:
            return
        self._capture_preview.src = data_url
        self._capture_preview.classes.remove("hidden")

    def _hide_capture_preview(self):
        if hasattr(self, "_capture_preview"):
            self._capture_preview.classes.add("hidden")

    def _refresh_capture_preview(self):
        preview_enabled = self.photo_output in ("preview", "both")
        if not preview_enabled:
            self._hide_capture_preview()
            return
        latest_photo = self.latest_capture(media_type="photo")
        if latest_photo:
            self._show_capture_preview(latest_photo)
        else:
            self._hide_capture_preview()

    def show_image(self, data_url):
        """Display any image in the preview panel, replacing the current content."""
        if not hasattr(self, "_capture_preview"):
            return
        self._capture_preview.src = data_url
        self._capture_preview.classes.remove("hidden")

    # Mode switching
    def set_mode(self, mode):
        """Set the active webcam mode when switching is enabled."""
        if self.mode != "both":
            return
        if mode in ["photo", "video"]:
            self._active_mode = mode
            mode_label = (
                "Video Mode"
                if self._current_mode() == "video"
                else "Photo Mode"
            )
            if hasattr(self, "_mode_buttons"):
                self._update_mode_buttons()
            if hasattr(self, "_mode_indicator"):
                self._mode_indicator._dom_element.textContent = mode_label
            if hasattr(self, "_shutter_btn"):
                self._set_shutter_text()

    def _current_mode(self):
        if self.mode == "both":
            return getattr(self, "_active_mode", "photo")
        return self.mode

    # Photo capture
    def capture_photo(self):
        """Capture a photo from the current video stream."""
        if hasattr(self, "_canvas") and hasattr(self, "_video_elem"):
            video_el = self._video_elem._dom_element
            canvas_el = self._canvas._dom_element

            width = video_el.videoWidth or 1280
            height = video_el.videoHeight or 720
            canvas_el.width = width
            canvas_el.height = height

            ctx = canvas_el.getContext("2d")
            ctx.drawImage(video_el, 0, 0, width, height)

            capture = self._store_capture(
                {
                    "type": "photo",
                    "timestamp": self._timestamp(),
                    "data_url": self._canvas._dom_element.toDataURL(
                        "image/jpeg"
                    ),
                }
            )

            download_enabled = self.photo_output in (
                "download",
                "both",
            )
            preview_enabled = self.photo_output in ("preview", "both")

            if download_enabled:
                self._download_canvas_as_image(capture)

            if not preview_enabled:
                self._hide_capture_preview()

            self.publish(self.photo_captured, webcam=self, capture=capture)

    # Status helpers
    def _set_status(self, text):
        if not hasattr(self, "_status_elem"):
            return
        self._status_elem._dom_element.textContent = text

    def _timestamp(self):
        return int(time.time() * 1000)

    # Video recording
    def start_recording(self):
        if hasattr(self, "_recorder"):
            if not self._recording and self._recorder.state == "inactive":
                self._recorded_chunks = []
                self._recording = True
                self._recorder.start()
                self._shutter_btn.classes.add("recording")
                self._set_shutter_text()
                self._set_status("Recording...")

    def stop_recording(self):
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

    # Callbacks
    def on_mode_changed(self):
        if not hasattr(self, "_controls"):
            return

        self._active_mode = "photo" if self.mode == "both" else self.mode
        mode_label = (
            "Video Mode" if self._current_mode() == "video" else "Photo Mode"
        )

        controls_el = self._controls._dom_element
        if (
            hasattr(self, "_modes_container")
            and self._modes_container is not None
        ):
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

        self._set_shutter_text()
        if hasattr(self, "_mode_indicator"):
            self._mode_indicator._dom_element.textContent = mode_label

        if hasattr(self, "_indicators"):
            if self.show_mode_indicator:
                self._indicators.classes.remove("hidden")
            else:
                self._indicators.classes.add("hidden")

    def on_photo_output_changed(self):
        if not hasattr(self, "_capture_preview"):
            return
        self._refresh_capture_preview()

    def on_preview_layout_changed(self):
        if not hasattr(self, "element"):
            return
        if self.preview_layout == "side-by-side":
            self.element.classes.add("invent-webcam--side-by-side")
        else:
            self.element.classes.remove("invent-webcam--side-by-side")

    # UI helpers
    def _update_mode_buttons(self):
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
        if not hasattr(self, "_shutter_btn"):
            return
        is_recording = getattr(self, "_recording", False)
        if self._current_mode() == "video":
            text = "Stop" if is_recording else "Record"
        else:
            text = "Take"
        self._shutter_btn._dom_element.textContent = text

    # Download helper
    def _download_canvas_as_image(self, capture=None):
        try:
            from pyscript import window

            capture = capture or self.latest_capture(media_type="photo")
            if capture and capture.get("data_url"):
                data_url = capture["data_url"]
            else:
                data_url = self._canvas._dom_element.toDataURL("image/jpeg")

            link = window.document.createElement("a")
            link.href = data_url
            link.download = f"photo-{self._timestamp()}.jpg"
            link.click()
        except Exception as e:
            print(f"Error downloading photo: {e}")

    def _on_shutter_click(self, event):
        if self._current_mode() == "photo":
            self.capture_photo()
        else:
            if self._recording:
                self.stop_recording()
            else:
                self.start_recording()

    # Webcam stream
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

            import asyncio

            asyncio.create_task(get_stream())

        except Exception as e:
            print(f"Error setting up webcam: {e}")

    def _setup_recorder(self, stream):
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

    # Determine Camera Mode (video or photo)
    def _build_mode_buttons(self):
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
        Render the webcam widget.
        """
        # hidden canvas for photo capture
        self._canvas = canvas()
        self._canvas.classes.add("invent-webcam-canvas-hidden")

        # live video element
        self._video_elem = video()
        self._video_elem.id = f"{self.id}-video"
        self._video_elem.autoplay = True
        self._video_elem.muted = True
        self._video_elem.classes.add("invent-webcam-video")

        def on_video_ready(event):
            video_el = self._video_elem._dom_element
            canvas_el = self._canvas._dom_element
            canvas_el.width = video_el.videoWidth or 1280
            canvas_el.height = video_el.videoHeight or 720

        self._video_elem._dom_element.addEventListener(
            "loadedmetadata", create_proxy(on_video_ready)
        )

        video_container = div(self._video_elem)
        video_container.classes.add("invent-webcam-box")
        video_container.classes.add("webcam-box")

        # shutter button
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

        self._controls = div(shutter_container)
        self._controls.classes.add("invent-webcam-actions")
        self._controls.classes.add("actions")
        self._shutter_container = shutter_container

        # status indicators
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

        # capture preview image
        self._capture_preview = img()
        self._capture_preview.id = f"{self.id}-capture-preview"
        self._capture_preview.classes.add("invent-webcam-capture-preview")
        self._capture_preview.classes.add("capture-preview")
        self._capture_preview.classes.add("hidden")

        # Wrap video and preview in a media row
        self._preview_col = div(self._capture_preview)
        self._preview_col.classes.add("invent-webcam-preview-col")

        self._media_row = div(video_container, self._preview_col)
        self._media_row.classes.add("invent-webcam-media-row")

        element = div(
            self._canvas,
            self._media_row,
            self._controls,
            self._indicators,
            id=self.id,
        )

        element.classes.add("invent-webcam")
        element.classes.add("webcam-container")

        # Start the camera stream!
        self._setup_webcam_stream()

        return element
        