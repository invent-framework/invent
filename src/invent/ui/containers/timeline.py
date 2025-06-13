"""
A timeline container is a column for displaying time-based data. For use as a
social media feed or an ordered list of events such as in a chat app.

Child components are laid out in a vertical column, with the latest at either
the top (as in a social media feed) or the bottom (as in a chat app). Arbitrary
child components can be added to the timeline container. However, it is
recommended to use the `TimelineEntry` component for consistency.

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
from ..core.property import ListProperty, ChoiceProperty
from .column import Column


class Timeline(Column):
    """
    A column for displaying time-based data.
    """

    direction = ChoiceProperty(
        _("The direction of the timeline entries"),
        choices=["latest-at-top", "latest-at-bottom"],
        default_value="latest-at-top",
    )

    entries = ListProperty(_("The timeline entries"))

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><path fill="currentColor" d="M216 80h-32V48a16 16 0 0 0-16-16H40a16 16 0 0 0-16 16v128a8 8 0 0 0 13 6.22L72 154v30a16 16 0 0 0 16 16h93.59L219 230.22a8 8 0 0 0 5 1.78a8 8 0 0 0 8-8V96a16 16 0 0 0-16-16M66.55 137.78L40 159.25V48h128v88H71.58a8 8 0 0 0-5.03 1.78M216 207.25l-26.55-21.47a8 8 0 0 0-5-1.78H88v-32h80a16 16 0 0 0 16-16V96h32Z"/></svg>'  # noqa

    def on_direction_changed(self):
        if self.direction == "latest-at-top":
            self.element.style["flex-direction"] = "column-reverse"
        else:
            self.element.style["flex-direction"] = "column"

    def on_entries_changed(self):
        self.clear_children()
        for entry in self.entries:
            self.add_child(entry)

    def add_entry(self, entry):
        """
        Add a timeline entry to the timeline.
        """
        self.add_child(entry)
        return self
