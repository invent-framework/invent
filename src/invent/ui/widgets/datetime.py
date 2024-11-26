"""
A datetime picker widget for the Invent framework.

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

from pyscript.web import input_, label, div
from pyscript.ffi import create_proxy

from invent.ui.core import Widget, DateProperty, TextProperty, TimeProperty


class DateTimePicker(Widget):
    """
    A widget for picking a date and time.
    """

    date = DateProperty(
        "The date to display in the picker.", default_value=None
    )
    time = TimeProperty(
        "The time to display in the picker.", default_value=None
    )

    label = TextProperty(
        "An optional label shown next to the picker",
        default_value="Select a date/time.",
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M208 32h-24v-8a8 8 0 0 0-16 0v8H88v-8a8 8 0 0 0-16 0v8H48a16 16 0 0 0-16 16v160a16 16 0 0 0 16 16h160a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16M72 48v8a8 8 0 0 0 16 0v-8h80v8a8 8 0 0 0 16 0v-8h24v32H48V48Zm136 160H48V96h160zm-96-88v64a8 8 0 0 1-16 0v-51.06l-4.42 2.22a8 8 0 0 1-7.16-14.32l16-8A8 8 0 0 1 112 120m59.16 30.45L152 176h16a8 8 0 0 1 0 16h-32a8 8 0 0 1-6.4-12.8l28.78-38.37a8 8 0 1 0-13.31-8.83a8 8 0 1 1-13.85-8A24 24 0 0 1 176 136a23.76 23.76 0 0 1-4.84 14.45"/></svg>'  # noqa

    def on_changed(self, event):
        """
        Bound to the js "changed" event on the widget's element.
        """
        try:
            date, time = self._input_element.value.split("T")
            self.date = date
            self.time = time
        except Exception as e:
            raise ValueError(f"Invalid date/time: {e}")

    def on_id_changed(self):
        self._input_element.id = self.id
        self._text_label.setAttribute("for", self.id)

    def on_name_changed(self):
        self._input_element.name = self.name

    def on_label_changed(self):
        self._text_label.innerText = self.label

    def on_date_changed(self):
        self._update_input_value()

    def on_time_changed(self):
        self._update_input_value()

    def _update_input_value(self):
        self._input_element.value = f"{self.date}T{self.time}"

    def render(self):
        self._input_element = input_(
            type="datetime-local", id=self.id, name=self.name
        )
        self._text_label = label(self.label)
        setattr(self._text_label, "for", self.id)
        element = div(self._input_element, self._text_label)
        self._input_element.addEventListener(
            "change", create_proxy(self.on_changed)
        )
        return element
