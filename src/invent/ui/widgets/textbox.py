"""
A minimal area of the UI containing textual content.
"""

from invent.ui.core import Widget, TextProperty
from pyscript import document


class TextBox(Widget):
    text = TextProperty("The content to display.", default_value="Text")

    @classmethod
    def preview(cls):
        return "<div>TextBox</div>"

    def on_text_changed(self):
        self.element.innerText = self.text

    def render(self):
        element = document.createElement("div")
        element.id = self.id
        element.innerText = self.text
        return element
