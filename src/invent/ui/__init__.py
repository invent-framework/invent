"""
The core classes for user interface things in the Invent framework.

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

from ..i18n import _
from .app import App
from .core import Widget, Container, Column, Row, from_datastore
from .page import Page
from .utils import random_id, sanitize
from .widgets.button import Button
from .widgets.code import Code
from .widgets.image import Image
from .widgets.textbox import TextBox
from .widgets.textinput import TextInput


__all__ = [
    "random_id",
    "sanitize",
    "App",
    "Code",
    "Page",
    "Widget",
    "Container",
    "Column",
    "Row",
    "from_datastore",
    "Button",
    "Image",
    "TextBox",
    "TextInput",
]


AVAILABLE_COMPONENTS = {
    _("Column"): Column,
    _("Row"): Row,
    _("Button"): Button,
    _("Image"): Image,
    _("TextBox"): TextBox,
    _("TextInput"): TextInput,
    _("Code"): Code,
}
