"""
An avatar is a visual representation of a user or entity. Avatars are commonly
used in social media, forums, and other online communities to help users
identify each other and personalize their online experience. They can also be
used in applications to represent users in chat interfaces, comments sections,
and other interactive elements. Avatars can be circular, rounded or square.

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

from pyscript import web

from invent.i18n import _
from invent.ui.core.measures import TSHIRT_SIZES, MEDIUM
from invent.ui.core import (
    Widget,
    TextProperty,
    ChoiceProperty,
    Event,
)
from pyscript.web import figure, img
from pyscript.ffi import create_proxy

_DEFAULT_AVATAR_IMAGE = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23585858' viewBox='0 0 256 256'%3E%3Cpath d='M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216ZM80,108a12,12,0,1,1,12,12A12,12,0,0,1,80,108Zm96,0a12,12,0,1,1-12-12A12,12,0,0,1,176,108Zm-1.07,48c-10.29,17.79-27.4,28-46.93,28s-36.63-10.2-46.92-28a8,8,0,1,1,13.84-8c7.47,12.91,19.21,20,33.08,20s25.61-7.1,33.07-20a8,8,0,0,1,13.86,8Z'%3E%3C/path%3E%3C/svg%3E%0A"  # noqa


class Avatar(Widget):
    """
    An avatar is a visual representation of a user or entity. Avatars are commonly
    used in social media, forums, and other online communities to help users
    identify each other and personalize their online experience. They can also be
    used in applications to represent users in chat interfaces, comments sections,
    and other interactive elements. Avatars can be circular, rounded or square.
    """

    image = TextProperty(
        _("The URL of the avatar image."), default_value=_DEFAULT_AVATAR_IMAGE
    )
    shape = ChoiceProperty(
        _("The shape of the avatar."),
        default_value="CIRCLE",
        choices=["CIRCLE", "ROUNDED", "SQUARE"],
        group="style",
    )
    size = ChoiceProperty(
        _("The size of the avatar."),
        default_value=MEDIUM,
        choices=TSHIRT_SIZES,
        group="style",
    )
    name = TextProperty(
        _("The name of the person or entity represented by the avatar."),
        default_value=None,
    )
    press = Event(_("Sent when the avatar is pressed."))

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216ZM80,108a12,12,0,1,1,12,12A12,12,0,0,1,80,108Zm96,0a12,12,0,1,1-12-12A12,12,0,0,1,176,108Zm-1.07,48c-10.29,17.79-27.4,28-46.93,28s-36.63-10.2-46.92-28a8,8,0,1,1,13.84-8c7.47,12.91,19.21,20,33.08,20s25.61-7.1,33.07-20a8,8,0,0,1,13.86,8Z"></path></svg>'  # noqa

    def click(self, event):
        self.publish(self.press)

    def render(self):
        """
        Build and return the root element for the avatar widget.

        The element is an <img> wrapped in a <figure>. The figure
        carries shape and size modifier classes and the click listener.
        """
        avatar = img()
        avatar.src = self.image if self.image else ""
        avatar.alt = self.name if self.name else ""
        avatar.title = self.name if self.name else ""
        fig = figure(avatar)
        fig.classes.add("invent-avatar")
        fig.classes.add(f"invent-avatar--{self.shape.lower()}")
        fig.classes.add(f"invent-avatar--{self.size.lower()}")
        fig.addEventListener("click", create_proxy(self.click))
        return fig

    def on_image_changed(self):
        """
        Update the src attribute on the <img> element.
        """
        self.element.find("img")[0].src = self.image if self.image else ""

    def on_name_changed(self):
        """
        Update the alt text and hover tooltip on the <img> element.
        """
        img = self.element.find("img")[0]
        name = self.name if self.name else ""
        img.alt = name
        img.title = name

    def on_shape_changed(self):
        """
        Swap the shape modifier class on the root figure.
        """
        for shape in ("circle", "rounded", "square"):
            self.element.classes.remove(f"invent-avatar--{shape}")
        self.element.classes.add(f"invent-avatar--{self.shape.lower()}")

    def on_size_changed(self):
        """
        Swap the size modifier class on the root figure.
        """
        for size in (s.lower() for s in TSHIRT_SIZES if s is not None):
            self.element.classes.remove(f"invent-avatar--{size}")
        self.element.classes.add(f"invent-avatar--{self.size.lower()}")
