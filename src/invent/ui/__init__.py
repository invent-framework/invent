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
from .widgets.audio import Audio
from .widgets.button import Button
from .widgets.code import Code
from .widgets.html import Html
from .widgets.image import Image
from .widgets.textbox import TextBox
from .widgets.textinput import TextInput
from .widgets.slider import Slider
from .widgets.audio import Audio


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
    "Audio",
    "Button",
    "Code",
    "Html",
    "Image",
    "Slider",
    "TextBox",
    "TextInput",
]


AVAILABLE_COMPONENTS = {
    # Containers...
    _("Column"): Column,
    _("Row"): Row,
    # Widgets...
    _("Audio"): Audio,
    _("Button"): Button,
    _("Code"): Code,
    _("Html"): Html,
    _("Image"): Image,
    _("Slider"): Slider,
    _("TextBox"): TextBox,
    _("TextInput"): TextInput,
}
