"""
Contains a definition of a column layout container. This is a vertical
container box.

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
from .box import Box
from ..core.property import ChoiceProperty
from ..core.measures import COMPONENT_DISTRIBUTION


class Column(Box):
    """
    A vertical container box.
    """

    vertical_align_content = ChoiceProperty(
        _("Alignment of child components in this column."),
        choices=COMPONENT_DISTRIBUTION,
        map_to_style="justify-content",
        group="layout",
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M104 32H64a16 16 0 0 0-16 16v160a16 16 0 0 0 16 16h40a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16m0 176H64V48h40Zm88-176h-40a16 16 0 0 0-16 16v160a16 16 0 0 0 16 16h40a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16m0 176h-40V48h40Z"/></svg>'  # noqa

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.element.style["flex-direction"] = "column"
