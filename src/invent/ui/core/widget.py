"""
The base widget class that defines common aspects of components drawn onto the
user interface via the Invent framework.

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

import invent
from invent.i18n import _
from .component import Component
from ..containers import Column, Row
from .property import ChoiceProperty, TextProperty
from .measures import COMPONENT_DISTRIBUTION


class Widget(Component):
    """
    A widget is a UI component drawn onto the interface in some way.

    All widgets have these things:

    * A unique human friendly name that's meaningful in the context of the
      application (if none is given, one is automatically generated).
    * A unique id (if none is given, one is automatically generated).
    * A render function that takes the widget's container and renders
      itself as an HTML element into the container.
    * An optional indication of the channel[s] to which it broadcasts
      messages (defaults to the id).
    * A publish method that takes the name of a message blueprint, and
      associated kwargs, and publishes it to the channel[s] set for the
      widget.
    """

    channel = TextProperty(
        _(
            "A comma separated list of channels to which the widget broadcasts."
        ),
        default_value=None,
    )

    horizontal_align = ChoiceProperty(
        _("The horizontal alignment of the widget."),
        choices=COMPONENT_DISTRIBUTION,
    )

    vertical_align = ChoiceProperty(
        _("The vertical alignment of the widget."),
        choices=COMPONENT_DISTRIBUTION,
    )

    def _on_new_parent(self):
        """
        When a widget is added to a new parent, set the alignment properties
        of the widget (which depend on the type of containing parent).
        """
        self.on_horizontal_align_changed()
        self.on_vertical_align_changed()

    def on_horizontal_align_changed(self):
        """
        Set the horizontal alignment of the widget.
        """
        if isinstance(self.parent, Column):
            self.element.style["align-self"] = self.horizontal_align
        elif isinstance(self.parent, Row):
            self.element.style["justify-self"] = self.horizontal_align

    def on_vertical_align_changed(self):
        """
        Set the vertical alignment of the widget.
        """
        if isinstance(self.parent, Row):
            self.element.style["align-self"] = self.vertical_align
        elif isinstance(self.parent, Column):
            self.element.style["justify-self"] = self.vertical_align

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.channel is None:
            self.channel = self.id

    def publish(self, event_name, **kwargs):
        """
        Given the name of one of the class's defined events, publish a message
        to all the widget's channels with the message content defined in kwargs.
        """
        # Ensure self.channel is treated as a comma-separated list of channel
        # names.
        if self.channel is not None:
            channels = [
                channel.strip()
                for channel in self.channel.split(",")
                if channel.strip()
            ]
            message = getattr(self, event_name).create_message(
                event_name, **kwargs
            )
            invent.publish(message, to_channel=channels)

    def when(self, subject, to_channel=None, do=None):
        """
        Convenience method for wrapping subscriptions.

        If no "do" handler is given, we assume this function is decorating the
        handler to "do" the stuff.

        The subject and to_channel can be either individual strings or a
        list of strings to indicate the channel[s] and message subject[s] to
        match.
        """
        if not to_channel:
            to_channel = self.id

        if do:
            invent.subscribe(
                handler=do, to_channel=to_channel, when_subject=subject
            )
        else:

            def inner_function(handler):
                invent.subscribe(
                    handler=handler,
                    to_channel=to_channel,
                    when_subject=subject,
                )

            return inner_function
