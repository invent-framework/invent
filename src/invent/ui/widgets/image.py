"""
A minimal image.
"""

from invent import publish, Message
from invent.ui.core import Widget, TextProperty
from pyscript import document


class Image(Widget):
    image = TextProperty("The path to the image media.", default_value="http://placekitten.com/200/200")

    def __init__(self, image=None, **kwargs):
        super().__init__(**kwargs)

        if image is not None:
            self.image = str(image)

        self.element = self.render()

    @classmethod
    def preview(cls):
        return '<img src="http://placekitten.com/200/200">'

    def touch(self, event):
        publish(Message("touch"), to_channel=self.channel)

    def render(self):
        element = document.createElement("img")
        element.src = self.image
        element.addEventListener("click", self.touch)
        return element