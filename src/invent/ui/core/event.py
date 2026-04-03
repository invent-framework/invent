"""
The core Event class for defining events in the life-cycle of a component in
the Invent framework. The Event class allows component authors to define the
structure and content of messages that will be sent when an event is triggered,
and to validate the content of those messages when they're created.

This ensures that messages sent by components are consistent and conform to
the expected structure, which can be useful for tooling and for other
components that subscribe to those messages.

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

    ```python
    click = Event("Sent when the widget it clicked.")
    hold = Event(
        "The button is held down.",
        duration="The amount of time the button was held down.",
    )
    double_click = Event()
    ```

    Instances may have an optional description to explain their intent, and
    key/value pairs describing the fields in the content of the resulting
    message. This metadata is used to validate the content of the message and
    could be used in associated tooling.

    The create_message method is used to create a message representing the
    event being triggered, with the content specified as kwargs. The resulting
    message's subject is the name of the event. The source is added to the
    message as the "source" field. The content of the message is validated
    against the content specification defined in the Event instance, and an
    error is raised if the content does not match the specification.

    An event is fired by creating a message using the create_message method
    and then publishing it to a channel. The publish method of the component
    can be used to easily publish the message to the appropriate channel[s].

    E.g. the following example shows how to fire the "hold" event defined above
    with a duration of 5 seconds:

    ```python
    # Somewhere in the button widget's code, when the hold event is triggered:
    self.publish(self.hold, duration=5)
    ```
    """

    def __init__(self, description=None, **kwargs):
        """
        Events may have an optional description and key/value pairs
        describing the expected content of future messages sent when the event
        is triggered.
        """
        self.description = description
        self.content = kwargs
        # Set via __set_name__ when assigned in a class.
        self._event_name = None
    
    def __set_name__(self, owner, name):
        """
        Helper via the descriptor protocol: provides the name against
        which to store the event instance.
        """
        self._event_name = name

    def create_message(self, source, **kwargs):
        """
        Returns a message representing an event triggered by a source with the
        given content (kwargs). The message's subject is the name of the event.
        The message can then be published to a channel to indicate the event
        has occurred.

        Validates kwargs match the fields described in the event's content
        specification. The source is added to the message as the "source"
        field.
        """
        for k in kwargs:
            if k not in self.content:
                raise ValueError(
                    _("Unknown field in event {event}: ").format(
                        event=self._event_name
                    )
                    + k
                )
        for k in self.content:
            if k not in kwargs:
                raise ValueError(
                    _("Field missing from event {event}:").format(
                        event=self._event_name
                    )
                    + k
                )
        kwargs["source"] = source
        return invent.Message(self._event_name, **kwargs)

    def as_dict(self):
        """
        Return a dictionary representation of the meta-data contained within
        this class.
        """
        return {
            "description": self.description,
            "content": self.content,
        }
