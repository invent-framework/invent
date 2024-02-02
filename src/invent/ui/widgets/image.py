"""
A minimal image.
"""
from invent import publish, Message
from pyscript import document


class Image:
    def __init__(self, image, channel):
        self.image = image
        self.channel = channel
        self.element = None

    def touch(self, event):
        publish(Message("touch"), to_channel=self.channel)

    def render(self):
        self.element = document.createElement("img")
        self.element.src = str(self.image)
        self.element.addEventListener("click", self.touch)
        return self.element
