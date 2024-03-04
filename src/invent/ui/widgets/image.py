"""
A minimal image.
"""

from invent import publish, Message
from invent.ui.core import Widget, TextProperty
from pyscript import document


class Image(Widget):
    image = TextProperty(
        "The path to the image media.",
        default_value="http://placekitten.com/400/400",
    )

    @classmethod
    def preview(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M216 40H40a16 16 0 0 0-16 16v144a16 16 0 0 0 16 16h176a16 16 0 0 0 16-16V56a16 16 0 0 0-16-16m0 16v102.75l-26.07-26.06a16 16 0 0 0-22.63 0l-20 20l-44-44a16 16 0 0 0-22.62 0L40 149.37V56ZM40 172l52-52l80 80H40Zm176 28h-21.37l-36-36l20-20L216 181.38zm-72-100a12 12 0 1 1 12 12a12 12 0 0 1-12-12"/></svg>'  # noqa

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
