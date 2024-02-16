"""
A minimal button.
"""

from invent import publish, Message
from invent.ui.core import Widget, TextProperty
from pyscript import document


class Button(Widget):
    label = TextProperty("The text on the button.")

    def __init__(self, name, label, channel):
        super().__init__(name=name, channel=channel)
        self.name = name
        self.label = label
        self.channel = channel

    def click(self, event):
        publish(Message("press", button=self.name), to_channel=self.channel)

    def render(self):
        self.element = document.createElement("button")
        self.element.id = self.name
        self.element.innerText = self.label
        self.element.addEventListener("click", self.click)
        return self.element
