"""
Utility and compatibility functions.
"""

import inspect
import sys
from pyscript.web import div
from .app import App


#: A flag to show if MicroPython is the current Python interpreter.
is_micropython = "micropython" in sys.version.lower()


def show_page(page_name):
    """
    Show the page with the specified name. Hide the current page if there is
    one.
    """
    App.app().show_page(page_name)


def getmembers_static(cls):
    """
    Cross-interpreter implementation of inspect.getmembers_static.
    """
    if is_micropython:  # pragma: no cover
        return [
            (name, getattr(cls, name)) for name, _ in inspect.getmembers(cls)
        ]
    return inspect.getmembers_static(cls)


def iscoroutinefunction(obj):
    """
    Cross-interpreter implementation of inspect.iscoroutinefunction.
    """
    if is_micropython:  # pragma: no cover
        # MicroPython seems to treat coroutines as generators :)
        # But the object may be a closure containing a generator.
        if "<closure <generator>" in repr(obj):
            # As far as I can tell, there's no way to check if a closure
            # contains a generator in MicroPython except by checking the
            # string representation.
            return True
        # And if not, just check it's a generator function.
        return inspect.isgeneratorfunction(obj)

    return inspect.iscoroutinefunction(obj)


def capitalize(s):
    """
    Cross-interpreter implementation of str.capitalize.
    """
    return s[0].upper() + s[1:].lower()


def sanitize(raw):
    """
    Returns an HTML safe version of the raw input string.
    """
    temp = div()
    temp.innerText = raw
    return temp.innerHTML


def from_markdown(raw_markdown):
    """
    Convert markdown to sanitized HTML.
    """
    result = raw_markdown
    from . import marked, purify  # To avoid circular imports.

    if marked:
        result = purify.default().sanitize(marked.parse(raw_markdown))
    return result
