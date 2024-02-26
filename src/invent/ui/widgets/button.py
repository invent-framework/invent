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
        self.render()

    def click(self, event):
        publish(Message("press", button=self.name), to_channel=self.channel)

    def on_label_changed(self):
        self.element.innerText = self.label

    def render(self):
        self.element = document.createElement("button")
        self.element.addEventListener("click", self.click)
        self.element.id = self.id
        self.element.innerText = self.label
