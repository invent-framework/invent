"""
Contains a definition of a row layout container. This is a horizontal container
box.

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


class Row(Box):
    """
    A horizontal container box.
    """

    horizontal_align_content = ChoiceProperty(
        _("Alignment of child components in this row."),
        choices=COMPONENT_DISTRIBUTION,
        map_to_style="justify-content",
        group="layout",
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M208 136H48a16 16 0 0 0-16 16v40a16 16 0 0 0 16 16h160a16 16 0 0 0 16-16v-40a16 16 0 0 0-16-16m0 56H48v-40h160zm0-144H48a16 16 0 0 0-16 16v40a16 16 0 0 0 16 16h160a16 16 0 0 0 16-16V64a16 16 0 0 0-16-16m0 56H48V64h160z"/></svg>'  # noqa

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.element.style["flex-direction"] = "row"
