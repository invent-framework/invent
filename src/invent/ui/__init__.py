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
from .core import Widget, Container, from_datastore
from .utils import random_id, sanitize
from .containers.column import Column
from .containers.grid import Grid
from .containers.page import Page
from .containers.row import Row
from .widgets.audio import Audio
from .widgets.button import Button
from .widgets.checkbox import CheckBox
from .widgets.code import Code
from .widgets.fileupload import FileUpload
from .widgets.html import Html
from .widgets.image import Image
from .widgets.slider import Slider
from .widgets.switch import Switch
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
    "Grid",
    "Row",
    "from_datastore",
    "Audio",
    "Button",
    "CheckBox",
    "Code",
    "FileUpload",
    "Html",
    "Image",
    "Slider",
    "Switch",
    "TextBox",
    "TextInput",
]


AVAILABLE_COMPONENTS = {
    # Containers...
    _("Column"): Column,
    _("Row"): Row,
    _("Grid"): Grid,
    # Widgets...
    _("Audio"): Audio,
    _("Button"): Button,
    _("CheckBox"): CheckBox,
    _("Code"): Code,
    _("FileUpload"): FileUpload,
    _("Html"): Html,
    _("Image"): Image,
    _("Slider"): Slider,
    _("Switch"): Switch,
    _("TextBox"): TextBox,
    _("TextInput"): TextInput,
}


def create_component(component_cls_name, **kwargs):
    """
    Create an instance of the subclass of Component with the specified name.
    """

    component_klass = AVAILABLE_COMPONENTS.get(component_cls_name)
    if component_klass is None:
        raise ValueError(f"No such component type: {component_cls_name}")

    return component_klass(**kwargs)
