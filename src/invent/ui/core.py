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

import invent
import inspect
from pyscript import document
from invent.i18n import _
from .utils import random_id


#: Valid flags for horizontal positions.
_VALID_HORIZONTALS = {"LEFT", "CENTER", "RIGHT"}
#: Valid flags for vertical positions.
_VALID_VERTICALS = {"TOP", "MIDDLE", "BOTTOM"}


class ValidationError(ValueError):
    """
    Raised when a component's property is set to an invalid value.
    """

    ...


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


class from_datastore:
    """
    Instances of this class signal that a property is bound to a datastore
    value.

    Implementation detail: snake case is used for this class, rather than the
    orthodox capitalised camel case, for aesthetic reasons. ;-)
    """

    def __init__(self, key):
        """
        The key identifies the value in the datastore.
        """
        self.key = key


class Property:
    """
    An instance of a child of this class represents a property of a Widget.

    This class implements the Python descriptor protocol. See:

    https://docs.python.org/3/howto/descriptor.html

    Using a Property class allows easier introspection and dynamic handling of
    properties in a way that works with MicroPython.

    Every property must have a human meaningful description of what it
    represents for the widget, an optional default value and optional flag to
    indicate if it is a required property.
    """

    _property_counter = 0

    def __init__(self, description, default_value=None, required=False):
        """
        All properties must have a description. They may have a default value
        and flag indicating if it is a required property.
        """
        self.description = description
        self.required = required
        self.default_value = self.validate(default_value)

    def __set_name__(self, owner, name):
        """
        Helps with the descriptor protocol, as it provides a name against
        which to store the descriptor's value.
        """
        self.private_name = "_" + name

    def __get__(self, obj, objtype=None):
        """
        Descriptor method to return the value associated with the property.
        """
        return getattr(obj, self.private_name, self.default_value)

    def __set__(self, obj, value):
        """
        Descriptor method to set and validate the value to be associated with
        the property.

        If the value is from_datastore, then a reactor function is defined to
        handle when the referenced value in the datastore changes. The reactor
        function ensures the widget is updated (i.e. appears reactive) when
        the associated value is updated.
        """

        if isinstance(value, from_datastore):

            def reactor(message, key=value.key):  # pragma: no cover
                """
                Set the value in the widget and call the optional
                "on_FOO_changed" to ensure the update is visible to the user.
                """
                valid_value = self.validate(message.value)
                setattr(obj, self.private_name, valid_value)
                # If the change handler exists on the object, call it to update
                # the widget.
                change_fn = "on" + self.private_name + "_changed"
                on_changed = getattr(obj, change_fn, None)
                if on_changed:
                    on_changed()

            # Subscribe to store events for the specified key.
            invent.subscribe(
                reactor, to_channel="store-data", when_subject=value.key
            )
            # Update value to the actual value from the datastore.
            value = invent.datastore.get(value.key, self.default_value)
        # Set the value in the widget.
        setattr(obj, self.private_name, self.validate(value))

    def coerce(self, value):
        """
        Return value as an acceptable type (or raise an exception while doing
        so).
        """
        return value  # pragma: no cover

    def validate(self, value):
        """
        Validate the incoming value of the property.
        """
        value = self.coerce(value)
        if self.required and value is None:
            raise ValidationError(_("This property is required."))
        return value

    def as_dict(self):
        """
        Return a Python dictionary as a data structure representing all the
        essential information about the property.
        """
        return {
            "property_type": self.__class__.__name__,
            "description": self.description,
            "required": self.required,
            "default_value": self.default_value,
        }


class NumericProperty(Property):
    """
    A numeric property, with an optional maximum and minimum, for a Widget.
    """

    def __init__(
        self,
        description,
        default_value=None,
        required=False,
        minimum=None,
        maximum=None,
    ):
        """
        In addition to the Property related attributes, the min and max
        define the bounds of a valid value. If set to None, these won't be
        checked during validation.
        """
        self.minimum = minimum
        self.maximum = maximum
        super().__init__(description, default_value, required)

    def validate(self, value):
        """
        The value must be a number (None is allowed if the property is not
        required).

        If set, the value must be between the minimum and maximum boundaries.
        """
        value = super().validate(value)
        if not (value is None or isinstance(value, (int, float))):
            raise ValidationError(_("The value must be a number."))
        if value is not None:
            if self.minimum and value < self.minimum:
                raise ValidationError(
                    _("The value is less than the minimum allowed."),
                    value,
                    self.minimum,
                )
            if self.maximum and value > self.maximum:
                raise ValidationError(
                    _("The value is greater than the maximum."),
                    value,
                    self.maximum,
                )
        return value

    def as_dict(self):
        """
        Return a Python dictionary as a data structure representing all the
        essential information about the property.
        """
        result = super().as_dict()
        result["minimum"] = self.minimum
        result["maximum"] = self.maximum
        return result


