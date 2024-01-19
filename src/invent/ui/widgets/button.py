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
from pyscript import document
from invent.ui import Widget


class Button(Widget):
    """
    A button.

    You push it and stuff happens. ;-)
    """

    # Button style constants.
    PLAIN = ""
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    DANGER = "DANGER"

    # Button size constants.
    LARGE = "LARGE"
    MEDIUM = "MEDIUM"
    SMALL = "SMALL"

    # Valid semantic style names that map to a CSS class to define a button's
    # look.
    STYLES = {
        "PLAIN": "",
        "PRIMARY": "btn-primary",
        "SECONDARY": "btn-secondary",
        "SUCCESS": "btn-success",
        "WARNING": "btn-warning",
        "DANGER": "btn-danger",
    }

    # Valid semantic size names that map to a CSS class to define the button's
    # size.
    SIZES = {"LARGE": "btn-large", "MEDIUM": "", "SMALL": "btn-small"}

    def __init__(
        self,
        name,
        label,
        size="MEDIUM",
        style="PLAIN",
        disabled=False,
        id=None,
        position="MIDDLE-CENTER",
    ):
        """
        All buttons have:

        * A label string written on the button.
        * A semantic size (default: MEDIUM).
        * A semantic style (default: PLAIN).
        * A disabled flag (default: False).
        * The id and position values defined by the base Widget class.
        """
        super().__init__(id, position)
        self._label = label
        self._size = size
        self._style = style
        self._disabled = disabled

    def update(self):
        """
        Updates the label, CSS classes and attributes to the correct state
        given the current label value, size, style and disabled flag.
        """
        if self.element:
            self.element.innerHTML = self._label
            self.element.className = ""
            self.element.removeAttribute("disabled")
            size = self.SIZES.get(self.size)
            if size:
                self.element.classList.add(size)
            style = self.STYLES.get(self.style)
            if style:
                self.element.classList.add(style)
            if self.disabled:
                self.element.setAttribute("disabled", "disabled")

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value
        self.update()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if value not in self.SIZES:
            raise ValueError(f"'{value}' is not a valid button size.")
        self._size = value
        self.update()

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, value):
        if value not in self.STYLES:
            raise ValueError(f"'{value}' is not a valid button style.")
        self._style = value
        self.update()

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, value):
        self._disabled = bool(value)
        self.update()

    def render_into(self, container):
        self.element = document.createElement("button")
        self.element.id = self.id
        self.update()
        container.appendChild(self.element)
        self.set_position(container)
