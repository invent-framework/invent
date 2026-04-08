import base64

import umock

from invent.ui.widgets.webcam import Webcam


def test_webcam_capture_store_filters_and_latest():
    w = Webcam()

    photo_capture = {"id": "photo-1", "type": "photo"}
    video_capture = {"id": "video-1", "type": "video"}

    w._store_capture(photo_capture)
    w._store_capture(video_capture)

    assert w.captures() == [photo_capture, video_capture]
    assert w.captures(media_type="photo") == [photo_capture]
    assert w.captures(media_type="video") == [video_capture]
    assert w.latest_capture() == video_capture
    assert w.latest_capture(media_type="photo") == photo_capture


def test_webcam_capture_store_respects_max_captures():
    w = Webcam(max_captures=2)
    w.publish = lambda *args, **kwargs: None

    w._store_capture({"id": "photo-1", "type": "photo"})
    w._store_capture({"id": "photo-2", "type": "photo"})
    w._store_capture({"id": "photo-3", "type": "photo"})

    captures = w.captures(media_type="photo")
    assert len(captures) == 2
    assert captures[0]["id"] == "photo-2"
    assert captures[1]["id"] == "photo-3"


def test_webcam_remove_and_clear_captures():
    w = Webcam()
    w.publish = lambda *args, **kwargs: None

    first = {"id": "photo-1", "type": "photo"}
    second = {"id": "video-1", "type": "video"}
    w._store_capture(first)
    w._store_capture(second)

    removed = w.remove_capture("photo-1")
    assert removed == first
    assert w.find_capture("photo-1") is None

    cleared = w.clear_captures(media_type="video")
    assert cleared == [second]
    assert w.captures() == []


def test_webcam_photo_bytes_decodes_data_url():
    w = Webcam()

    raw = b"hello"
    encoded = base64.b64encode(raw).decode("ascii")
    capture = {
        "id": "photo-1",
        "type": "photo",
        "data_url": f"data:image/jpeg;base64,{encoded}",
    }

    assert w.photo_bytes(capture=capture) == raw


def test_webcam_photo_output_preview_updates_inline_image():
    w = Webcam()
    w.photo_output = "preview"

    preview_classes = umock.Mock()
    preview_classes.remove = umock.Mock()
    preview = umock.Mock()
    preview.classes = preview_classes
    w._capture_preview = preview

    raw = b"hello"
    encoded = base64.b64encode(raw).decode("ascii")
    capture = w._store_capture(
        {
            "id": "photo-1",
            "type": "photo",
            "data_url": f"data:image/jpeg;base64,{encoded}",
        }
    )

    assert preview.src == capture["data_url"]
    preview.classes.remove.assert_called_once_with("hidden")
