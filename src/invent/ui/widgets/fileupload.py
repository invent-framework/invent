"""
A file upload widget for the Invent framework.

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

from pyscript import document
from invent.ui.core import (
    Widget,
    TextProperty,
    IntegerProperty,
    BooleanProperty,
    ChoiceProperty,
    MessageBlueprint,
    ListProperty,
)


class FileUpload(Widget):
    """
    A file upload widget.
    """

    files = ListProperty("The files to upload")
    required = BooleanProperty(
        "A flag to indicate entry into the text box is required.",
        default_value=False,
        map_to_attribute="required",
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><g fill="currentColor"><path d="M208 88h-56V32Z" opacity="0.2"/><path d="m213.66 82.34l-56-56A8 8 0 0 0 152 24H56a16 16 0 0 0-16 16v176a16 16 0 0 0 16 16h144a16 16 0 0 0 16-16V88a8 8 0 0 0-2.34-5.66M160 51.31L188.69 80H160ZM200 216H56V40h88v48a8 8 0 0 0 8 8h48zm-42.34-77.66a8 8 0 0 1-11.32 11.32L136 139.31V184a8 8 0 0 1-16 0v-44.69l-10.34 10.35a8 8 0 0 1-11.32-11.32l24-24a8 8 0 0 1 11.32 0Z"/></g></svg>'  # noqa

    def render(self):
        element = document.createElement("input")
        element.id = self.id
        element.setAttribute("type", "file")
        return element
