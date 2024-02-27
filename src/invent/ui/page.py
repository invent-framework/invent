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

from pyscript import document


class Page:
    """
    Only one page at a time is displayed on the screen. Pages contain related
    widgets to achieve some aim.
    """

    def __init__(self, name, content=None):
        self.name = name
        self.content = content or []
        self.element = None

    def as_dict(self):
        """
        Return a dictionary representation of the object.
        """

        return dict(
            name=self.name, content=[item.as_dict() for item in self.content]
        )

    def append(self, component):
        """
        Append a component to the page.
        """
        self.content.append(component)

    def render(self):
        """
        Returns an HTML element to insert into the DOM.
        """
        self.element = document.createElement("div")
        self.element.classList.add("paper")
        self.element.classList.add("container")
        self.element.id = self.name
        self.hide()
        # TODO: FIX THIS FOR CONTAINERS (cols / rows)
        for item in self.content:
            self.element.appendChild(item.element)
        return self.element

    def show(self):
        """
        Make the page visible to the user.
        """
        if self.element:
            self.element.style.display = "block"

    def hide(self):
        """
        Hide the page from the user.
        """
        if self.element:
            self.element.style.display = "None"  # Hidden by default.
