"""
A widget for displaying arbitrary content that requires a related title,
timestamp and/or image/icon for the Invent framework.

Works well with the `Timeline` container - which is a column for
displaying time-based data. For use as a social media feed or an
ordered list of events or items such as in an RSS reader or catalogue.

This widget can also be used stand-alone to display a single piece of
content with a timestamp, title, image/icon and body of text. For
example, an entry in an address book or call out for a specific purpose.

The look and layout of the ContentCard can be modified. The background
colour and border can be changed. The shape can be rounded or square.
The widget alignment can be set to left, right or centre. The image,
timestamp, and title can be hidden.

```
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
```
"""

from invent.i18n import _
from ..containers.column import Column
from pyscript.ffi import create_proxy
from pyscript.web import article, header, img, h3, time, footer, div
from invent.ui.core import (
    Widget,
    TextProperty,
    DatetimeProperty,
    ChoiceProperty,
    Event,
)
from invent.ui.core.measures import PURPOSES
from invent.utils import humanise_timestamp

CARD_SHAPES = [
    "rounded",  # Rounded corners.
    "square",  # Square corners.
]

IMAGE_POSITIONS = [
    "avatar",  # The image is displayed as a circular avatar.
    "banner",  # The image is displayed as a full-width banner.
]

PUBLISH_POSITIONS = [
    "start",  # The timestamp appears in the card header.
    "end",  # The timestamp appears in the card footer.
]


