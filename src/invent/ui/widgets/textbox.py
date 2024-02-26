"""
A minimal area of the UI containing textual content.
"""

from invent import publish, Message
from invent.ui.core import Widget, TextProperty
from pyscript import document


class TextBox(Widget):
    text = TextProperty("The content to display.")

    def __init__(self, text, name=None):
        super().__init__(name=name)
        self.text = text
        self.render()

    def on_text_changed(self):
        self.element.innerText = self.text

    def render(self):
        self.element = document.createElement("div")
        self.element.id = self.id
        self.on_text_changed()
