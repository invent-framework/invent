from importlib import import_module

from . import stubs


def __getattr__(name):
    try:
        return getattr(stubs, name)
    except AttributeError:
        pass

    for package in ["toga_invent", "toga_invent.widgets"]:
        try:
            module = import_module(f"{package}.{name.lower()}")
        except ImportError:
            pass
        else:
            return getattr(module, name)

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
