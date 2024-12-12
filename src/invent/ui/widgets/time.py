"""
A time picker widget for the Invent framework.

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


class TimePicker(Widget):
    """
    A widget for picking a time.
    """

    time = TimeProperty(
        _("The time to display in the picker."), default_value=None
    )

    label = TextProperty(
        _("An optional label shown next to the picker"),
        default_value="Select a time.",
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M128 24a104 104 0 1 0 104 104A104.11 104.11 0 0 0 128 24m0 192a88 88 0 1 1 88-88a88.1 88.1 0 0 1-88 88m64-88a8 8 0 0 1-8 8h-56a8 8 0 0 1-8-8V72a8 8 0 0 1 16 0v48h48a8 8 0 0 1 8 8"/></svg>'  # noqa

    def on_changed(self, event):
        """
        Bound to the js "changed" event on the widget's element.
        """
        self.time = self._input_element.value

    def on_id_changed(self):
        self._input_element.id = self.id
        self._text_label.setAttribute("for", self.id)

    def on_name_changed(self):
        self._input_element.name = self.name

    def on_label_changed(self):
        self._text_label.innerText = self.label

    def on_time_changed(self):
        self._input_element.value = f"{self.time}"

    def render(self):
        self._input_element = input_(type="time", id=self.id, name=self.name)
        self._text_label = label(self.label)
        setattr(self._text_label, "for", self.id)
        element = div(self._input_element, self._text_label)
        self._input_element.addEventListener(
            "change", create_proxy(self.on_changed)
        )
        return element
