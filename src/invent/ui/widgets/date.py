"""
A date picker widget for the Invent framework.

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

from invent.i18n import _
from pyscript.web import input_, label, div
from pyscript.ffi import create_proxy

from invent.ui.core import Widget, DateProperty, TextProperty, TimeProperty


class DatePicker(Widget):
    """
    A widget for picking a date.
    """

    date = DateProperty(
        _("The date to display in the picker."), default_value=None
    )

    label = TextProperty(
        _("An optional label shown next to the picker"),
        default_value="Select a date.",
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M208 32h-24v-8a8 8 0 0 0-16 0v8H88v-8a8 8 0 0 0-16 0v8H48a16 16 0 0 0-16 16v160a16 16 0 0 0 16 16h160a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16M72 48v8a8 8 0 0 0 16 0v-8h80v8a8 8 0 0 0 16 0v-8h24v32H48V48Zm136 160H48V96h160zm-68-76a12 12 0 1 1-12-12a12 12 0 0 1 12 12m44 0a12 12 0 1 1-12-12a12 12 0 0 1 12 12m-88 40a12 12 0 1 1-12-12a12 12 0 0 1 12 12m44 0a12 12 0 1 1-12-12a12 12 0 0 1 12 12m44 0a12 12 0 1 1-12-12a12 12 0 0 1 12 12"/></svg>'  # noqa

    def on_changed(self, event):
        """
        Bound to the js "changed" event on the widget's element.
        """
        self.date = self._input_element.value

    def on_id_changed(self):
        self._input_element.id = self.id
        self._text_label.setAttribute("for", self.id)

    def on_name_changed(self):
        self._input_element.name = self.name

    def on_label_changed(self):
        self._text_label.innerText = self.label

    def on_date_changed(self):
        self._input_element.value = f"{self.date}"

    def render(self):
        self._input_element = input_(type="date", id=self.id, name=self.name)
        self._text_label = label(self.label)
        setattr(self._text_label, "for", self.id)
        element = div(self._input_element, self._text_label)
        self._input_element.addEventListener(
            "change", create_proxy(self.on_changed)
        )
        return element
