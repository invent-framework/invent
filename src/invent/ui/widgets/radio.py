"""
A radio button widget for the Invent framework.

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
from pyscript.web import input_, label, span
from pyscript.ffi import create_proxy

from invent.ui.core import Widget, BooleanProperty, TextProperty


class Radio(Widget):
    """
    A checkbox for indicating a boolean value.
    """

    selected = BooleanProperty(
        _("A flag to indicate if the radio button is selected"),
        default_value=False,
    )

    value = TextProperty(
        _("The meaningful value associated with the checkbox."),
        default_value="",
    )

    label = TextProperty(
        _("An optional label shown next to the radio button"), default_value=""
    )

    group = TextProperty(
        _("The group to which the radio button belongs"), default_value=""
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M128 24a104 104 0 1 0 104 104A104.11 104.11 0 0 0 128 24m0 192a88 88 0 1 1 88-88a88.1 88.1 0 0 1-88 88m0-144a56 56 0 1 0 56 56a56.06 56.06 0 0 0-56-56m0 96a40 40 0 1 1 40-40a40 40 0 0 1-40 40"/></svg>'  # noqa

    def on_changed(self, event):
        """
        Bound to the js "changed" event on the widget's element.
        """
        self.selected = not self.selected

    def on_id_changed(self):
        self._radio_element.id = self.id
        self.element.setAttribute("for", self.id)

    def on_name_changed(self):
        self._radio_element.name = self.name

    def on_label_changed(self):
        self._text_span.innerText = self.label

    def on_selected_changed(self):
        if self.selected:
            self._radio_element.setAttribute("checked", True)
        else:
            self._radio_element.removeAttribute("checked")

    def on_group_changed(self):
        self._radio_element.name = self.group

    def on_value_changed(self):
        self._radio_element.value = self.value

    def render(self):
        self._radio_element = input_(type="radio", id=self.id, name=self.group)
        self._text_span = span(self.label)
        element = label(self._radio_element, self._text_span)
        setattr(element, "for", self.id)
        self._radio_element.addEventListener(
            "change", create_proxy(self.on_changed)
        )
        return element
