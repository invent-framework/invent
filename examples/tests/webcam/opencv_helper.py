import base64
import cv2
import numpy as np


def _decode_data_url(data_url):
    if not data_url or "," not in data_url:
        raise ValueError("Expected an image data URL")
    payload = data_url.split(",", 1)[1]
    binary = base64.b64decode(payload)
    buf = np.frombuffer(binary, dtype=np.uint8)
    image = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Could not decode input image")
    return image


def _encode_png_data_url(image):
    ok, encoded = cv2.imencode(".png", image)
    if not ok:
        raise ValueError("Could not encode processed image")
    payload = base64.b64encode(encoded.tobytes()).decode("ascii")
    return "data:image/png;base64," + payload


def process(user_code, data_url):
    image_bgr = _decode_data_url(data_url)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    grey = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    namespace = {
        "cv2": cv2,
        "np": np,
        "image_bgr": image_bgr,
        "image_rgb": image_rgb,
        "grey": grey,
        "result_image": None,
        "result": None,
    }

    exec(user_code, namespace, namespace)

    result = namespace.get("result_image")
    if result is None:
        result = namespace.get("result")
    if result is None:
        result = image_bgr

    if not isinstance(result, np.ndarray):
        raise ValueError(
            "Your code must assign a numpy ndarray to result_image or result"
        )

    if result.ndim == 2:
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
    elif result.ndim == 3 and result.shape[2] == 3:
        pass
    else:
        raise ValueError("Unsupported result_image shape")

    return {
        "ok": True,
        "kind": "user_code",
        "data_url": _encode_png_data_url(result),
    }
