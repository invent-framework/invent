"""
A chat bubble is used to show one line of conversation and all its data,
including the author image, author name, time, etc.

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

from datetime import datetime
from invent.i18n import _
from invent.utils import from_markdown, contrast_colours, humanise_timestamp
from invent.ui.core import (
    Widget,
    TextProperty,
    Event,
    DatetimeProperty,
    ChoiceProperty,
)
from pyscript import web


_DEFAULT_AUTHOR_IMAGE = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23585858' viewBox='0 0 256 256'%3E%3Cpath d='M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216ZM80,108a12,12,0,1,1,12,12A12,12,0,0,1,80,108Zm96,0a12,12,0,1,1-12-12A12,12,0,0,1,176,108Zm-1.07,48c-10.29,17.79-27.4,28-46.93,28s-36.63-10.2-46.92-28a8,8,0,1,1,13.84-8c7.47,12.91,19.21,20,33.08,20s25.61-7.1,33.07-20a8,8,0,0,1,13.86,8Z'%3E%3C/path%3E%3C/svg%3E%0A"  # noqa


class ChatBubble(Widget):
    """
    A chat bubble is used to show a contribution to a conversation along
    with all its data, including the author image, author name, time, etc.

    The ChatBubble is useful for displaying a conversation in a chat-like
    interface. The ChatBubble can be used to show messages from different
    authors, with different styles and content.
    """

    author_name = TextProperty(
        _("The name of the author of the message."), default_value=None
    )
    author_image = TextProperty(
        _("The URL of the author's image."),
        default_value=_DEFAULT_AUTHOR_IMAGE,
    )
    timestamp = DatetimeProperty(
        _("The time when the message was sent."), default_value=None
    )
    shade = TextProperty(
        _("The colour of the chat bubble as a CSS colour string."),
        default_value=None,
    )
    content = TextProperty(_("The content of the message."), min_length=1)
    direction = ChoiceProperty(
        _(
            "The direction of broadcast. Sent or received. "
            "Determines the alignment of the chat bubble."
        ),
        choices=["sent", "received"],
        default_value="sent",
    )

    clicked = Event(
        _("An event that is fired when the chat bubble is clicked."),
        author_name=str,
        author_image=str,
        timestamp=datetime,
        content=str,
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="#currentColor" viewBox="0 0 256 256"><path d="M216,48H40A16,16,0,0,0,24,64V224a15.85,15.85,0,0,0,9.24,14.5A16.13,16.13,0,0,0,40,240a15.89,15.89,0,0,0,10.25-3.78l.09-.07L83,208H216a16,16,0,0,0,16-16V64A16,16,0,0,0,216,48ZM40,224h0ZM216,192H80a8,8,0,0,0-5.23,1.95L40,224V64H216ZM88,112a8,8,0,0,1,8-8h64a8,8,0,0,1,0,16H96A8,8,0,0,1,88,112Zm0,32a8,8,0,0,1,8-8h64a8,8,0,1,1,0,16H96A8,8,0,0,1,88,144Z"></path></svg>'  # noqa

    def update_bubble(self):
        """
        Update the chat bubble element with the appropriate classes and content.
        """
        if not self.content:
            return  # Don't render an empty bubble
        self.element.replaceChildren()  # Clear existing content
        self.element.classes.clear()  # Clear existing classes
        self.element.classes.add("invent-bubble")
        self.element.classes.add(self.direction)
        if self.shade:
            # Compute contrast colours for text and links based on the
            # user-defined bubble background.
            colours = contrast_colours(self.shade)
            self.element.style["--bubble-bg"] = self.shade
            self.element.style["--bubble-text"] = colours["text"]
            self.element.style["--bubble-link"] = colours["link"]
        if self.author_image:
            image = web.img(
                src=self.author_image,
                alt=self.author_name,
                width="40",
                height="40",
            )
            self.element.append(image)
        bubble_body = web.div(classes=["invent-bubble-body"])
        if self.author_name:
            header = web.header(web.strong(self.author_name))
            bubble_body.append(header)
        content = web.div()
        content.innerHTML = from_markdown(self.content)
        bubble_body.append(content)
        if self.timestamp:
            footer = web.footer()
            time = web.time(humanise_timestamp(self.timestamp))
            time.setAttribute("datetime", self.timestamp.isoformat())
            footer.append(time)
            bubble_body.append(footer)
        self.element.append(bubble_body)

    on_author_name_changed = update_bubble
    on_author_image_changed = update_bubble
    on_timestamp_changed = update_bubble
    on_content_changed = update_bubble
    on_direction_changed = update_bubble
    on_shade_changed = update_bubble

    def render(self):
        """
        Render the chat bubble as a div with the appropriate classes and content.
        """
        element = web.div(classes=["invent-bubble"])
        element.addEventListener(
            "click",
            lambda event: self.publish(
                "clicked",
                author_name=self.author_name,
                author_image=self.author_image,
                timestamp=self.timestamp,
                content=self.content,
            ),
        )
        return element
