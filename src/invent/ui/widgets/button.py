"""
A minimal button.
"""

from invent import publish, Message
from invent.ui.core import Widget, TextProperty
from pyscript import document


class Button(Widget):
    label = TextProperty("The text on the button.", default_value="Click Me")

    def __init__(self, id=None, name=None, position="TOP-LEFT", channel=None, label=None):
        super().__init__(id=id, name=name, channel=channel, position=position)

        if label is not None:
            self.label = label

        self.element = self.render()

    def click(self, event):
        publish(Message("press", button=self.name), to_channel=self.channel)

    def on_label_changed(self):
        self.element.innerText = self.label

    def render(self):
        element = document.createElement("button")
        element.addEventListener("click", self.click)
        element.id = self.id
        element.innerText = self.label

        return element

    @classmethod
    def preview(cls):
        return cls().render().outerHTML
