"""
An image widget for the Invent framework.

Based on original pre-COVID work by [Nicholas H.Tollervey.](https://ntoll.org/)

Copyright (c) 2019-present Invent contributors.

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

from invent.i18n import _
from invent.ui.core import Widget, TextProperty, Event
from pyscript.web import img


#: The default image to display if none is given. The Invent logo in grey.
_DEFAULT_IMAGE = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 428.21 280.2'%3E%3Cdefs%3E%3Cstyle%3E.d%7Bfill:%23888;%7D%3C/style%3E%3C/defs%3E%3Cg id='a'/%3E%3Cg id='b'%3E%3Cg id='c'%3E%3Cg%3E%3Cg%3E%3Cpath class='d' d='M198.2,153.6c36.38,12.54,70.21,10.13,75.56-5.4,5.35-15.52-19.8-38.28-56.17-50.82-36.38-12.54-70.21-10.13-75.56,5.4-5.35,15.52,19.8,38.28,56.17,50.82Zm-31.12-42.18c2.42-7.02,22.65-6.4,45.19,1.37,22.54,7.77,38.85,19.76,36.43,26.78-2.42,7.02-22.65,6.41-45.19-1.37-22.54-7.77-38.85-19.76-36.43-26.78Z'/%3E%3Cpath class='d' d='M176.67,82.65c13.47,.35,26.52,2.95,39.31,7.07,14.94,4.81,29.06,11.28,41.81,20.53,1.87,1.35,1.87,1.35,2.94-.45,9.98-16.73,19.94-33.47,29.94-50.18,2.07-3.47,4.07-6.91,4-11.14-.09-5.63-2.23-10.53-5.3-15.07-6.1-9.03-14.47-15.51-23.87-20.68C252.61,5.63,238.81,1.28,224.07,.22c-8.97-.65-17.82-.01-26.27,3.36-5.62,2.24-10.44,5.5-13.08,11.26-1.21,2.65-1.29,5.51-1.64,8.32-.89,7.01-1.75,14.03-2.62,21.04l-2.05,16.68c-.94,7-1.87,14.01-2.81,21.01-.13,.96,.55,.73,1.08,.74Z'/%3E%3C/g%3E%3Cpath class='d' d='M30.76,177.58c4.4,0,8.04-1.49,10.92-4.49,2.88-2.99,4.32-6.63,4.32-10.92,0-3.73-1.16-6.77-3.47-9.14-2.32-2.37-5.39-3.56-9.23-3.56-4.4,0-8.04,1.47-10.92,4.4-2.88,2.94-4.32,6.66-4.32,11.18,0,3.61,1.19,6.6,3.56,8.98,2.37,2.37,5.42,3.56,9.14,3.56Z'/%3E%3Cpath class='d' d='M39.65,190.79c-.51-.56-1.27-.85-2.29-.85H17.72c-1.81,0-2.82,.85-3.05,2.54L.11,274.78c-.23,.9-.08,1.67,.42,2.29,.51,.62,1.21,.93,2.12,.93H22.29c1.8,0,2.88-.9,3.22-2.71l14.56-82.3c.23-.9,.08-1.64-.42-2.2Z'/%3E%3Cpath class='d' d='M88.39,187.57c-5.42,0-11.15,.62-17.19,1.86-6.04,1.24-11.77,2.88-17.19,4.91-1.35,.57-2.2,1.58-2.54,3.05l-13.89,77.39c-.23,.9-.08,1.67,.42,2.29,.51,.62,1.27,.93,2.29,.93h19.64c1.8,0,2.88-.9,3.22-2.71l11.18-63.5c2.93-1.35,6.55-2.03,10.84-2.03,7.45,0,11.18,3.5,11.18,10.5,0,1.47-.17,3.16-.51,5.08l-8.47,49.45c-.11,.9,.08,1.67,.59,2.29,.51,.62,1.21,.93,2.12,.93h19.47c1.8,0,2.88-.9,3.22-2.71l8.47-47.42c.56-3.61,.85-6.72,.85-9.31,0-9.59-2.91-17.16-8.72-22.69-5.82-5.53-14.14-8.3-24.98-8.3Z'/%3E%3Cpath class='d' d='M210.72,191.8c0-1.24-.85-1.86-2.54-1.86h-21c-1.58,0-2.77,.74-3.56,2.2l-16.09,36.75c-2.15,5.08-3.95,9.6-5.42,13.55-.9,1.92-2.15,4.91-3.73,8.98h-.34c-.57-7.79-1.24-15.24-2.03-22.35l-4.06-36.41c-.11-1.8-1.13-2.71-3.05-2.71h-19.64c-1.92,0-2.88,.9-2.88,2.71v.34l13.04,82.3c.11,1.81,1.19,2.71,3.22,2.71h22.35c1.58,0,2.71-.73,3.39-2.2l41.83-82.47c.34-.56,.51-1.07,.51-1.52Z'/%3E%3Cpath class='d' d='M276.78,194.68c-6.1-4.74-14.17-7.11-24.22-7.11-10.73,0-19.96,2.77-27.69,8.3-7.73,5.53-12.56,13.61-14.48,24.22l-4.4,24.55c-.45,3.16-.68,5.36-.68,6.6,0,8.92,3.19,15.98,9.57,21.17,6.38,5.19,14.65,7.79,24.81,7.79,13.55,0,25.34-3.44,35.39-10.33,.9-.45,1.35-1.24,1.35-2.37,0-.23-.11-.79-.34-1.69l-6.94-13.04c-.45-1.02-1.13-1.52-2.03-1.52-.68,0-1.3,.23-1.86,.68-7.56,4.52-14.9,6.77-22.01,6.77-8.02,0-12.02-3.22-12.02-9.65,0-.68,.11-1.92,.34-3.73l.51-2.37h47.08c1.69,0,2.71-.85,3.05-2.54l2.88-16.43c.56-3.39,.85-6.15,.85-8.3,0-9.26-3.05-16.26-9.14-21Zm-16.09,27.09l-.85,4.23h-24.72l.85-4.57c.79-3.95,2.46-7,5-9.14,2.54-2.14,5.67-3.22,9.4-3.22,3.5,0,6.15,.9,7.96,2.71,1.8,1.81,2.71,4.18,2.71,7.11,0,.57-.11,1.52-.34,2.88Z'/%3E%3Cpath class='d' d='M336.94,187.57c-5.42,0-11.15,.62-17.19,1.86-6.04,1.24-11.77,2.88-17.19,4.91-1.35,.57-2.2,1.58-2.54,3.05l-13.89,77.39c-.23,.9-.08,1.67,.42,2.29,.51,.62,1.27,.93,2.29,.93h19.64c1.8,0,2.88-.9,3.22-2.71l11.18-63.5c2.93-1.35,6.55-2.03,10.84-2.03,7.45,0,11.18,3.5,11.18,10.5,0,1.47-.17,3.16-.51,5.08l-8.47,49.45c-.11,.9,.08,1.67,.59,2.29,.51,.62,1.21,.93,2.12,.93h19.47c1.8,0,2.88-.9,3.22-2.71l8.47-47.42c.56-3.61,.85-6.72,.85-9.31,0-9.59-2.91-17.16-8.72-22.69-5.82-5.53-14.14-8.3-24.98-8.3Z'/%3E%3Cpath class='d' d='M427.68,192.9c-.51-.62-1.27-.93-2.29-.93l-17.16,.2,4.63-20.35c.11-.9-.08-1.64-.59-2.2-.51-.56-1.27-.85-2.29-.85h-16.6c-1.81,0-2.88,.9-3.22,2.71l-12.7,72.65c-.57,2.82-.85,6.04-.85,9.65,0,8.69,2.46,15.27,7.37,19.73,4.91,4.46,11.54,6.69,19.9,6.69,2.93,0,5.81-.28,8.64-.85,1.58-.11,2.54-1.07,2.88-2.88l2.71-15.75c.45-1.92-.28-2.88-2.2-2.88h-5.08c-5.76,0-8.64-2.71-8.64-8.13,0-.79,.11-1.97,.34-3.56l5.76-32.68h13.89c1.8,0,2.88-.9,3.22-2.71l2.71-15.58c.22-.9,.08-1.66-.42-2.29Z'/%3E%3C/g%3E%3C/g%3E%3C/g%3E%3C/svg%3E"  # noqa


class Image(Widget):
    """
    Represents an image to display on the user interface.
    """

    image = TextProperty(
        _("The path to the image media."),
        default_value=_DEFAULT_IMAGE,
    )

    width = TextProperty(
        _("The width of the image."),
        default_value=None,
        group="style",
    )

    height = TextProperty(
        _("The height of the image."),
        default_value=None,
        group="style",
    )

    touch = Event(
        _("Sent when the image is touched."),
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M216 40H40a16 16 0 0 0-16 16v144a16 16 0 0 0 16 16h176a16 16 0 0 0 16-16V56a16 16 0 0 0-16-16m0 16v102.75l-26.07-26.06a16 16 0 0 0-22.63 0l-20 20l-44-44a16 16 0 0 0-22.62 0L40 149.37V56ZM40 172l52-52l80 80H40Zm176 28h-21.37l-36-36l20-20L216 181.38zm-72-100a12 12 0 1 1 12 12a12 12 0 0 1-12-12"/></svg>'  # noqa

    def on_image_changed(self):
        self.element.src = self.image

    def on_width_changed(self):
        if self.width is not None:
            self.element.style["width"] = self.width
        else:
            self.element.style.remove("width")

    def on_height_changed(self):
        if self.height is not None:
            self.element.style["height"] = self.height
        else:
            self.element.style.remove("height")

    def touch_handler(self, event):
        self.publish("touch")

    def render(self):
        element = img(src=self.image, id=self.id)
        element.addEventListener("click", self.touch_handler)
        return element
