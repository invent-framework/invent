"""
A minimal area of the UI containing textual content.
"""

from invent.ui.core import Widget, TextProperty
from pyscript import document


class TextBox(Widget):
    text = TextProperty("The content to display.", default_value="Text")

    @classmethod
    def preview(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M216 40H40a16 16 0 0 0-16 16v144a16 16 0 0 0 16 16h176a16 16 0 0 0 16-16V56a16 16 0 0 0-16-16m0 160H40V56h176zM184 96a8 8 0 0 1-8 8H80a8 8 0 0 1 0-16h96a8 8 0 0 1 8 8m0 32a8 8 0 0 1-8 8H80a8 8 0 0 1 0-16h96a8 8 0 0 1 8 8m0 32a8 8 0 0 1-8 8H80a8 8 0 0 1 0-16h96a8 8 0 0 1 8 8"/></svg>'  # noqa

    def on_text_changed(self):
        self.element.innerText = self.text

    def render(self):
        element = document.createElement("div")
        element.id = self.id
        element.innerText = self.text
        return element
