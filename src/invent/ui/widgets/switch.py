"""
A slider widget for the Invent framework.

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
from pyscript.ffi import create_proxy

from invent.ui.core import Widget
from invent.ui.properties import BooleanProperty, TextProperty
from ..utils import random_id


class Switch(Widget):
    """
    A switch for indicating a boolean value.
    """

    value = BooleanProperty("The value of the switch.", default_value=False)

    label = TextProperty(
        "An optional label shown next to the switch", default_value=""
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M176 56H80a72 72 0 0 0 0 144h96a72 72 0 0 0 0-144m0 128H80a56 56 0 0 1 0-112h96a56 56 0 0 1 0 112M80 88a40 40 0 1 0 40 40a40 40 0 0 0-40-40m0 64a24 24 0 1 1 24-24a24 24 0 0 1-24 24"/></svg>'  # noqa

    def on_js_changed(self, event):
        """
        Bound to the js "changed" event on the widget's element.
        """

        self.value = not self.value

    def on_label_changed(self):
        self.label_.innerText = self.label

    def on_value_changed(self):
        if self.value:
            self.input_.setAttribute("checked", True)

        else:
            self.input_.removeAttribute("checked")

    def render(self):
        input_id = random_id()

        element = document.createElement("fieldset")
        element.classList.add("form-group")

        label = document.createElement("label")
        label.classList.add("paper-switch-2")
        element.appendChild(label)

        self.input_ = input_ = document.createElement("input")
        input_.id = input_id
        input_.name = input_id
        input_.setAttribute("type", "checkbox")
        label.appendChild(input_)

        span = document.createElement("span")
        span.classList.add("paper-switch-slider")
        label.appendChild(span)

        self.label_ = label = document.createElement("label")
        label.innerText = self.label
        label.setAttribute("for", input_id)
        label.classList.add("paper-switch-2-label")
        element.appendChild(label)

        element.addEventListener("change", create_proxy(self.on_js_changed))
        return element
