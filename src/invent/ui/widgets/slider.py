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

from invent.i18n import _
from pyscript.web import input_
from pyscript.ffi import create_proxy

from invent.ui.core import Widget, NumericProperty


class Slider(Widget):
    """
    A slider for indicating a value within a certain min/max range, and of a
    certain granularity (step).
    """

    value = NumericProperty(
        _("The value of the slider."),
        default_value=50,
        map_to_attribute="value",
    )
    minvalue = NumericProperty(
        _("The minimum value of the slider."),
        default_value=0,
        map_to_attribute="min",
    )
    maxvalue = NumericProperty(
        _("The maximum value of the slider."),
        default_value=100,
        map_to_attribute="max",
    )
    step = NumericProperty(
        _("The granularity of the value of the slider."),
        default_value=1,
        map_to_attribute="step",
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M40 88h33a32 32 0 0 0 62 0h81a8 8 0 0 0 0-16h-81a32 32 0 0 0-62 0H40a8 8 0 0 0 0 16m64-24a16 16 0 1 1-16 16a16 16 0 0 1 16-16m112 104h-17a32 32 0 0 0-62 0H40a8 8 0 0 0 0 16h97a32 32 0 0 0 62 0h17a8 8 0 0 0 0-16m-48 24a16 16 0 1 1 16-16a16 16 0 0 1-16 16"/></svg>'  # noqa

    def on_input(self, event):
        """
        Bound to the js "input" event on the widget's element.
        """
        self.value = int(event.target.value)

    def on_value_changed(self):
        self.element.value = self.value

    def render(self):
        element = input_(type="range", id=self.id)
        element.addEventListener("input", create_proxy(self.on_input))
        return element
