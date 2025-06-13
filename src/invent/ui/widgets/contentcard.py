"""
A widget for displaying arbitrary content that requires a related title,
timestamp and/or image/icon for the Invent framework.

Works well with the `Timeline` container - which is a column for displaying
time-based data. For use as a social media feed or an ordered list of events
such as in a chat app.

This widget could also be used "stand alone" to display a single piece of
content with a timestamp, title, image/icon and body of text. For example, an
entry in an address book or catalogue.

The look and layout of the ContentCard can be modified. The background colour
and border can be changed. The shape can be rounded, square or speech. The
widget alignment can be set to left, right or center. The image, timestamp, and
title can be hidden.

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
from invent.utils import from_markdown
from pyscript.web import div, img, h3, span


from invent.ui.core import (
    Widget,
    TextProperty,
    DatetimeProperty,
    ChoiceProperty,
    BooleanProperty,
)


CARD_SHAPES = [
    "rounded",  # Rounded corners.
    "square",  # Square corners.
    "speech",  # Speech bubble.
]


SPEECH_BUBBLE_ALIGNMENTS = [
    "left",
    "right",
]


class ContentCard(Widget):
    """
    A ContentCard widget for the Invent framework.
    """

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><path fill="currentColor" d="M200 112a8 8 0 0 1-8 8h-40a8 8 0 0 1 0-16h40a8 8 0 0 1 8 8m-8 24h-40a8 8 0 0 0 0 16h40a8 8 0 0 0 0-16m40-80v144a16 16 0 0 1-16 16H40a16 16 0 0 1-16-16V56a16 16 0 0 1 16-16h176a16 16 0 0 1 16 16m-16 144V56H40v144zm-80.26-34a8 8 0 1 1-15.5 4c-2.63-10.26-13.06-18-24.25-18s-21.61 7.74-24.25 18a8 8 0 1 1-15.5-4a39.84 39.84 0 0 1 17.19-23.34a32 32 0 1 1 45.12 0a39.76 39.76 0 0 1 17.2 23.34ZM96 136a16 16 0 1 0-16-16a16 16 0 0 0 16 16"/></svg>'  # noqa

    published_at = DatetimeProperty(
        _("The publication date and time relating to the content."),
        default_value=None,
    )

    image = TextProperty(
        _("The image/icon associated with the content."),
        default_value="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNTYiIGhlaWdodD0iMjU2IiB2aWV3Qm94PSIwIDAgMjU2IDI1NiI+PHBhdGggZmlsbD0iY3VycmVudENvbG9yIiBkPSJNMjA4IDMySDQ4YTE2IDE2IDAgMCAwLTE2IDE2djE2MGExNiAxNiAwIDAgMCAxNiAxNmgxNjBhMTYgMTYgMCAwIDAgMTYtMTZWNDhhMTYgMTYgMCAwIDAtMTYtMTZNNDggMjA4VjU5LjMxTDE5Ni42OSAyMDhaTTU5LjMxIDQ4SDIwOHYxNDguN1oiLz48L3N2Zz4=",  # noqa
    )

    title = TextProperty(_("The title of the content."), default_value="")

    body = TextProperty(
        _("The textual (markdown) body of the content."),
        required=True,
    )

    shape = ChoiceProperty(
        _("The shape of the content card."),
        values=CARD_SHAPES,
        default_value="rounded",
        group="style",
    )

    speech_align = ChoiceProperty(
        _("The optional speech bubble alignment of the content card."),
        values=SPEECH_BUBBLE_ALIGNMENTS,
        default_value=None,
        group="style",
    )

    hide_image = BooleanProperty(
        _("Hide the image associated with the content card."),
        default_value=False,
        group="layout",
    )

    hide_date = BooleanProperty(
        _("Hide the datetime associated with the content card."),
        default_value=False,
        group="layout",
    )

    hide_title = BooleanProperty(
        _("Hide the title of the content card."),
        default_value=False,
        group="layout",
    )

    def on_shape_changed(self):
        """
        Update the CSS class of the card when the shape changes to reflect the
        new shape. The class name is of the form `contentcard-{shape}`.
        """
        for shape in CARD_SHAPES:
            self.element.classes.remove(f"contentcard-{shape}")
        self.element.classes.add(f"contentcard-{self.shape}")

    def on_speech_align_changed(self):
        """
        Update the CSS class of the card when the speech_align property changes
        to reflect the new alignment. The class name is of the form
        `contentcard-speech-{alignment}`.
        """
        for alignment in SPEECH_BUBBLE_ALIGNMENTS:
            self.element.classes.remove(f"contentcard-speech-{alignment}")
        if self.speech_align:
            self.element.classes.add(f"contentcard-speech-{self.speech_align}")

    def on_date_changed(self):
        """
        Update the timestamp of the card when the date changes.
        """
        self.datetime_element.text = str(self.published_at)

    def on_image_changed(self):
        """
        Update the image of the card when the image changes.
        """
        self.image_element.src = self.image

    def on_title_changed(self):
        """
        Update the title of the card when the title changes.
        """
        self.title_element.text = self.title

    def on_body_changed(self):
        """
        Update the body of the card when the body changes.
        """
        self.body_element.innerHTML = from_markdown(self.body)

    def on_hide_image_changed(self):
        """
        Update the visibility of the image when the hide_image property changes.
        """
        if self.hide_icon:
            self.image_element.style["display"] = "none"
        else:
            self.image_element.style["display"] = "block"

    def on_hide_date_changed(self):
        """
        Update the visibility of the timestamp when the hide_date property
        changes.
        """
        if self.hide_date:
            self.datetime_element.style["display"] = "none"
        else:
            self.datetime_element.style["display"] = "block"

    def on_hide_title_changed(self):
        """
        Update the visibility of the title when the hide_title property changes.
        """
        if self.hide_title:
            self.title_element.style["display"] = "none"
        else:
            self.title_element.style["display"] = "block"

    def render(self):
        """
        Render the card to the DOM.
        """
        self.image_element = img(src=self.image)
        self.image_element.classes.add("contentcard-image")
        self.title_element = h3(self.title)
        self.title_element.classes.add("contentcard-title")
        self.datetime_element = span(str(self.published_at))
        self.datetime_element.classes.add("contentcard-date")
        self.body_element = div()
        self.body_element.classes.add("contentcard-body")
        return div(
            self.image_element,
            self.title_element,
            self.datetime_element,
            self.body_element,
            id=self.id,
        )
