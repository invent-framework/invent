"""
A footer is a horizontal container used to show content at the bottom of the
page. The footer can be sticky, meaning it will stay at the bottom of the page
even when the user scrolls up. Typically the footer may contain a logo,
copyright information or a menu.

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
from .row import Row
from ..core.property import ChoiceProperty
from ..core.measures import COMPONENT_DISTRIBUTION


class Footer(Row):
    """
    Footer is a horizontal container used to show content at the bottom of the
    page. The footer can be sticky, meaning it will stay at the bottom of the
    page even when the user scrolls up. Typically the footer may contain a logo,
    copyright information or a menu.

    The Footer is useful for displaying a consistent navigation experience
    across different pages. The Footer is a subclass of the Row container and
    inherits all of its properties and methods.
    """

    ...
