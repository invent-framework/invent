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

from toga import Box, Button, Label, TextInput, Widget
from toga.sources import ValueSource
from toga.style import Pack

import invent
from .. import Message, publish, subscribe
from ..i18n import _
from .app import App
from .box import Row, Column
from .page import Page
from .utils import random_id, sanitize

__all__ = [
    "random_id",
    "sanitize",
    "App",
    # "Code",
    "Page",
    "Widget",
    "Box",
    "Column",
    # "Grid",
    "Row",
    "from_datastore",
    "to_channel",
    # "Audio",
    "Button",
    # "CheckBox",
    # "Code",
    # "FileUpload",
    # "Html",
    # "Image",
    # "Slider",
    # "Switch",
    "Label",
    "TextInput",

    "Pack",
]


def to_channel(channel):
    def handler(widget, **kwargs):
        # TODO: generalize `press` and `button`.
        publish(Message("press", button=widget), channel)

    return handler


class from_datastore(ValueSource):
    def __init__(self, key, with_function=None):
        super().__init__()
        self.key = key
        self.with_function = with_function
        self.accessor = "value"
        subscribe(self.reactor, "store-data", when_subject=key)

    def reactor(self, message):
        self.notify("change", item=self.value)

    @property
    def value(self):
        result = invent.datastore.get(self.key)
        if self.with_function:
            result = self.with_function(result)
        return result

    @value.setter
    def value(self, new_value):
        pass  # TODO


# AVAILABLE_COMPONENTS = {
#     # Containers...
#     _("Column"): Column,
#     _("Row"): Row,
#     _("Grid"): Grid,
#     # Widgets...
#     _("Audio"): Audio,
#     _("Button"): Button,
#     _("CheckBox"): CheckBox,
#     _("Code"): Code,
#     _("FileUpload"): FileUpload,
#     _("Html"): Html,
#     _("Image"): Image,
#     _("Slider"): Slider,
#     _("Switch"): Switch,
#     _("TextBox"): TextBox,
#     _("TextInput"): TextInput,
# }


def create_component(component_cls_name, **kwargs):
    """
    Create an instance of the subclass of Component with the specified name.
    """

    component_klass = AVAILABLE_COMPONENTS.get(component_cls_name)
    if component_klass is None:
        raise ValueError(f"No such component type: {component_cls_name}")

    return component_klass(**kwargs)
