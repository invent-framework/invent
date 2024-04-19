"""MicroPython/pyodide compatability layer."""

import inspect
import sys
import types


#: A flag to show if MicroPython is the current Python interpreter.
is_micropython = "MicroPython" in sys.version


def getmembers_static(cls):
    """Cross-interpreter implementation of inspect.getmembers_static."""

    if is_micropython:  # pragma: no cover
        return [
            (name, getattr(cls, name)) for name, _ in inspect.getmembers(cls)
        ]

    return inspect.getmembers_static(cls)


def iscoroutinefunction(obj):
    """Cross-interpreter implementation of inspect.iscoroutinefunction."""

    if is_micropython:  # pragma: no cover
        # MicroPython seems to treat coroutines as generators :)
        return type(obj) is types.GeneratorType

    return inspect.iscoroutinefunction(obj)
