"""
Contains a definition of a grid layout container.

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
from ..core.container import Container
from ..core.property import ChoiceProperty, IntegerProperty
from ..core.measures import TSHIRT_SIZES, MEDIUM


class Grid(Container):
    """
    A grid.
    """

    column_gap = ChoiceProperty(
        _("The gap between columns in the grid."),
        choices=TSHIRT_SIZES,
        default_value=MEDIUM,
    )
    row_gap = ChoiceProperty(
        _("The gap between rows in the grid."),
        choices=TSHIRT_SIZES,
        default_value=MEDIUM,
    )

    columns = IntegerProperty(_("Number of columns."), 4)

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M216 48H40a16 16 0 0 0-16 16v128a16 16 0 0 0 16 16h176a16 16 0 0 0 16-16V64a16 16 0 0 0-16-16m-112 96v-32h48v32Zm48 16v32h-48v-32ZM40 112h48v32H40Zm64-16V64h48v32Zm64 16h48v32h-48Zm48-16h-48V64h48ZM88 64v32H40V64Zm-48 96h48v32H40Zm176 32h-48v-32h48z"/></svg>'  # noqa

    def on_column_gap_changed(self):
        self._set_gap(self.column_gap, "column-gap")

    def on_row_gap_changed(self):
        self._set_gap(self.row_gap, "row-gap")

    def on_columns_changed(self):
        self.element.style["grid-template-columns"] = "auto " * self.columns

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content_align = "stretch"

    def render(self):
        """
        Render the component.
        """
        element = super().render()
        element.style["display"] = "grid"
        return element
