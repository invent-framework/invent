"""
A minimal image.
"""

from invent import publish, Message
from invent.ui.core import Widget, TextProperty
from pyscript import document


class Image(Widget):
    image = TextProperty("The path to the image media.")

    def __init__(self, image, name=None, channel=None, position="FILL"):
        super().__init__(name=name, channel=channel, position=position)
        self.image = str(image)
        self.render()

    def touch(self, event):
        publish(Message("touch"), to_channel=self.channel)

    def render(self):
        self.element = document.createElement("img")
        self.element.src = self.image
        self.element.addEventListener("click", self.touch)
