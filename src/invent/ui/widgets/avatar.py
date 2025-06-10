"""
An avatar is a visual representation of a user or entity. Avatars are commonly
used in social media, forums, and other online communities to help users 
identify each other and personalize their online experience. They can also be
used in applications to represent users in chat interfaces, comments sections,
and other interactive elements. Avatars can be circular or square.

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