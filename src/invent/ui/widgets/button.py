"""
A button widget for the Invent framework.

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

from invent.ui.core import (
    Widget,
    TextProperty,
    BooleanProperty,
    ChoiceProperty,
    MessageBlueprint,
)

from pyscript import document
from pyscript.ffi import create_proxy


class Button(Widget):
    """
    A button. Press it.

    Can be large, medium (default) or small in size. It's also possible to
    define the button's purpose as a default, primary, secondary, success,
    warning or danger button.
    """

    label = TextProperty("The text on the button.", default_value="Click Me")
    size = ChoiceProperty(
        "The size of the button.",
        default_value="MEDIUM",
        choices=["LARGE", "MEDIUM", "SMALL"],
    )
    purpose = ChoiceProperty(
        "The button's purpose.",
        default_value="DEFAULT",
        choices=[
            "DEFAULT",
            "PRIMARY",
            "SECONDARY",
            "SUCCESS",
            "WARNING",
            "DANGER",
        ],
    )
    disabled = BooleanProperty(
        "Indicates if the button is disabled.",
        default_value=False,
        map_to_attribute="disabled",
    )

    press = MessageBlueprint(
        "Sent when the button is pressed.",
        button="The button that was clicked.",
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M216 40H40a16 16 0 0 0-16 16v144a16 16 0 0 0 16 16h176a16 16 0 0 0 16-16V56a16 16 0 0 0-16-16m0 160H40V56h176z"/></svg>'  # noqa

    def click(self, event):
        self.publish("press", button=self)

    def on_label_changed(self):
        self.element.innerText = self.label

    def on_size_changed(self):
        # Reset
        self.element.classList.remove("btn-large")
        self.element.classList.remove("btn-small")
        if self.size == "LARGE":
            self.element.classList.add("btn-large")
        elif self.size == "SMALL":
            self.element.classList.add("btn-small")

    def on_purpose_changed(self):
        # Reset
        self.element.classList.remove("btn-primary")
        self.element.classList.remove("btn-secondary")
        self.element.classList.remove("btn-success")
        self.element.classList.remove("btn-warning")
        self.element.classList.remove("btn-danger")
        if self.purpose == "PRIMARY":
            self.element.classList.add("btn-primary")
        elif self.purpose == "SECONDARY":
            self.element.classList.add("btn-secondary")
        elif self.purpose == "SUCCESS":
            self.element.classList.add("btn-success")
        elif self.purpose == "WARNING":
            self.element.classList.add("btn-warning")
        elif self.purpose == "DANGER":
            self.element.classList.add("btn-danger")

    def render(self):
        element = document.createElement("button")
        element.id = self.id
        element.innerText = self.label
        element.addEventListener("click", create_proxy(self.click))
        return element
