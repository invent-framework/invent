"""
Utility functions.
"""


import inspect
import sys
from pyscript import window


#: A flag to show if MicroPython is the current Python interpreter.
is_micropython = "MicroPython" in sys.version


def play_sound(url):
    sound = window.Audio.new(str(url))
    sound.play()


def show_page(page_name):
    from invent.ui import App
    App.app().show_page(page_name)


def getmembers_static(cls):
    """Cross-interpreter implementation of inspect.getmembers_static."""

    if is_micropython:  # pragma: no cover
        return [
            (name, getattr(cls, name))

            for name, _ in inspect.getmembers(cls)
        ]

    return inspect.getmembers_static(cls)


def iscoroutinefunction(obj):
    """Cross-interpreter implementation of inspect.iscoroutinefunction."""

    if is_micropython:
        # TODO: No async handlers in MicroPython just yet...
        return False

    return inspect.iscoroutinefunction(obj)
