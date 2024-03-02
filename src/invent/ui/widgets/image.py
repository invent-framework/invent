"""
A minimal image.
"""

from invent import publish, Message
from invent.ui.core import Widget, TextProperty
from pyscript import document


class Image(Widget):
    image = TextProperty(
        "The path to the image media.",
        default_value="http://placekitten.com/200/200",
    )

    @classmethod
    def preview(cls):
        return '<img src="http://placekitten.com/250/100">'

    def touch(self, event):
        publish(Message("touch"), to_channel=self.channel)

    def render(self):
        element = document.createElement("img")
        element.id = self.id
        element.src = self.image
        element.addEventListener("click", self.touch)
        return element

    def on_image_changed(self):
        self.element.src = self.image
