"""
A webcam widget for the Invent framework.

Enables photo capture and video recording with automatic downloads.
Supports live video preview from the user's webcam.
Supports an opencv_mode for running OpenCV processing on captured images,
with side-by-side layout and no automatic downloads.

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
    IntegerProperty,
)
from pyscript.web import div, video, button, canvas, img, p
from pyscript.ffi import create_proxy

try:
    import cv2 as _cv2
except ImportError:
    _cv2 = None

try:
    import numpy as _np
except ImportError:
    _np = None

try:
    from PIL import Image as _PILImage
    from PIL import ImageFilter as _PILImageFilter
except ImportError:
    _PILImage = None
    _PILImageFilter = None

_OPENCV_AVAILABLE = _cv2 is not None
_NUMPY_AVAILABLE = _np is not None
_PIL_AVAILABLE = _PILImage is not None


class _Cv2Compat:
    """Minimal cv2-compatible surface for browser runtimes without cv2."""

    COLOR_RGB2BGR = 1
    COLOR_RGB2GRAY = 2

    @staticmethod
    def cvtColor(array, code):
        if _np is None:
            raise RuntimeError("numpy is required for cv2 compatibility mode")

        if code == _Cv2Compat.COLOR_RGB2BGR:
            return array[..., ::-1].copy()

        if code == _Cv2Compat.COLOR_RGB2GRAY:
            if array.ndim != 3 or array.shape[2] < 3:
                raise ValueError("Expected RGB image with shape (H, W, 3)")
            grey = _np.dot(array[..., :3], _np.array([0.299, 0.587, 0.114]))
            return grey.astype(_np.uint8)

        raise ValueError(f"Unsupported color conversion code: {code}")

    @staticmethod
    def Canny(grey, threshold1, threshold2):
        del threshold1, threshold2
        if _PILImage is None or _PILImageFilter is None or _np is None:
            raise RuntimeError(
                "Pillow and numpy are required for edge detection"
            )
        pil = _PILImage.fromarray(grey.astype(_np.uint8), mode="L")
        edges = pil.filter(_PILImageFilter.FIND_EDGES)
        return _np.array(edges, dtype=_np.uint8)


try:
    # CodeEditor is a peer Invent widget – import lazily so webcam.py can be
    # imported even in environments where the editor widget isn't present.
    from invent.ui import CodeEditor as _CodeEditor

    _CODE_EDITOR_AVAILABLE = True
except ImportError:
    _CodeEditor = None
    _CODE_EDITOR_AVAILABLE = False

import base64
import io


class Webcam(Widget):
    """
    A webcam widget with photo capture, video recording, and optional
    OpenCV processing capabilities.

    opencv_mode
    -----------
    When True the widget renders a self-contained OpenCV playground:
      • Captured image appears **side-by-side** with the live feed.
      • Automatic file downloads are suppressed regardless of photo_output.
      • A code editor pre-filled with a starter snippet and a "Run OpenCV"
        button are rendered below the video row.
      • The processed result is shown next to the raw capture.

    The code snippet executed by "Run OpenCV" has the following names bound
    in its namespace:

        capture       – the raw capture dict stored by the widget
        image         – PIL Image (RGB) of the captured photo
        array_of_rgb  – numpy uint8 array, shape (H, W, 3), RGB order
        array_of_bgr  – numpy uint8 array, shape (H, W, 3), BGR order
        grey          – numpy uint8 array, shape (H, W),    greyscale
        cv2           – the cv2 module
        np            – the numpy module
        PILImage      – PIL.Image module

    The snippet should assign one of the following names to be shown as the
    result image:

        result_image | processed_image | output_image | result

    Any of those may be a numpy ndarray or a PIL Image; both are handled.
    If none is assigned the original captured image is shown unchanged.
    """

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    photo_output = ChoiceProperty(
        _("How captured photos are handled: downloaded, previewed, or both."),
        default_value="download",
        choices=["download", "preview", "both"],
        group="behavior",
    )

    max_captures = IntegerProperty(
        _(
            "The maximum number of captured images and recordings to keep in memory."
        ),
        default_value=10,
        minimum=0,
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

    opencv_mode = BooleanProperty(
        _(
            "When True, enables the built-in OpenCV processing playground. "
            "The capture preview is shown side-by-side with the live feed, "
            "downloads are suppressed, and a code editor + run button are "
            "rendered inside the widget."
        ),
        default_value=False,
        group="behavior",
    )

    opencv_default_code = _(
        "The default OpenCV snippet shown in the code editor."
    )

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------

    photo_captured = Event(
        _("Sent when a photo is captured."),
        webcam=_("The Webcam widget that captured the photo."),
        capture=_("The captured photo metadata."),
    )

    video_recorded = Event(
        _("Sent when a video is recorded."),
        webcam=_("The Webcam widget that recorded the video."),
    )

    # ------------------------------------------------------------------
    # Default OpenCV starter snippet
    # ------------------------------------------------------------------

    _DEFAULT_OPENCV_CODE = (
        "# Names available: capture, image, array_of_rgb, array_of_bgr,\n"
        "# grey, cv2, np, PILImage\n"
        "#\n"
        "# Assign result_image (PIL Image or numpy array) to show output.\n"
        "\n"
        "grey = cv2.cvtColor(array_of_rgb, cv2.COLOR_RGB2GRAY)\n"
        "edges = cv2.Canny(grey, 80, 160)\n"
        "result_image = PILImage.fromarray(edges)\n"
    )

    # ------------------------------------------------------------------

    @classmethod
    def icon(cls):
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em"'
            ' viewBox="0 0 256 256"><circle cx="128" cy="128" r="32"'
            ' fill="currentColor" opacity="0.2"/><path fill="currentColor"'
            ' d="M208 56H48a16 16 0 0 0-16 16v112a16 16 0 0 0 16 16h160a16'
            " 16 0 0 0 16-16V72a16 16 0 0 0-16-16m0 128H48V72h160zM128"
            " 96a32 32 0 1 0 32 32a32 32 0 0 0-32-32m0 48a16 16 0 1 1"
            ' 16-16a16 16 0 0 1-16 16"/></svg>'
        )

    @staticmethod
    def _coerce_bool(value):
        """Best-effort bool coercion for initial constructor kwargs."""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in {
                "1",
                "true",
                "yes",
                "on",
            }
        return bool(value)

    def __init__(self, *args, **kwargs):
        # Invent may render before all properties are fully applied. Capture
        # the requested mode from kwargs so initial layout is correct.
        self._initial_opencv_mode = self._coerce_bool(
            kwargs.get("opencv_mode", False)
        )
        self._captures = []
        self._capture_counter = 0
        # opencv_mode internal state
        self._opencv_code = self._DEFAULT_OPENCV_CODE
        self._opencv_result_img_elem = None  # the <img> DOM wrapper for result
        self._opencv_status_elem = None  # <p> for status text
        super().__init__(*args, **kwargs)

    # ------------------------------------------------------------------
    # Download / preview helpers
    # ------------------------------------------------------------------

    def _capture_output_enabled(self):
        """True when the preview img should be shown after capture."""
        return self.photo_output in ("preview", "both")

    def _capture_download_enabled(self):
        """
        True when the file should be auto-downloaded after capture.
        Downloads are always suppressed in opencv_mode.
        """
        use_opencv_layout = self.opencv_mode or self._initial_opencv_mode
        if use_opencv_layout:
            return False
        return self.photo_output in ("download", "both")

    # ------------------------------------------------------------------
    # Capture management
    # ------------------------------------------------------------------

    def _capture_id(self, media_type):
        self._capture_counter += 1
        return f"{media_type}-{self._timestamp()}-{self._capture_counter}"

    def _store_capture(self, capture):
        capture = dict(capture)
        capture.setdefault("type", "photo")
        capture.setdefault("timestamp", self._timestamp())
        capture.setdefault("id", self._capture_id(capture["type"]))
        self._captures.append(capture)

        if self.max_captures and self.max_captures > 0:
            overflow = len(self._captures) - self.max_captures
            if overflow > 0:
                self._captures = self._captures[overflow:]

        if capture["type"] == "photo" and self._capture_output_enabled():
            self._show_capture_preview(capture)

        # In opencv_mode, always show the raw capture in the side panel.
        if self.opencv_mode and capture["type"] == "photo":
            self._show_capture_preview(capture)

        return capture

    def captures(self, media_type=None):
        if media_type is None:
            return list(self._captures)
        return [c for c in self._captures if c.get("type") == media_type]

    def latest_capture(self, media_type=None):
        captures = self.captures(media_type=media_type)
        return captures[-1] if captures else None

    def find_capture(self, capture_id):
        for capture in self._captures:
            if capture.get("id") == capture_id:
                return capture
        return None

    def remove_capture(self, capture_id):
        for index, capture in enumerate(self._captures):
            if capture.get("id") == capture_id:
                removed = self._captures.pop(index)
                self._refresh_capture_preview()
                return removed
        return None

    def clear_captures(self, media_type=None):
        if media_type is None:
            removed = list(self._captures)
            self._captures = []
            self._refresh_capture_preview()
            return removed

        kept, removed = [], []
        for capture in self._captures:
            if capture.get("type") == media_type:
                removed.append(capture)
            else:
                kept.append(capture)
        self._captures = kept
        self._refresh_capture_preview()
        return removed

    def photo_bytes(self, capture=None):
        """Return raw JPEG bytes for *capture* (defaults to latest photo)."""
        capture = capture or self.latest_capture(media_type="photo")
        if not capture:
            return None
        if capture.get("photo_bytes") is not None:
            return capture["photo_bytes"]
        data_url = capture.get("data_url")
        if not data_url or "," not in data_url:
            return None
        return base64.b64decode(data_url.split(",", 1)[1])

    # ------------------------------------------------------------------
    # Preview helpers
    # ------------------------------------------------------------------

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
        if not self._capture_output_enabled() and not self.opencv_mode:
            self._hide_capture_preview()
            return
        latest_photo = self.latest_capture(media_type="photo")
        if latest_photo:
            self._show_capture_preview(latest_photo)
        else:
            self._hide_capture_preview()

    # ------------------------------------------------------------------
    # Programmatic trigger
    # ------------------------------------------------------------------

    def trigger(self):
        """Trigger the current action (capture photo or start/stop recording)."""
        if hasattr(self, "_shutter_btn"):
            self._shutter_btn.click()

    # ------------------------------------------------------------------
    # Mode switching
    # ------------------------------------------------------------------

    def set_mode(self, mode):
        """Set the active webcam mode when switching is enabled."""
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
        if self.mode == "both":
            return getattr(self, "_active_mode", "photo")
        return self.mode

    # ------------------------------------------------------------------
    # Photo capture
    # ------------------------------------------------------------------

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

            if self._capture_download_enabled():
                self._download_canvas_as_image(capture)

            if not self._capture_output_enabled() and not self.opencv_mode:
                self._hide_capture_preview()

            self.publish(self.photo_captured, webcam=self, capture=capture)

    # ------------------------------------------------------------------
    # Status helpers
    # ------------------------------------------------------------------

    def _set_status(self, text):
        if not hasattr(self, "_status_elem"):
            return
        self._status_elem._dom_element.textContent = text

    def _timestamp(self):
        return int(time.time() * 1000)

    # ------------------------------------------------------------------
    # Video recording
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Property-change callbacks
    # ------------------------------------------------------------------

    def on_mode_changed(self):
        if not hasattr(self, "_controls"):
            return

        self._active_mode = "photo" if self.mode == "both" else self.mode

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
            self._mode_indicator._dom_element.textContent = self._mode_label()

        if hasattr(self, "_indicators"):
            if self.show_mode_indicator:
                self._indicators.classes.remove("hidden")
            else:
                self._indicators.classes.add("hidden")

    def on_photo_output_changed(self):
        if not hasattr(self, "_capture_preview"):
            return
        self._refresh_capture_preview()

    def on_max_captures_changed(self):
        if self.max_captures and self.max_captures > 0:
            overflow = len(self._captures) - self.max_captures
            if overflow > 0:
                self._captures = self._captures[overflow:]
        self._refresh_capture_preview()

    # ------------------------------------------------------------------
    # Mode-button UI helpers
    # ------------------------------------------------------------------

    def _mode_label(self):
        if self._current_mode() == "video":
            return "Video Mode"
        return "Photo Mode"

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

    # ------------------------------------------------------------------
    # Download helper
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Shutter click
    # ------------------------------------------------------------------

    def _on_shutter_click(self, event):
        if self._current_mode() == "photo":
            self.capture_photo()
        else:
            if self._recording:
                self.stop_recording()
            else:
                self.start_recording()

    # ------------------------------------------------------------------
    # Webcam stream setup
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Mode-button builder
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # OpenCV helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _pil_to_data_url(pil_image):
        """Convert a PIL Image to a PNG data URL string."""
        buf = io.BytesIO()
        pil_image.save(buf, format="PNG")
        encoded = base64.b64encode(buf.getvalue()).decode("ascii")
        return f"data:image/png;base64,{encoded}"

    def _set_opencv_status(self, text):
        """Update the status <p> element inside the OpenCV panel."""
        if self._opencv_status_elem is not None:
            self._opencv_status_elem._dom_element.textContent = text

    def _set_opencv_result_image(self, data_url):
        """Set the src of the OpenCV result <img> element."""
        if self._opencv_result_img_elem is not None:
            self._opencv_result_img_elem.src = data_url
            self._opencv_result_img_elem.classes.remove("hidden")

    def run_opencv(self, event=None):
        """
        Execute the OpenCV snippet from the embedded code editor against
        the most recent captured photo.

        This method is also callable from outside the widget, e.g. from
        main.py, if you keep a reference to the Webcam instance:

            my_webcam.run_opencv()
        """
        self._set_opencv_status("Running OpenCV...")
        self._set_status("Running OpenCV...")

        cv2_module = _cv2
        compatibility_mode = False
        if cv2_module is None:
            if not (_NUMPY_AVAILABLE and _PIL_AVAILABLE):
                self._set_opencv_status(
                    "OpenCV unavailable. Install numpy + Pillow to run compatibility mode."
                )
                self._set_status("OpenCV unavailable")
                return
            cv2_module = _Cv2Compat
            compatibility_mode = True

        if not (_NUMPY_AVAILABLE and _PIL_AVAILABLE):
            self._set_opencv_status(
                "Image processing requires numpy and Pillow in this runtime."
            )
            self._set_status("Image processing unavailable")
            return

        capture = self.latest_capture(media_type="photo")
        if not capture:
            self._set_opencv_status(
                "No photo captured yet. Press 'Take' first."
            )
            self._set_status("No photo to process")
            return

        raw_bytes = self.photo_bytes(capture=capture)
        if raw_bytes is None:
            self._set_opencv_status("Could not decode the latest capture.")
            self._set_status("Capture decode failed")
            return

        # Retrieve the current snippet from the embedded CodeEditor, falling
        # back to the stored string if the editor widget isn't available.
        code_to_run = self._opencv_code
        if hasattr(self, "_opencv_code_editor"):
            try:
                code_to_run = self._opencv_code_editor.code
            except Exception:
                pass

        try:
            source_image = _PILImage.open(io.BytesIO(raw_bytes)).convert("RGB")
            array_of_rgb = _np.array(source_image)
            array_of_bgr = cv2_module.cvtColor(
                array_of_rgb, cv2_module.COLOR_RGB2BGR
            )
            grey = cv2_module.cvtColor(array_of_rgb, cv2_module.COLOR_RGB2GRAY)

            namespace = {
                "capture": capture,
                "image": source_image,
                "array_of_rgb": array_of_rgb,
                "array_of_bgr": array_of_bgr,
                "grey": grey,
                "cv2": cv2_module,
                "np": _np,
                "PILImage": _PILImage,
            }

            exec(code_to_run, namespace, namespace)  # noqa: S102

            result = (
                namespace.get("result_image")
                or namespace.get("processed_image")
                or namespace.get("output_image")
                or namespace.get("result")
            )

            if isinstance(result, _np.ndarray):
                # Greyscale (2-D) → needs conversion for PIL
                if result.ndim == 2:
                    result = _PILImage.fromarray(result)
                else:
                    result = _PILImage.fromarray(result)

            if result is None:
                result = source_image  # show original if snippet set nothing

            if isinstance(result, _PILImage.Image):
                data_url = self._pil_to_data_url(result)
                self._set_opencv_result_image(data_url)
                self._set_opencv_status(
                    f"OK — {array_of_rgb.shape[1]}×{array_of_rgb.shape[0]} px  "
                    f"| capture {capture.get('id', '?')}"
                )
                if compatibility_mode:
                    self._set_opencv_status(
                        "OK (compat mode: numpy + Pillow) — "
                        f"{array_of_rgb.shape[1]}×{array_of_rgb.shape[0]} px  "
                        f"| capture {capture.get('id', '?')}"
                    )
                self._set_status("OpenCV processing complete")
            else:
                self._set_opencv_status(
                    "Snippet did not produce a displayable image."
                )
                self._set_status("OpenCV produced no displayable image")

        except Exception as exc:
            self._set_opencv_status(f"Error: {exc}")
            self._set_status("OpenCV error")

    # ------------------------------------------------------------------
    # OpenCV panel builder
    # ------------------------------------------------------------------

    def _build_opencv_panel(self):
        """
        Build and return the OpenCV editor + result panel that sits below
        the video row when opencv_mode=True.

        Also populates:
            self._opencv_code_editor   – CodeEditor widget (if available)
            self._opencv_result_img_elem – img element for the result
            self._opencv_status_elem   – p element for status text
        """
        # ---- result image (shown in the side panel, updated after run) ----
        # (The raw capture preview is shown in _capture_preview which lives
        #  inside the video row.  The *processed* result goes here.)
        result_img = img()
        result_img.id = f"{self.id}-opencv-result"
        result_img.classes.add("invent-webcam-opencv-result-img")
        result_img.classes.add("hidden")
        self._opencv_result_img_elem = result_img

        result_label_el = p("Processed result:")
        result_label_el.classes.add("invent-webcam-opencv-label")

        result_container = div(result_label_el, result_img)
        result_container.classes.add("invent-webcam-opencv-result-panel")

        # ---- status line ----
        status_p = p("Run OpenCV to see results.")
        status_p.classes.add("invent-webcam-opencv-status")
        self._opencv_status_elem = status_p

        # ---- code editor ----
        if _CODE_EDITOR_AVAILABLE:
            try:
                editor = _CodeEditor(
                    language="python",
                    min_height="180px",
                    code=self._opencv_code,
                )
                self._opencv_code_editor = editor
                editor_element = editor
            except Exception as e:
                print(f"Could not create CodeEditor: {e}")
                editor_element = p(
                    "CodeEditor unavailable – edit self._opencv_code directly."
                )
                self._opencv_code_editor = None
        else:
            editor_element = p(
                "CodeEditor widget not available – edit self._opencv_code directly."
            )
            self._opencv_code_editor = None

        # ---- run button ----
        run_btn = button("Run OpenCV")
        run_btn.id = f"{self.id}-opencv-run-btn"
        run_btn.classes.add("invent-webcam-opencv-run-btn")
        run_btn._dom_element.addEventListener(
            "click", create_proxy(self.run_opencv)
        )

        # ---- assemble panel ----
        opencv_panel = div(
            editor_element,
            run_btn,
            status_p,
            result_container,
        )
        opencv_panel.classes.add("invent-webcam-opencv-panel")

        return opencv_panel

    # ------------------------------------------------------------------
    # render()
    # ------------------------------------------------------------------

    def render(self):
        """
        Render the webcam widget.

        Normal mode  → identical layout to the original widget.
        opencv_mode  → video + raw-capture side-by-side in a flex row,
                       followed by a code-editor + result panel below.
        """
        # ---- hidden canvas for photo capture ----
        self._canvas = canvas()
        self._canvas.classes.add("invent-webcam-canvas-hidden")

        # ---- live video element ----
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

        # ---- shutter button ----
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

        # ---- status indicators ----
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

        # ---- capture preview image ----
        self._capture_preview = img()
        self._capture_preview.id = f"{self.id}-capture-preview"
        self._capture_preview.classes.add("invent-webcam-capture-preview")
        self._capture_preview.classes.add("capture-preview")
        self._capture_preview.classes.add("hidden")

        # ------------------------------------------------------------------
        # Layout differs between normal and opencv_mode
        # ------------------------------------------------------------------

        if self.opencv_mode:
            # ----------------------------------------------------------
            # opencv_mode layout
            # ----------------------------------------------------------
            # Row 1: [live feed] [raw capture preview]  ← flex row
            # Row 2: [opencv panel: editor + run btn + result]

            # Label the two panels
            live_label = p("Live feed")
            live_label.classes.add("invent-webcam-opencv-label")

            capture_label = p("Captured image")
            capture_label.classes.add("invent-webcam-opencv-label")

            live_col = div(live_label, video_container, self._controls)
            live_col.classes.add("invent-webcam-opencv-col")

            capture_preview_box = div(self._capture_preview)
            capture_preview_box.classes.add("invent-webcam-box")
            capture_preview_box.classes.add("webcam-box")
            capture_preview_box.classes.add("invent-webcam-opencv-preview-box")

            capture_col = div(
                capture_label,
                capture_preview_box,
                self._indicators,
            )
            capture_col.classes.add("invent-webcam-opencv-col")

            video_row = div(live_col, capture_col)
            video_row.classes.add("invent-webcam-opencv-video-row")

            opencv_panel = self._build_opencv_panel()

            element = div(
                self._canvas,
                video_row,
                opencv_panel,
                id=self.id,
            )

        else:
            # ----------------------------------------------------------
            # Normal (original) layout
            # ----------------------------------------------------------
            element = div(
                self._canvas,
                video_container,
                self._controls,
                self._indicators,
                self._capture_preview,
                id=self.id,
            )

        element.classes.add("invent-webcam")
        element.classes.add("webcam-container")

        # Kick off the camera stream
        self._setup_webcam_stream()

        return element
