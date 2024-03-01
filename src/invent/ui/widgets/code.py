"""
A minimal area of the UI containing CODE content.
"""

from invent.ui.core import Widget, TextProperty
from pyscript import document


class Code(Widget):
    code = TextProperty("The code to display.", default_value="Text")

    @classmethod
    def preview(cls):
        return "<pre>Code</pre>"

    def on_code_changed(self):
        self.element.innerText = self.code

    def render(self):
        element = document.createElement("pre")
        element.id = self.id
        element.innerText = self.code
        return element