class IntegerProperty(NumericProperty):
    """
    An integer (whole number) property for a Widget.
    """

    def validate(self, value):
        """
        Ensure the property's value is an integer.
        """
        if isinstance(value, int):
            return super().validate(value)
        raise ValidationError(
            _("The value must be an integer (whole number).")
        )


class FloatProperty(NumericProperty):
    """
    A floating point (a number with a decimal point) property for a Widget.
    """

    def validate(self, value):
        """
        Ensure the property's value is a floating point number.
        """
        if isinstance(value, float):
            return super().validate(value)
        raise ValidationError(
            _("The value must be a float (a number with a decimal point).")
        )


class TextProperty(Property):
    """
    A textual property for a Widget.
    """

    def __init__(
        self,
        description,
        default_value=None,
        required=False,
        min_length=None,
        max_length=None,
    ):
        """
        In addition to the Property related attributes, the min_length and
        max_length define the bounds of the length of a valid value. If set to
        None, these won't be checked during validation.
        """
        self.min_length = min_length
        self.max_length = max_length
        super().__init__(description, default_value, required)

    def coerce(self, value):
        """
        Coerce to a string.
        """
        return str(value)

    def validate(self, value):
        """
        The value must be a string (or None if not a required property).

        If set, the value must be between the minimum and maximum boundaries.
        """
        value = super().validate(value)
        if value is not None and not isinstance(value, str):
            raise ValidationError(_("The value must be a string:") + value)
        if value is not None:
            length = len(value)
            if self.min_length and length < self.min_length:
                raise ValidationError(
                    _("The length of the value is less than minimum allowed.")
                )
            if self.max_length and length > self.max_length:
                raise ValidationError(
                    _("The length of the value is more than maximum allowed.")
                )
        return value

    def as_dict(self):
        """
        Return a Python dictionary as a data structure representing all the
        essential information about the property.
        """
        result = super().as_dict()
        result["min_length"] = self.min_length
        result["max_length"] = self.max_length
        return result


class BooleanProperty(Property):
    """
    A boolean (True/False) flag property for a Widget.
    """

    def validate(self, value):
        """
        Ensure the property's value is a boolean value (True / False).
        """
        if isinstance(value, bool) or value is None:
            return super().validate(value)
        raise ValidationError(
            _("The value must be a boolean (True or False).")
        )


class ChoiceProperty(Property):
    """
    A property for a Widget whose value can only be from a pre-determined set
    of choices.
    """

    def __init__(
        self, description, choices, default_value=None, required=False
    ):
        """
        In addition to the Property related attributes, the choices enumerate
        a set of valid values.
        """
        self.choices = choices
        super().__init__(description, default_value, required)

    def validate(self, value):
        """
        Ensure the property's value is in the set of valid choices.
        """
        if value in self.choices or value is None:
            return super().validate(value)
        raise ValidationError(_("The value must be one of the valid choices."))

    def as_dict(self):
        """
        Return a Python dictionary as a data structure representing all the
        essential information about the property.
        """
        result = super().as_dict()
        result["choices"] = self.choices
        return result


