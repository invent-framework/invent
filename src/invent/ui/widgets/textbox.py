"""
A minimal area of the UI containing textual content.
"""
from invent import publish, Message
from invent.ui.core import Widget, Property
from pyscript import document


class TextBox(Widget):
    text = Property("The content to display.")

    def __init__(self, text, name=None):
        super().__init__(name=name)
        self.text = text

    def render(self):
        if not self.element:
            self.element = document.createElement("div")
            self.element.id = self.name
        self.element.innerText = str(self.text)
        return self.element
