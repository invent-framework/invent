"""
An image widget for the Invent framework.

Based on original pre-COVID work by [Nicholas H.Tollervey.](https://ntoll.org/)

Copyright (c) 2024 Invent contributors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from invent.ui.core import Widget, MessageBlueprint
from invent.ui.properties import TextProperty
from pyscript import document


class Image(Widget):
    """
    Represents an image to display on the user interface.
    """

    image = TextProperty(
        "The path to the image media.",
        default_value="https://loremflickr.com/400/400",
    )

    touch = MessageBlueprint(
        "Sent when the image is touched.",
    )

    position = TextProperty(
        "The component's position inside it's parent.",
        default_value="MIDDLE-CENTER",
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M216 40H40a16 16 0 0 0-16 16v144a16 16 0 0 0 16 16h176a16 16 0 0 0 16-16V56a16 16 0 0 0-16-16m0 16v102.75l-26.07-26.06a16 16 0 0 0-22.63 0l-20 20l-44-44a16 16 0 0 0-22.62 0L40 149.37V56ZM40 172l52-52l80 80H40Zm176 28h-21.37l-36-36l20-20L216 181.38zm-72-100a12 12 0 1 1 12 12a12 12 0 0 1-12-12"/></svg>'  # noqa

    def on_image_changed(self):
        self.element.src = self.image

    def touch_handler(self, event):
        self.publish("touch")

    def render(self):
        element = document.createElement("img")
        element.id = self.id
        element.src = self.image
        element.addEventListener("click", self.touch_handler)
        return element