class Component:
    """
    A base class for all user interface components (Widget, Container).

    Ensures they all have optional names and ids. If they're not given, will
    auto-generate them for the user.
    """

    _object_counter = 0

    name = TextProperty(
        "The meaningful name of the widget instance.",
    )
    id = TextProperty("The id of the widget instance in the DOM.")

    def __init__(self, name=None, id=None, position="FILL"):
        if invent.is_micropython:
            for name, prop in type(self).properties().items():
                prop.__set_name__(self, name)
        # TODO: automagically grab values from kwargs and inflate properties,
        # then call self.render to create self.element.
        # Then set the element's id to self.id
        # Then call self.update() to do the on_<FOO>_changed calls.
        self.name = name if name else type(self)._generate_name()
        self.id = id if id else random_id()
        self.position = position

    @classmethod
    def _generate_name(cls):
        cls._object_counter += 1
        return f"{cls.__name__} {cls._object_counter}"

    def render(self, container):
        raise NotImplementedError()  # pragma: no cover

    @classmethod
    def preview(cls):
        raise NotImplementedError()  # pragma: no cover

    @classmethod
    def properties(cls):
        """
        Returns a dictionary of properties associated with the component. The
        key is the property name, the value an instance of the relevant
        property class.

        Implementation detail: we branch on interpreter type because of the
        different behaviour of `getmembers`.
        """
        if invent.is_micropython:  # pragma: no cover
            result = {}
            for name, member in inspect.getmembers(cls):
                value = getattr(cls, name)
                if isinstance(value, Property):
                    result[name] = value
            return result
        return {
            name: value
            for name, value in inspect.getmembers_static(cls)
            if isinstance(value, Property)
        }

    @classmethod
    def message_blueprints(cls):
        """
        Returns a dictionary of the message blueprints that define the sort of
        messages a component may send during its lifetime.

        Implementation detail: we branch on interpreter type because of the
        different behaviour of `getmembers`.
        """
        if invent.is_micropython:  # pragma: no cover
            result = {}
            for name, member in inspect.getmembers(cls):
                value = getattr(cls, name)
                if isinstance(value, MessageBlueprint):
                    result[name] = value
            return result
        return {
            name: value
            for name, value in inspect.getmembers_static(cls)
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
            "properties": {
                name: prop.as_dict() for name, prop in cls.properties().items()
            },
            "message_blueprints": {
                key: value for key, value in cls.message_blueprints().items()
            },
            "preview": cls.preview(),
        }

    def as_dict(self):
        """
        Return a dict representation of the state of this component's
        properties and message blueprints.
        """
        properties = {
            key: getattr(self, key) for key in type(self).properties()
        }
        return {
            "type": type(self).__name__,
            "properties": properties,
            "message_blueprints": {
                key: value
                for key, value in type(self).message_blueprints().items()
            },
        }

    def parse_position(self):
        """
        Parse the self.position as: "VERTICAL-HORIZONTAL", "VERTICAL" or
        "HORIZONTAL" values.

        Valid values are defined in _VALID_VERTICALS and _VALID_HORIZONTALS.

        Returns a tuple of (vertical_position, horizontal_position). Each
        return value could be None.
        """
        definition = self.position.upper().split("-")
        # Default values for the horizontal and vertical positions.
        horizontal_position = None
        vertical_position = None
        if len(definition) == 1:
            # Unary position (e.g. "TOP" or "CENTER")
            unary_position = definition[0]
            if unary_position in _VALID_HORIZONTALS:
                horizontal_position = unary_position
            elif unary_position in _VALID_VERTICALS:
                vertical_position = unary_position
        elif len(definition) == 2:
            # Binary position (e.g. "TOP-CENTER" or "BOTTOM-RIGHT")
            if definition[0] in _VALID_VERTICALS:
                vertical_position = definition[0]
            if definition[1] in _VALID_HORIZONTALS:
                horizontal_position = definition[1]
        if not (horizontal_position or vertical_position):
            # Bail out if we don't have a valid position state.
            raise ValueError(f"'{self.position}' is not a valid position.")
        return (vertical_position, horizontal_position)

    def set_position(self, container):
        """
        Given the value of self.position, will adjust the CSS for the rendered
        self.element, and its container, so the resulting HTML puts the element
        into the expected position in the container.
        """
        if self.position.upper() == "FILL":
            # Fill the full extent of the container.
            self.element.style.width = "100%"
            self.element.style.height = "100%"
            return
        # Parse into horizontal and vertical positions.
        vertical_position, horizontal_position = self.parse_position()
        # Check vertical position and adjust the container via CSS magic.
        if vertical_position == "TOP":
            container.style.setProperty("align-self", "start")
        elif vertical_position == "MIDDLE":
            container.style.setProperty("align-self", "center")
        elif vertical_position == "BOTTOM":
            container.style.setProperty("align-self", "end")
        # Check the horizontal position and adjust the container.
        if horizontal_position == "LEFT":
            container.style.setProperty("justify-self", "start")
        elif horizontal_position == "CENTER":
            container.style.setProperty("justify-self", "center")
        elif horizontal_position == "RIGHT":
            container.style.setProperty("justify-self", "end")
        # Ensure a vertical only position ensures a full horizontal fill.
        if not horizontal_position:
            container.style.setProperty("justify-self", "stretch")
            self.element.style.width = "100%"
        # Ensure a horizontal only position ensures a full vertical fill.
        if not vertical_position:
            container.style.setProperty("align-self", "stretch")
            self.element.style.height = "100%"


