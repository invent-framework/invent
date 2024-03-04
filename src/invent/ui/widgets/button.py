"""
A minimal button.
"""

from invent.ui.core import Widget, TextProperty
from pyscript import document


class Button(Widget):
    label = TextProperty("The text on the button.", default_value="Click Me")

    @classmethod
    def preview(cls):
        return "<button>Button</button>"

    def click(self, event):
        self.publish("press", button=self.name)

    def on_label_changed(self):
        self.element.innerText = self.label

    def render(self):
        element = document.createElement("button")
        element.id = self.id
        element.innerText = self.label
        element.addEventListener("click", self.click)
        return element
