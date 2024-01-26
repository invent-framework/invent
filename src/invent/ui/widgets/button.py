"""
A minimal button.
"""
from invent import publish, Message
from pyscript import document


class Button:

    def __init__(self, name, label, channel):
        self.name = name
        self.label = label
        self.channel = channel
        self.element = None

    def click(self, event):
        publish(
            Message("press", button=self.name),
            to_channel=self.channel
        )
    
    def render(self):
        self.element = document.createElement("button")
        self.element.id = self.name
        self.element.innerText = self.label
        self.element.addEventListener("click", self.click)
        return self.element
