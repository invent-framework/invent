"""
Contains a definition of a box layout container. This is a common base class
for Row and Column. It is a flex container box.

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
from ..core.property import ChoiceProperty
from ..core.measures import TSHIRT_SIZES, MEDIUM, COMPONENT_DISTRIBUTION


class Box(Container):
    """
    Common base class for Row and Column.
    """

    gap = ChoiceProperty(
        _("The gap between items in the container"),
        choices=TSHIRT_SIZES,
        default_value=MEDIUM,
        group="style",
    )

    def render(self):
        element = super().render()
        element.style["display"] = "flex"
        return element

    def on_gap_changed(self):
        """
        Set the gap between elements in the container (translating from t-shirt
        sizes).
        """
        self._set_gap(self.gap, "gap")