class Widget(Component):
    """
    All widgets have these things:

    * A unique human friendly name that's meaningful in the context of the
      application (if none is given, one is automatically generated).
    * A unique id (if none is given, one is automatically generated).
    * An indication of the widget's preferred position (default: top left).
    * A render function that takes the widget's container and renders
      itself as an HTML element into the container.
    * An optional channel name to which it broadcasts its messages (defaults to
      the id).
    """

    channel = TextProperty("The channel[s] to which the widget broadcasts.")
    position = TextProperty("The widget's preferred position.")

    def __init__(self, name=None, id=None, position="TOP-LEFT", channel=None):
        super().__init__(name, id, position)
        self.channel = channel if channel else self.id
        # Reference to the HTML element (once rendered).
        self.element = None

    def publish(self, blueprint, **kwargs):
        """
        Given the name of one of the class's MessageBlueprints, publish the
        a message to all the widget's channels with the message content
        defined in kwargs.
        """
        message = getattr(self, blueprint).create_message(blueprint, **kwargs)
        invent.publish(message, to_channel=self.channel)


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

    width = IntegerProperty(
        "The default width of the container.",
        default_value=100,
        maximum=100,
        minimum=0,
    )
    height = IntegerProperty(
        "The default height of the container.",
        default_value=100,
        maximum=100,
        minimum=0,
    )
    background_color = TextProperty("The color of the container's background.")
    border_color = TextProperty("The color of the container's border.")
    border_width = ChoiceProperty(
        "The size of the container's border.",
        choices=[None, "XS", "S", "M", "L", "XL"],
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

    def __init__(
        self,
        name=None,
        id=None,
        content=None,
        position="FILL",
        width=100,
        height=100,
        background_color=None,
        border_color=None,
        border_width=None,
        border_style=None,
    ):
        super().__init__(name, id, position)
        # An ordered list of child components.
        self.content = content or []
        # To reference the container's parent in the DOM tree.
        self.parent = None
        # Component property settings.
        self.width = width
        self.height = height
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_style = border_style
        self.render()

    def append(self, item):
        """
        Append like a list.
        """
        item.parent = self
        self.content.append(item)

    def __getitem__(self, index):
        """
        Index items like a list.
        """
        return self.content[index]

    def __iter__(self):
        """
        Iterate like a list.
        """
        return iter(self.content)

    def __delete__(self, item):
        """
        Delete like a list.
        """
        del self.content[item]

    def render(self):
        """
        Return a div element representing the container (set with the expected
        height and width).

        Sub classes should call this, then override with the specific details
        for how to add their children in a way that reflects the way they
        layout their widgets.
        """
        self.element = document.createElement("div")
        self.element.id = self.id
        self.element.style.display = "grid"
        # TODO: Make these dynamic from on_FOO_updated.
        if self.height:
            self.element.style.height = f"{self.height}%"
        if self.width:
            self.element.style.width = f"{self.width}%"
        if self.background_color:
            self.element.style.setProperty(
                "background-color", self.background_color
            )
        if self.border_color:
            self.element.style.setProperty(
                "border-color", self.border_color
            )
        if self.border_width:
            self.element.style.setProperty(
                "border-width", self.border_width
            )
        if self.border_style:
            self.element.style.setProperty(
                "border-style", self.border_style
            )
        # TODO: Add children via sub-class.
        return self.element

    def as_dict(self):
        """
        Return a dict representation of the container, including the ordered
        content of children.
        """
        result = super().as_dict()
        result["content"] = [child.as_dict for child in self.content]


class Column(Container):
    """
    A vertical container box.
    """

    def render(self):
        super().render()
        for counter, child in enumerate(self.content, start=1):
            child_container = document.createElement("div")
            child_container.style.setProperty("grid-column", 1)
            child_container.style.setProperty("grid-row", counter)
            child_container.appendChild(child.element)
            child.set_position(child_container)
            self.element.appendChild(child_container)
        return self.element


class Row(Container):
    """
    A horizontal container box.
    """

    def render(self):
        super().render()
        for counter, child in enumerate(self.content, start=1):
            child_container = document.createElement("div")
            child_container.style.setProperty("grid-column", counter)
            child_container.style.setProperty("grid-row", 1)
            child_container.appendChild(child.element)
            child.set_position(child_container)
            self.element.appendChild(child_container)
        return self.element
