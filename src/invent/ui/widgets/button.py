"""
A minimal button.
"""

from invent import publish, Message
from invent.ui.core import Widget, TextProperty
from pyscript import document


class Button(Widget):
    label = TextProperty("The text on the button.", default_value="Click Me")

    def __init__(self, name=None, id=None, position="TOP-LEFT", channel=None, label=None):
        super().__init__(name=name, id=id, position=position, channel=channel)

        if label is not None:
            self.label = label

        self.element = self.render()

    @classmethod
    def preview(cls):
        return "<button>Button</button>"

    def click(self, event):
        publish(Message("press", button=self.name), to_channel=self.channel)

    def on_label_changed(self):
        self.element.innerText = self.label

    def render(self):
        element = document.createElement("button")
        element.id = self.id
        element.innerText = self.label
        element.addEventListener("click", self.click)
        return element
