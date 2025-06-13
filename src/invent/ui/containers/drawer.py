"""
A drawer is a column that can show/hide a sidebar on the left or right side of
the page.

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
from .column import Column
from ..core.property import ChoiceProperty
from ..core.measures import COMPONENT_DISTRIBUTION


class Drawer(Column):
    """
    Drawer is a column that acts as a dynamic sidebar on the left or right side
    of the page. The Drawer is initially hidden, but once triggered it will
    slide into view, allowing for a more interactive user experience. Clicking
    outside the Drawer will cause it to slide back into a hidden state.

    The Drawer is useful for displaying additional information or controls
    without cluttering the main interface. The Drawer is a subclass of the
    Column container and inherits all of its properties and methods.
    """

    ...
