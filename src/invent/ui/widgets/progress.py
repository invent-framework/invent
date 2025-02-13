"""
An progress bar widget for the Invent framework.

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
from pyscript.web import progress
from invent.ui.core import Widget, Event, FloatProperty


class Progress(Widget):
    """
    A progress widget for displaying a value to indicate how far through a task
    the user is.
    """

    value = FloatProperty(_("The value to display."), default_value=None)

    maximum = FloatProperty(
        _("The maximum allowed value."), default_value=100.0
    )

    changed = Event(
        _("The value of the progress has changed."),
        value=_("The new progress value."),
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><path fill="currentColor" d="M128 40a96 96 0 1 0 96 96a96.11 96.11 0 0 0-96-96m0 176a80 80 0 1 1 80-80a80.09 80.09 0 0 1-80 80m45.66-125.66a8 8 0 0 1 0 11.32l-40 40a8 8 0 0 1-11.32-11.32l40-40a8 8 0 0 1 11.32 0M96 16a8 8 0 0 1 8-8h48a8 8 0 0 1 0 16h-48a8 8 0 0 1-8-8"/></svg>'  # noqa

    def on_value_changed(self):
        self.element.value = self.value
        self.publish("changed", value=self.value)

    def on_maximum_changed(self):
        self.element.max = self.maximum

    def render(self):
        return progress(id=self.id)
