"""
Utility functions relating to the user interface aspects of the Invent
framework.

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

import random
from pyscript import document
from pyscript.ffi import create_proxy


__all__ = [
    "random_id",
    "sanitize",
]


# Characters to use when generating a unique ID.
_ID_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def random_id(prefix="invent", separator="-", length=10):
    """
    Generate a valid yet random looking id.

    Takes the form of:

    prefix + separator + length random _ID_CHARS
    """
    return (
        prefix
        + separator
        + "".join([random.choice(_ID_CHARS) for i in range(length)])
    )


def sanitize(raw):
    """
    Returns an HTML safe version of the raw input string.
    """
    temp = document.createElement("div")
    temp.innerText = raw
    return temp.innerHTML


def proxy(function):
    if not function:
        return None

    return create_proxy(function)
