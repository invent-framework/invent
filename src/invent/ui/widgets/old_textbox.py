"""
A textboc widget for the Invent framework. Displays Markdown text.

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

# from pyscript.js_modules import showdown
from invent.ui import Widget


class TextBox(Widget):
    """
    Contains textual (Markdown) content.
    """

    def __init__(self, content, id=None, position="FILL"):
        """
        All TextBoxes have:

        * A content string (containing Markdown).
        * The id and position values defined by the base Widget class.
        """
        super().__init__(id, position)
        self._content = content

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value
        self.update()

    def update(self):
        """
        Update the content of the text area from Markdown to HTML.
        """
        if self.element:
            ...
            # converter = showdown.Converter.new()
            # self.element.innerHTML = converter.makeHtml(self.content)

    def render_into(self, container):
        self.element = document.createElement("div")
        self.element.id = self.id
        self.update()
        container.appendChild(self.element)
        self.set_position(container)
