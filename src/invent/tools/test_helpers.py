"""Small helpers shared by interactive donkey test pages."""

import invent

_PASS = "color:green;font-family:monospace;margin:4px 0"
_FAIL = "color:red;font-family:monospace;margin:4px 0"
_WAIT = "color:#555;font-family:monospace;margin:4px 0"


def pass_html(text):
    return f'<p style="{_PASS}">[PASS] {text}</p>'


def fail_html(text):
    return f'<p style="{_FAIL}">[FAIL] {text}</p>'


def wait_html(text):
    return f'<p style="{_WAIT}">[ ] {text}</p>'


class StatusProxy:
    """Proxy a label while publishing status updates."""

    def __init__(self, status_label, channel):
        self._label = status_label
        self._channel = channel

    @property
    def text(self):
        return self._label.text

    @text.setter
    def text(self, value):
        self._label.text = value
        invent.publish(
            invent.Message("status", status=value),
            to_channel=self._channel,
        )
