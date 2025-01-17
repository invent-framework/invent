"""
A selector widget containing choices, for the Invent framework.

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
from pyscript.web import select
from pyscript.ffi import create_proxy
from invent.ui.core import Widget, TextProperty, ListProperty, Event


class Selector(Widget):
    """
    A drop-down selector widget containing choices.
    """

    value = TextProperty(_("The selected option."), default_value="")

    choices = ListProperty(_("The options from which to select."))

    changed = Event(
        _("The selected option has changed."),
        selected=_("The new selected option."),
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M112 40a8 8 0 0 0-8 8v16H24A16 16 0 0 0 8 80v96a16 16 0 0 0 16 16h80v16a8 8 0 0 0 16 0V48a8 8 0 0 0-8-8M24 176V80h80v96Zm224-96v96a16 16 0 0 1-16 16h-88a8 8 0 0 1 0-16h88V80h-88a8 8 0 0 1 0-16h88a16 16 0 0 1 16 16M88 112a8 8 0 0 1-8 8h-8v24a8 8 0 0 1-16 0v-24h-8a8 8 0 0 1 0-16h32a8 8 0 0 1 8 8"/></svg>'  # noqa

    def on_choices_changed(self):
        self.element.options.clear()
        for choice in self.choices:
            selected = bool(choice == self.value)
            self.element.options.add(
                value=choice, text=choice, selected=selected
            )

    def on_change(self, event):
        """
        Bound to the js "change" event on the widget's element.
        """
        self.value = self.element.options.selected.value
        self.publish("changed", selected=self.value)

    def render(self):
        element = select(id=self.id)
        element.addEventListener("change", create_proxy(self.on_change))
        return element
