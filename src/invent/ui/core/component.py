"""
Core classes relating to the user interface aspects of the Invent framework.

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

from pyscript import document

import invent
from invent.compatability import capitalize, getmembers_static
from invent.i18n import _
from .model import Model
from .property import (
    BooleanProperty,
    ChoiceProperty,
    ListProperty,
    TextProperty,
)


ALIGNMENTS = ["start", "center", "end"]
ALIGNMENTS_STRETCH = ALIGNMENTS + ["stretch"]


def align_self_property(direction):
    return ChoiceProperty(
        f"{capitalize(direction)} alignment.",
        choices=ALIGNMENTS_STRETCH,
        default_value="stretch",
        map_to_style="align-self",
    )


#: T-shirt sizes used to indicate relative sizes of things.
_TSHIRT_SIZES = (
    None,
    "XS",
    "S",
    "M",
    "L",
    "XL",
)
#: The default icon for a component. https://github.com/phosphor-icons/core
_DEFAULT_ICON = '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M140 180a12 12 0 1 1-12-12a12 12 0 0 1 12 12M128 72c-22.06 0-40 16.15-40 36v4a8 8 0 0 0 16 0v-4c0-11 10.77-20 24-20s24 9 24 20s-10.77 20-24 20a8 8 0 0 0-8 8v8a8 8 0 0 0 16 0v-.72c18.24-3.35 32-17.9 32-35.28c0-19.85-17.94-36-40-36m104 56A104 104 0 1 1 128 24a104.11 104.11 0 0 1 104 104m-16 0a88 88 0 1 0-88 88a88.1 88.1 0 0 0 88-88"/></svg>'  # noqa


class MessageBlueprint:
    """
    An instance of this class represents a type of message potentially
    triggered in the life-cycle of a Widget object. The name assigned in the
    parent class definition should become the message's subject (an
    implementation detail left to the author of the Widget class).

    E.g.:

    click = MessageBlueprint("Sent when the widget it clicked.")
    hold = MessageBlueprint(
        "The button is held down.",
        duration="The amount of time the button was held down.",
    )
    double_click = MessageBlueprint()

    Instances may have an optional description to explain their intent, and
    key/value pairs describing the fields in the content of the message. This
    metadata is used in the visual builder.
    """

    def __init__(self, description=None, **kwargs):
        """
        Messages may have an optional description and key/value pairs
        describing the expected content of future messages.
        """
        self.description = description
        self.content = kwargs

    def create_message(self, name, **kwargs):
        """
        Returns an actual message to send to channels with the given content.

        Validates kwargs match the fields described in the blueprint's content
        specification.
        """
        for k in kwargs:
            if k not in self.content:
                raise ValueError(_("Unknown field in message content: ") + k)
        for k in self.content:
            if k not in kwargs:
                raise ValueError(_("Field missing from message content:") + k)
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


class Component(Model):
    """
    A base class for all user interface components (Widget, Container).

    Ensures they all have optional names and ids. If they're not given, will
    auto-generate them for the user.
    """

    # Used for quick component look-up.
    _components_by_id = {}
    # Used for generating unique component names.
    _component_counter = 0

    id = TextProperty("The id of the widget instance in the DOM.")
    name = TextProperty(
        "The meaningful name of the widget instance.",
        map_to_attribute="name",
    )
    enabled = BooleanProperty(
        "Indicates if the component is enabled.", default_value=True
    )
    visible = BooleanProperty(
        "The component is visible is set to True.", default_value=True
    )

    def __init__(self, **kwargs):
        if invent.is_micropython:  # pragma: no cover
            # When in MicroPython, ensure all the properties have a reference
            # to their name within this class.
            for property_name, property_obj in type(self).properties().items():
                property_obj.__set_name__(self, property_name)
        self.element = self.render()
        self._parent = None
        self._layout = {}
        super().__init__(**kwargs)

        type(self)._component_counter += 1
        if not self.id:
            self.id = type(self)._generate_unique_id()
        if not self.name:
            self.name = type(self)._generate_name()
        Component._components_by_id[self.id] = self

    @property
    def is_container(self):
        """
        Return True if this component is a container, otherwise False.

        Just a convenience property in place of "isinstance".
        """
        return isinstance(self, Container)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        old_parent = self._parent
        self._parent = parent

        if parent:
            # Validate the layout against the new parent.
            try:
                self.layout = self.layout
            except Exception:
                self._parent = old_parent
                raise

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, layout):
        def type_error():
            raise TypeError(
                f"container type {type(self.parent).__name__} "
                + f"doesn't support layout type {type(layout).__name__}"
            )

        if isinstance(layout, Layout):
            if self.parent:
                if type(layout) is self.parent.layout_class:
                    # Create a new Layout object for this component, and copy
                    # all properties.
                    self._layout = self.parent.layout_class(
                        self,
                        **{
                            key: getattr(layout, key)
                            for key, prop in layout.properties().items()
                        },
                    )
                else:
                    type_error()
            else:
                # Validate it later, when we have a parent.
                self._layout = layout

        elif isinstance(layout, dict):
            if self.parent:
                self._layout = self.parent.layout_class(self, **layout)
            else:
                # Validate it later, when we have a parent.
                self._layout = layout

        else:
            type_error()

    def on_id_changed(self):
        """
        Automatically called to update the id of the HTML element associated
        with the component.
        """
        self.element.id = self.id

    def on_enabled_changed(self):
        """
        Ensure the underlying HTML element is enabled/disabled according to
        the value of the property.
        """
        self.element.disabled = not self.enabled

    def on_visible_changed(self):
        """
        Show / hide the element depending on the value of the property.
        """
        self.element.style.visibility = "visible" if self.visible else "hidden"

    @classmethod
    def _generate_unique_id(cls):
        """
        Create a unique but meaningful id for the component.

        E.g.

        "invent-button-1"

        The pattern is "invent-classname-counter".
        """
        return f"invent-{cls.__name__.lower()}-{cls._component_counter}"

    @classmethod
    def _generate_name(cls):
        """
        Create a human friendly name for the component.

        E.g.

        "Button 1"
        """
        return f"{cls.__name__} {cls._component_counter}"

    @classmethod
    def get_component_by_id(cls, component_id):
        """
        Return the component with the specified id or None if no such
        component exists.
        """
        return Component._components_by_id.get(component_id)

    def render(self):
        """
        In base classes, return the HTML element used to display the
        component.
        """
        raise NotImplementedError()  # pragma: no cover

    @classmethod
    def icon(cls):
        """
        Return the SVG to display in the menu of available components in the
        UI builder.
        """
        return _DEFAULT_ICON

    @classmethod
    def message_blueprints(cls):
        """
        Returns a dictionary of the message blueprints that define the sort of
        messages a component may send during its lifetime.

        Implementation detail: we branch on interpreter type because of the
        different behaviour of `getmembers`.
        """
        return {
            name: value
            for name, value in getmembers_static(cls)
            if isinstance(value, MessageBlueprint)
        }

    @classmethod
    def blueprint(cls):
        """
        Return a Python dictionary as a data structure representing all the
        essential information about the components, its properties, message
        blueprints and preview.
        """
        return {
            "name": cls.__name__,
            "properties": {
                name: prop.as_dict() for name, prop in cls.properties().items()
            },
            "message_blueprints": {
                key: value.as_dict()
                for key, value in cls.message_blueprints().items()
            },
            "icon": cls.icon(),
        }

    def as_dict(self):
        """
        Return a dict representation of the state of this instance.
        """
        properties = super().as_dict()
        layout_dict = (
            self.layout
            if isinstance(self.layout, dict)
            else self.layout.as_dict()
        )
        if layout_dict:
            properties["layout"] = layout_dict

        # If the component is a Container, we format its content recursively.
        if isinstance(self, Container):
            if not self.get_from_datastore("children"):
                properties["children"] = [
                    item.as_dict() for item in self.children
                ]

        return {
            "type": type(self).__name__,
            "properties": properties,
        }

    def update_attribute(self, attribute_name, attribute_value):
        """
        Convenience method to update an HTML attribute on self.element. If
        the attribute_value is false-y, the attribute is removed.
        Otherwise, the named attribute is set to the given value.
        """
        if attribute_value:
            self.element.setAttribute(attribute_name, str(attribute_value))
        else:
            self.element.removeAttribute(attribute_name)


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
        "A comma separated list of channels to which the widget broadcasts.",
        default_value=None,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.channel is None:
            self.channel = self.id

    def publish(self, blueprint, **kwargs):
        """
        Given the name of one of the class's MessageBlueprints, publish
        a message to all the widget's channels with the message content
        defined in kwargs.
        """
        # Ensure self.channel is treated as a comma-separated list of channel
        # names.
        if self.channel is not None:
            channels = [
                channel.strip()
                for channel in self.channel.split(",")
                if channel.strip()
            ]
            message = getattr(self, blueprint).create_message(
                blueprint, **kwargs
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


class Container(Component):
    """
    All containers have these things:

    * A unique human friendly name that's meaningful in the context of the
      application (if none is given, one is automatically generated).
    * A unique id (if none is given, one is automatically generated).
    * Is a list of children (that are either widgets or further containers).
    * A notion of relative width/height to the containing element (defaults
      100%).
    * A render function that returns an HTML element representing the
      container to insert into the DOM. Child classes override this method to
      insert the children into the container in the correct manner.
    """

    children = ListProperty(
        "The contents of the container",
        default_value=None,
    )

    background_color = TextProperty("The color of the container's background.")
    border_color = TextProperty("The color of the container's border.")
    border_width = ChoiceProperty(
        "The size of the container's border.",
        choices=_TSHIRT_SIZES,
    )
    border_style = ChoiceProperty(
        "The style of the container's border.",
        choices=[
            None,
            "Dotted",
            "Dashed",
            "Solid",
            "Double",
            "Groove",
            "Ridge",
            "Inset",
            "Outset",
        ],
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for item in self.children:
            item.parent = self

    def on_children_changed(self):
        self.element.innerHTML = ""
        for child in self.children:
            self.element.appendChild(child.element)
        self.update_children()

    def on_background_color_changed(self):
        if self.background_color:
            self.element.style.setProperty(
                "background-color", self.background_color
            )
        else:
            self.element.style.removeProperty("background-color")

    def on_border_color_changed(self):
        if self.border_color:
            self.element.style.setProperty("border-color", self.border_color)
        else:
            self.element.style.removeProperty("border-color")

    def on_border_width_changed(self):
        """
        Set the border with (transliating from t-shirt sizes).
        """
        sizes = {
            "XS": "2px",
            "S": "4px",
            "M": "8px",
            "L": "16px",
            "XL": "32px",
        }
        if self.border_width is not None:
            size = sizes[self.border_width.upper()]
            self.element.style.setProperty("border-width", size)
        else:
            self.element.style.removeProperty("border-width")

    def on_border_style_changed(self):
        if self.border_style:
            self.element.style.setProperty("border-style", self.border_style)
        else:
            self.element.style.removeProperty("border-style")

    def _set_gap(self, gap, attr):
        sizes = {
            "XS": "2px",
            "S": "4px",
            "M": "8px",
            "L": "16px",
            "XL": "32px",
        }
        size = "0px"

        if gap is not None:
            size = sizes[gap.upper()]
        self.element.style.setProperty(attr, size)

    def append(self, item):
        """
        Append like a list.
        """
        # Update the object model.
        item.parent = self
        self.children.append(item)

        # Update the DOM.
        self.element.appendChild(item.element)

        # Update the grid indices of the container's children.
        self.update_children()

    def insert(self, index, item):
        """
        Insert like a list.
        """
        # Update the object model.
        item.parent = self
        self.children.insert(index, item)

        # Update the DOM.
        if item is self.children[-1]:
            self.element.appendChild(item.element)
        else:
            self.element.insertBefore(
                item.element, self.element.childNodes[index]
            )

        # Update the grid indices of the container's children.
        self.update_children()

    def remove(self, item):
        """
        Remove like a list.
        """
        # Update the object model.
        item.parent = None
        self.children.remove(item)

        # Update the DOM.
        item.element.remove()

        # Update the grid indices of the container's children.
        self.update_children()

    def __getitem__(self, index):
        """
        Index items like a list.
        """
        return self.children[index]

    def __iter__(self):
        """
        Iterate like a list.
        """
        return iter(self.children)

    def __delitem__(self, item):
        """
        Delete like a list.
        """
        self.remove(item)

    def contains(self, component):
        """Return True if the specified component is in this container.

        This is recursive, so this really means "is a descendant of".
        """
        for item in self.children:
            if item is component:
                return True

            if item.is_container:
                if item.contains(component):
                    return True

        return False

    def render(self):
        """
        Return a div element representing the container.

        Subclasses should call this, then override with the specific details
        for how to add their children in a way that reflects the way they
        lay out their widgets.
        """
        element = document.createElement("div")
        element.classList.add(f"invent-{type(self).__name__.lower()}")
        return element

    def update_children(self):
        """
        Update the container's children.
        """
        for counter, child in enumerate(self.children, start=1):
            self.update_child(child, counter)

    def update_child(self, child, index):
        pass


class Layout(Model):
    def __init__(self, component, **kwargs):
        self.component = component
        self.element = self.component.element
        super().__init__(**kwargs)
