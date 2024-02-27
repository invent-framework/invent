"""
A minimal area of the UI containing textual content.
"""

from invent.ui.core import Widget, TextProperty
from pyscript import document


class TextBox(Widget):
    text = TextProperty("The content to display.", default_value="Text")

    def __init__(self, text=None, **kwargs):
        super().__init__(**kwargs)

        if text is not None:
            self.text = text

        self.element = self.render()

    @classmethod
    def preview(cls):
        return "<div>TextBox</div>"

    def on_text_changed(self):
        if self.element:
            self.element.innerText = self.text

    def render(self):
        element = document.createElement("div")
        element.id = self.id
        element.innerText = self.text
        return element
