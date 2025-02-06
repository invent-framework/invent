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

from collections.abc import Iterable

from toga.widgets.base import StyleT, Widget


class Grid(Widget):
    """
    A grid.
    """

    def __init__(
        self,
        *,
        id: str | None = None,
        style: StyleT | None = None,
        children: Iterable[Widget] | None = None,
        **kwargs,
    ):
        super().__init__(id, style, **kwargs)

        self._children = []
        if children is not None:
            self.add(*children)

    def _create(self):
        return self.factory.Grid(interface=self)
