"""
A button widget for the Invent framework.

Based on original pre-COVID work by [Nicholas H.Tollervey.](https://ntoll.org/)

Copyright (c) 2019-present Invent contributors.

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
from invent.ui.core import (
    Widget,
    TextProperty,
    ChoiceProperty,
    Event,
)
from pyscript.web import button
from pyscript.ffi import create_proxy


class Button(Widget):
    """
    A button. Press it.

    Can be large, medium (default) or small in size. It's also possible to
    define the button's purpose as a default, primary, secondary, success,
    warning or danger button.
    """

    text = TextProperty(_("The text on the button."), default_value="Click Me")
    size = ChoiceProperty(
        _("The size of the button."),
        default_value="MEDIUM",
        choices=["LARGE", "MEDIUM", "SMALL"],
        group="style",
    )
    purpose = ChoiceProperty(
        _("The button's purpose."),
        default_value="DEFAULT",
        choices=[
            "DEFAULT",
            "PRIMARY",
            "SECONDARY",
            "SUCCESS",
            "WARNING",
            "DANGER",
        ],
        group="style",
    )

    press = Event(
        _("Sent when the button is pressed."),
        button=_("The button that was clicked."),
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M216 40H40a16 16 0 0 0-16 16v144a16 16 0 0 0 16 16h176a16 16 0 0 0 16-16V56a16 16 0 0 0-16-16m0 160H40V56h176z"/></svg>'  # noqa

    def click(self, event):
        self.publish("press", button=self)

    def on_text_changed(self):
        self.element.innerText = self.text

    def on_size_changed(self):
        # Reset
        self.element.classList.remove("large")
        self.element.classList.remove("small")
        if self.size == "LARGE":
            self.element.classList.add("large")
        elif self.size == "SMALL":
            self.element.classList.add("small")

    def on_purpose_changed(self):
        # Reset
        self.element.classList.remove("primary")
        self.element.classList.remove("secondary")
        self.element.classList.remove("success")
        self.element.classList.remove("warning")
        self.element.classList.remove("danger")
        if self.purpose == "PRIMARY":
            self.element.classList.add("primary")
        elif self.purpose == "SECONDARY":
            self.element.classList.add("secondary")
        elif self.purpose == "SUCCESS":
            self.element.classList.add("success")
        elif self.purpose == "WARNING":
            self.element.classList.add("warning")
        elif self.purpose == "DANGER":
            self.element.classList.add("danger")

    def render(self):
        element = button(self.text, id=self.id)
        element.addEventListener("click", create_proxy(self.click))
        return element
