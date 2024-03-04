"""
A minimal button.
"""

from invent.ui.core import Widget, TextProperty
from pyscript import document


class Button(Widget):
    label = TextProperty("The text on the button.", default_value="Click Me")

    @classmethod
    def preview(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M216 40H40a16 16 0 0 0-16 16v144a16 16 0 0 0 16 16h176a16 16 0 0 0 16-16V56a16 16 0 0 0-16-16m0 160H40V56h176z"/></svg>'  # noqa

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
