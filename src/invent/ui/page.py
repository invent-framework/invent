"""
Contains the definition of an Invent page - i.e. the content of the screen at
any single point in time. Many pages make an app. Move between pages via
transitions triggered by the user.

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

from .box import Column


class Page(Column):
    """
    Only one page at a time is displayed on the screen. Pages contain related
    widgets to achieve some aim.
    """

    def __init__(self, *args, name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

        element = self._impl.element
        element.classList.add("paper")
        element.classList.add("container")

