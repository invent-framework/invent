"""
A rating is used to show a rating of something, like a movie, book, etc. The
rating can be used as input (to indicate the user's rating) or as a read-only
output (to show the rating of something). A rating is a number of stars (or
other symbols) that can be filled or empty. The rating can be set to a number
between 0 and the maximum number of stars (or other symbols).

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
from invent.ui.core import (
    Widget,
    TextProperty,
    ChoiceProperty,
    Event,
)