class ContentCard(Widget):
    """
    A ContentCard widget for the Invent framework.

    Displays arbitrary content alongside an optional title, image/icon
    and publication timestamp. Append child widgets as you would with
    any container widget.
    """

    def __init__(self, **kwargs):
        self.children = Column()
        if "children" in kwargs:
            for item in kwargs.pop("children"):
                self.children.append(item)
        super().__init__(**kwargs)

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><path fill="currentColor" d="M200 112a8 8 0 0 1-8 8h-40a8 8 0 0 1 0-16h40a8 8 0 0 1 8 8m-8 24h-40a8 8 0 0 0 0 16h40a8 8 0 0 0 0-16m40-80v144a16 16 0 0 1-16 16H40a16 16 0 0 1-16-16V56a16 16 0 0 1 16-16h176a16 16 0 0 1 16 16m-16 144V56H40v144zm-80.26-34a8 8 0 1 1-15.5 4c-2.63-10.26-13.06-18-24.25-18s-21.61 7.74-24.25 18a8 8 0 1 1-15.5-4a39.84 39.84 0 0 1 17.19-23.34a32 32 0 1 1 45.12 0a39.76 39.76 0 0 1 17.2 23.34ZM96 136a16 16 0 1 0-16-16a16 16 0 0 0 96 16"/></svg>'  # noqa

    published_at = DatetimeProperty(
        _("The publication date and time relating to the content."),
        default_value=None,
    )

    image = TextProperty(
        _("The image/icon associated with the content."),
        default_value=None,
    )

    title = TextProperty(
        _("The title related to the content."),
        default_value=None,
    )

    shape = ChoiceProperty(
        _("The shape of the content card."),
        choices=CARD_SHAPES,
        default_value="rounded",
        group="style",
    )

    image_position = ChoiceProperty(
        _("The position of the image on the content card."),
        choices=IMAGE_POSITIONS,
        default_value="avatar",
        group="style",
    )

    publish_position = ChoiceProperty(
        _("The position of the publication timestamp" " on the content card."),
        choices=PUBLISH_POSITIONS,
        default_value="start",
        group="style",
    )

    purpose = ChoiceProperty(
        _("The card's purpose."),
        default_value="DEFAULT",
        choices=PURPOSES,
        group="style",
    )

    pressed = Event(_("Sent when the card is pressed."))

    def click(self, event):
        """
        Publish a press event when the card is clicked.
        """
        self.publish(self.pressed)

    def render(self):
        """
        Build and return the card's DOM skeleton. References to all
        mutable sub-elements are stored on self so that property-change
        handlers can update them directly, without ever rebuilding the
        skeleton.
        """
        card = article(
            style={
                "--card-border-color": f"var(--primary)",
            }
        )
        card.classes.add("invent-card")
        if self.shape == "square":
            card.classes.add("square")
        if self.publish_position == "end":
            card.classes.add("publish-end")
        if self.image_position == "banner":
            card.classes.add("banner-image")
        # Banner: full-width image above the header.
        # CSS hides this element unless the banner-image class is set.
        self._banner = img()
        self._banner.setAttribute("src", self.image or "")
        self._banner.setAttribute("alt", self.title or "")
        card.append(self._banner)
        # Header: avatar, title and optional start-position timestamp.
        self._header = header()
        self._avatar = img()
        self._avatar.setAttribute("src", self.image or "")
        self._avatar.setAttribute("alt", self.title or "")
        self._header.append(self._avatar)
        # Meta div: groups the title and header timestamp as a flex
        # column beside the avatar.
        meta = div()
        self._h3 = h3()
        self._h3.textContent = self.title or ""
        meta.append(self._h3)
        # Shared timestamp values used by both time elements.
        dt = self.published_at.isoformat() if self.published_at else ""
        label = (
            humanise_timestamp(self.published_at) if self.published_at else ""
        )
        self._header_time = time()
        self._header_time.setAttribute("datetime", dt)
        self._header_time.textContent = label
        meta.append(self._header_time)
        self._header.append(meta)
        card.append(self._header)
        # Body: holds the column of child widgets.
        card.append(self.children.element)
        # Footer: end-position timestamp.
        # CSS hides the footer unless the publish-end class is set.
        self._footer_time = time()
        self._footer_time.setAttribute("datetime", dt)
        self._footer_time.textContent = label
        ftr = footer()
        ftr.append(self._footer_time)
        card.append(ftr)
        card.addEventListener("click", create_proxy(self.click))
        self._update_header_visibility()
        return card

    def _update_header_visibility(self):
        """
        Show the header only when it has at least one visible item:
        an avatar image, a title, or a start-position timestamp.
        """
        visible = (
            bool(self.image and self.image_position == "avatar")
            or bool(self.title)
            or bool(self.published_at and self.publish_position == "start")
        )
        self._header.style.display = "" if visible else "none"

    def on_title_changed(self):
        """
        Update the heading text and both image alt attributes.
        """
        self._h3.textContent = self.title or ""
        for im in (self._banner, self._avatar):
            im.setAttribute("alt", self.title or "")
        self._update_header_visibility()

    def on_image_changed(self):
        """
        Update the src attribute on both image elements.
        """
        for im in (self._banner, self._avatar):
            im.setAttribute("src", self.image or "")
        self._update_header_visibility()

    def on_image_position_changed(self):
        """
        Switch between avatar and banner image display modes.
        """
        if self.image_position == "banner":
            self.element.classes.add("banner-image")
        else:
            self.element.classes.remove("banner-image")
        self._update_header_visibility()

    def on_published_at_changed(self):
        """
        Update both timestamp elements with the new date/time.
        """
        dt = self.published_at.isoformat() if self.published_at else ""
        label = (
            humanise_timestamp(self.published_at) if self.published_at else ""
        )
        for ts in (self._header_time, self._footer_time):
            ts.setAttribute("datetime", dt)
            ts.textContent = label
        self._update_header_visibility()

    def on_publish_position_changed(self):
        """
        Switch the timestamp between header and footer positions.
        """
        if self.publish_position == "end":
            self.element.classes.add("publish-end")
        else:
            self.element.classes.remove("publish-end")
        self._update_header_visibility()

    def on_shape_changed(self):
        """
        Toggle square-corner styling on the card.
        """
        if self.shape == "square":
            self.element.classes.add("square")
        else:
            self.element.classes.remove("square")

    def on_purpose_changed(self):
        """
        Update the card's colour-scheme CSS variables.
        """
        if self.purpose == "DEFAULT":
            self.element.style.pop("--card-bg", None)
            self.element.style["--card-border-color"] = "var(--primary)"
        else:
            p = self.purpose.lower()
            self.element.style["--card-bg"] = f"var(--{p}-light)"
            self.element.style["--card-border-color"] = f"var(--{p})"
