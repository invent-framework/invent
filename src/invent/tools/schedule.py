"""
Scheduling functions for the Invent framework.

Based on original pre-COVID work by [Nicholas H.Tollervey.](https://ntoll.org/)

Copyright (c) 2024 Invent contributors.

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
from pyscript import window
from pyscript.ffi import create_proxy


#: A dictionary of scheduled functions, keyed by the function's ID. The value
#: is the handle returned by the JavaScript `setTimeout` function. This handle
#: can be used to cancel the scheduled function.
SCHEDULED_FUNCTIONS = {}


def schedule(func, delay, *args, **kwargs):
    """
    Schedule the given function to be called after the given delay (in
    milliseconds).

    The function will be called with the given arguments and keyword arguments.

    Returns a handle, in the form of a positive integer, that can be used to
    cancel the scheduled function.

    This is a simple wrapper around the JavaScript `setTimeout` function:

    https://developer.mozilla.org/en-US/docs/Web/API/Window/setTimeout
    """
    if not callable(func):
        raise ValueError(_("The func argument must be a callable."))
    if delay < 0:
        raise ValueError(_("Delay must be a non-negative number."))
    func_id = id(func)
    if func_id in SCHEDULED_FUNCTIONS:
        raise ValueError(_("Function already scheduled."))
    
    def wrapper():
        """
        Call the function, then remove it from the scheduled functions because
        it's no longer scheduled!
        """
        func(*args, **kwargs)
        SCHEDULED_FUNCTIONS.pop(func_id, None)

    handle = window.setTimeout(create_proxy(wrapper), delay)
    SCHEDULED_FUNCTIONS[func_id] = handle
    return handle


def repeatedly_schedule(func, delay, *args, **kwargs):
    """
    Schedule the given function to be called repeatedly with the given delay
    (in milliseconds).

    The function will be called with the given arguments and keyword arguments.

    Returns a handle, in the form of a positive integer, that can be used to
    cancel the scheduled function.

    This is a simple wrapper around the JavaScript `setInterval` function:

    https://developer.mozilla.org/en-US/docs/Web/API/Window/setInterval
    """
    if not callable(func):
        raise ValueError(_("The func argument must be a callable."))
    if delay < 0:
        raise ValueError(_("Delay must be a non-negative number."))
    func_id = id(func)
    if func_id in SCHEDULED_FUNCTIONS:
        raise ValueError(_("Function already scheduled."))
    handle = window.setInterval(create_proxy(func), delay, *args, **kwargs)
    SCHEDULED_FUNCTIONS[func_id] = handle
    return handle


def cancel_scheduled_function(func):
    """
    Cancel the scheduled function.

    Returns a boolean indicating whether the function was successfully
    cancelled.

    This is a simple wrapper around the JavaScript `clearTimeout` function:

    https://developer.mozilla.org/en-US/docs/Web/API/Window/clearTimeout
    """
    handle = SCHEDULED_FUNCTIONS.pop(id(func), None)
    if handle is not None:
        window.clearTimeout(handle)
        return True
    return False
