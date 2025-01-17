"""
An meter widget for the Invent framework.

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
from pyscript.web import meter
from invent.ui.core import (
    Widget,
    Event,
    FloatProperty,
    TextProperty,
)


class Meter(Widget):
    """
    A meter widget for displaying a value within a range.
    """

    value = FloatProperty(_("The value to display."), default_value=50.0)

    minimum = FloatProperty(_("The minimum allowed value."), default_value=0.0)

    maximum = FloatProperty(
        _("The maximum allowed value."), default_value=100.0
    )

    low = FloatProperty(
        _("The value below which the meter is considered low."),
        default_value=33.0,
        group="display",
    )

    high = FloatProperty(
        _("The value above which the meter is considered high."),
        default_value=66.0,
        group="display",
    )

    optimum = FloatProperty(
        _("The value considered to be the optimum value."),
        default_value=50.0,
        group="display",
    )

    title = TextProperty(
        _("The title of the meter, displayed when the mouse hovers over it."),
        default_value="",
    )

    changed = Event(
        _("The value of the meter has changed."),
        value=_("The new value of the meter."),
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><path fill="currentColor" d="M80 96a8 8 0 0 1-8 8H24a8 8 0 0 1 0-16h48a8 8 0 0 1 8 8m-8 24H24a8 8 0 0 0 0 16h48a8 8 0 0 0 0-16m0 32H24a8 8 0 0 0 0 16h48a8 8 0 0 0 0-16m0 32H24a8 8 0 0 0 0 16h48a8 8 0 0 0 0-16m80-64h-48a8 8 0 0 0 0 16h48a8 8 0 0 0 0-16m0 32h-48a8 8 0 0 0 0 16h48a8 8 0 0 0 0-16m0 32h-48a8 8 0 0 0 0 16h48a8 8 0 0 0 0-16m80-96h-48a8 8 0 0 0 0 16h48a8 8 0 0 0 0-16m-48-16h48a8 8 0 0 0 0-16h-48a8 8 0 0 0 0 16m48 48h-48a8 8 0 0 0 0 16h48a8 8 0 0 0 0-16m0 32h-48a8 8 0 0 0 0 16h48a8 8 0 0 0 0-16m0 32h-48a8 8 0 0 0 0 16h48a8 8 0 0 0 0-16"/></svg>'  # noqa

    def on_value_changed(self):
        self.element.value = self.value
        self.publish("changed", value=self.value)

    def on_minimum_changed(self):
        self.element.min = self.minimum

    def on_maximum_changed(self):
        self.element.max = self.maximum

    def on_low_changed(self):
        self.element.low = self.low

    def on_high_changed(self):
        self.element.high = self.high

    def on_optimum_changed(self):
        self.element.optimum = self.optimum

    def on_title_changed(self):
        self.element.title = self.title

    def render(self):
        return meter(id=self.id)
