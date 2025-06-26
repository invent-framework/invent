"""
A checkbox widget for the Invent framework.

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
from pyscript.web import input_, label, span
from pyscript.ffi import create_proxy

from invent.ui.core import Event, Widget, BooleanProperty, TextProperty


class CheckBox(Widget):
    """
    A checkbox for indicating a boolean value.
    """

    value = BooleanProperty(
        _("The value of the checkbox."), default_value=False
    )

    label = TextProperty(
        _("An optional label shown next to the checkbox"), default_value=""
    )

    checked = Event(_("Sent when the checkbox is checked."))

    unchecked = Event(_("Sent when the checkbox is un-checked."))

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M173.66 98.34a8 8 0 0 1 0 11.32l-56 56a8 8 0 0 1-11.32 0l-24-24a8 8 0 0 1 11.32-11.32L112 148.69l50.34-50.35a8 8 0 0 1 11.32 0M224 48v160a16 16 0 0 1-16 16H48a16 16 0 0 1-16-16V48a16 16 0 0 1 16-16h160a16 16 0 0 1 16 16m-16 160V48H48v160z"/></svg>'  # noqa

    def on_changed(self, event):
        """
        Bound to the js "changed" event on the widget's element.
        """
        self.value = not self.value

    def on_id_changed(self):
        self._checkbox_element.id = self.id
        self.element.setAttribute("for", self.id)

    def on_name_changed(self):
        self._checkbox_element.name = self.name

    def on_label_changed(self):
        self._text_span.innerText = self.label

    def on_value_changed(self):
        if self.value:
            self._checkbox_element.setAttribute("checked", True)
            self.publish("checked")
        else:
            self._checkbox_element.removeAttribute("checked")
            self.publish("unchecked")

    def render(self):
        self._checkbox_element = input_(
            type="checkbox", id=self.id, name=self.name
        )
        self._text_span = span(self.label)
        self._text_span.classes.add("checkbox")
        element = label(self._checkbox_element, self._text_span)
        setattr(element, "for", self.id)
        self._checkbox_element.addEventListener(
            "change", create_proxy(self.on_changed)
        )
        return element
