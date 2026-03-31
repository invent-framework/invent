"""
The core Event class for defining events in the life-cycle of a component in
the Invent framework.

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

import invent
from invent.i18n import _


class Event:
    """
    An instance of this class represents an event in the life-cycle of a
    component, expressed in the form of a message. The name assigned to the
    instance of the Event in the component's class definition is the event's
    name and will become the resulting message's subject (an implementation
    detail left to the author of the related component class).

    E.g. the following example defines three events called "click", "hold" and
    "double_click" that occur in the life-cycle of a component (such as a
    button widget):

    click = Event("Sent when the widget it clicked.")
    hold = Event(
        "The button is held down.",
        duration="The amount of time the button was held down.",
    )
    double_click = Event()

    Instances may have an optional description to explain their intent, and
    key/value pairs describing the fields in the content of the resultng
    message. This metadata could be used in associated tooling.
    """

    def __init__(self, description=None, **kwargs):
        """
        Events may have an optional description and key/value pairs
        describing the expected content of future messages sent when the event
        is triggered.
        """
        self.description = description
        self.content = kwargs

    def create_message(self, widget, name, **kwargs):
        """
        Returns a message representing an event triggered by a widget with the
        given content (kwargs). The message's subject is the name of the event.
        The message can then be published to a channel to indicate the event
        has occurred.

        Validates kwargs match the fields described in the event's content
        specification. The source widget is added to the message as the
        "widget" field.
        """
        for k in kwargs:
            if k not in self.content:
                raise ValueError(
                    _("Unknown field in event {event}: ").format(event=name)
                    + k
                )
        for k in self.content:
            if k not in kwargs:
                raise ValueError(
                    _("Field missing from event {event}:").format(event=name)
                    + k
                )
        kwargs["widget"] = widget
        return invent.Message(name, **kwargs)

    def as_dict(self):
        """
        Return a dictionary representation of the meta-data contained within
        this class.
        """
        return {
            "description": self.description,
            "content": self.content,
        }
