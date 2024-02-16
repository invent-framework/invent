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
from invent.ui import Widget, sanitize


class TextInput(Widget):
    """
    A single line box for short amounts of text.
    """

    def __init__(
        self,
        value=None,
        label=None,
        focus=False,
        read_only=False,
        placeholder="",
        minlength=None,
        maxlength=None,
        id=None,
        position="MIDDLE",
    ):
        """
        TextInputs have these optional arguments:

        * A value to set into the TextInput (if an empty string, no value is
          set).
        * A label to describe what the input is for (if an empty string or
          None, no label is displayed)
        * A focus flag (when True, the widget acquires user focus).
        * A read_only flag (when True, the user cannot type into the
          TextInput).
        * A placeholder (containing example input if not value is set).
        * A minlength (defining the minimum number of characters to enter).
        * A maxlength (defining the maximum number of characters to enter).
        * The id and position values defined by the base Widget class.
        """
        super().__init__(id, position)
        # Reference to the HTML element for the label.
        self._label_element = None
        self._label = label
        self._value = value
        self._focus = focus
        self._read_only = read_only
        self._placeholder = placeholder
        self._minlength = minlength
        self._maxlength = maxlength
        # The HTML input type value - to be overridden by child classes.
        self._input_type = "text"

    def update(self):
        for attr in [
            "placeholder",
            "readonly",
            "minlength",
            "maxlength",
            "autofocus",
        ]:
            self.element.removeAttribute(attr)
        if self.element:
            self.element.value = self._value
            if self._focus:
                self.element.setAttribute("autofocus", "autofocus")
            if self._read_only:
                self.element.setAttribute("readonly", "readonly")
            if self._placeholder:
                self.element.setAttribute("placeholder", self._placeholder)
            if self._minlength:
                self.element.setAttribute("minlength", self._minlength)
            if self._maxlength:
                self.element.setAttribute("maxlength", self._maxlength)
        if self._label_element:
            self._label_element.innerHTML = self._label

    def render_into(self, container):
        self.element = document.createElement("input")
        self.element.id = self.id
        self.element.setAttribute("type", self._input_type)
        if self._label:
            self._label_element = document.createElement("label")
            self._label_element.setAttribute("for", self.id)
            self._label_element.innerHTML = self._label
            container.appendChild(self._label_element)
        container.appendChild(self.element)
        self.update()
        self.set_position(container)

    @property
    def value(self):
        """
        The textual content of the TextInput.
        """
        if self.element:
            self._value = self.element.value
        return sanitize(self._value)

    @value.setter
    def value(self, val):
        self._value = val
        self.update()

    @property
    def read_only(self):
        """
        A flag to indicate if the text input is read-only.
        """
        return self._read_only

    @read_only.setter
    def read_only(self, value):
        self._read_only = bool(value)
        self.update()

    @property
    def placeholder(self):
        """
        The placeholder example text to display when the value is empty.
        """
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value):
        self._placeholder = value
        self.update()

    @property
    def minlength(self):
        """
        The minimum number of characters to enter to make the text box valid.

        If None, no minimum value.
        """
        return self._minlength

    @minlength.setter
    def minlength(self, value):
        self._minlength = value
        self.update()

    @property
    def maxlength(self):
        """
        The maximium number of characters it is possible to enter.

        If None, no maximum value.
        """
        return self._maxlength

    @maxlength.setter
    def maxlength(self, value):
        self._maxlength = value
        self.update()
