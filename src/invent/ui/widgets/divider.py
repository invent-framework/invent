"""
A divider is used to separate content vertically or horizontally.

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
from pyscript.web import hr
from invent.ui.core import Widget
from invent.ui.containers import Row


class Divider(Widget):
    """
    A divider. Renders as a vertical rule inside a Row, or a horizontal rule
    everywhere else. The actual orientation is determined after the widget is
    inserted into its parent
    """

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M216 128a8 8 0 0 1-8 8H48a8 8 0 0 1 0-16h160a8 8 0 0 1 8 8Z"/></svg>'  # noqa

    def render(self):
        # Always render as <hr> initially
        element = hr(id=self.id)
        element.classes.add("invent-divider")
        element.classes.add("invent-divider-horizontal")
        return element

    @property
    def parent(self):
        return super().parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent
        self._parent_type = type(parent).__name__
        self.on_horizontal_align_changed()
        self.on_vertical_align_changed()
        self._update_orientation()

    def _update_orientation(self):
        # Swap the orientation to match the actual parent container.
        # Called whenever the parent is assigned.
        self.element.classes.remove("invent-divider-horizontal")
        self.element.classes.remove("invent-divider-vertical")
        if isinstance(self._parent, Row):
            self.element.classes.add("invent-divider-vertical")
        else:
            self.element.classes.add("invent-divider-horizontal")
