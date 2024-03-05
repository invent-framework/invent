"""
A text input widget for the Invent framework. For textual user input.

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
)


class TextInput(Widget):
    """
    A single line box for short amounts of textual input.


    """

    value = TextProperty("The text in the text box.")
    required = BooleanProperty(
        "A flag to indicate entry into the text box is required.",
        default_value=False,
    )
    readonly = BooleanProperty(
        "A flag to indicate the text box is read only.", default_value=False
    )
    placeholder = TextProperty(
        "The placeholder text to put into the empty text box."
    )
    minlength = IntegerProperty("The minimum character length for the input.")
    maxlength = IntegerProperty("The maximum character length for the input.")
    input_type = ChoiceProperty(
        "The type of text input.",
        default_value="text",
        choices=[
            "text",
            "email",
            "password",
            "tel",
            "url",
        ],
    )
    keypress = MessageBlueprint(
        "Triggered when a key is pressed to enter text.",
        key="The key that was pressed.",
    )

    @classmethod
    def preview(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M112 40a8 8 0 0 0-8 8v16H24A16 16 0 0 0 8 80v96a16 16 0 0 0 16 16h80v16a8 8 0 0 0 16 0V48a8 8 0 0 0-8-8M24 176V80h80v96Zm224-96v96a16 16 0 0 1-16 16h-88a8 8 0 0 1 0-16h88V80h-88a8 8 0 0 1 0-16h88a16 16 0 0 1 16 16M88 112a8 8 0 0 1-8 8h-8v24a8 8 0 0 1-16 0v-24h-8a8 8 0 0 1 0-16h32a8 8 0 0 1 8 8"/></svg>'  # noqa

    def on_value_changed(self):
        self.update_attribute("value", self.value)

    def on_required_changed(self):
        self.update_attribute("required", self.required)

    def on_readonly_changed(self):
        self.update_attribute("disabled", self.readonly)

    def on_placeholder_changed(self):
        self.update_attribute("placeholder", self.placeholder)

    def on_minlength_changed(self):
        self.update_attribute("minlength", self.minlength)

    def on_maxlength_changed(self):
        self.update_attribute("maxlength", self.maxlength)

    def on_input_type_changed(self):
        self.update_attribute("type", self.input_type)

    def render(self):
        element = document.createElement("input")
        element.id = self.id
        return element
