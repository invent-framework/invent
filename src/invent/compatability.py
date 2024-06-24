"""MicroPython/pyodide compatability layer."""

import asyncio
import inspect
import sys


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
        return inspect.isgeneratorfunction(obj)

    return inspect.iscoroutinefunction(obj)


async def sleep_ms(ms):
    """Asynchronous sleep for 'ms' milliseconds."""

    if is_micropython:
        await asyncio.sleep_ms(ms)

    else:
        await asyncio.sleep(ms / 1000)
