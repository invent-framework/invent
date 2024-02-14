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
from pyscript import document
from invent.i18n import _
from .utils import random_id


#: Valid flags for horizontal positions.
_VALID_HORIZONTALS = {"LEFT", "CENTER", "RIGHT"}
#: Valid flags for vertical positions.
_VALID_VERTICALS = {"TOP", "MIDDLE", "BOTTOM"}


class ValidationError(ValueError):
    """
    Raised when a widget's property is set to an invalid value.
    """

    ...


class Event:
    """
    An instance of this class represents an event triggered in the life-cycle
    of a Widget.
    """

    def __init__(self, name, **kwargs):
        """
        An event has a name.
        """
        ...  # TODO: Finish me.


class from_datastore:
    """
    Instances of this class signal that a widget property is bound to a
    datastore value.
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
        if not hasattr(self, "private_name"):
            self.private_name = (
                f"_{self.__class__.__name__.lower()}{self._property_counter}"
            )
            self._property_counter += 1
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
        """
        if isinstance(value, from_datastore):

            def reactor(message, key=value.key):
                if message._subject == key:
                    setattr(
                        obj, self.private_name, self.validate(message.value)
                    )
                    obj.render()

            invent.subscribe(reactor, to_channel="store-data", when=value.key)
            value = invent.datastore.get(value.key)
        setattr(obj, self.private_name, self.validate(value))

    def validate(self, value):
        """
        Validate the incoming value of the property.
        """
        if self.required and value is None:
            raise ValidationError(_("This property is required."))
        return value

    def as_dict(self, value):
        """
        Return a Python dictionary as a data structure representing all the
        essential information about the property.
        """
        return {
            "property_type": self.__class__.__name__,
            "description": self.description,
            "required": self.required,
            "value": value,
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
        return super().validate(value)

    def as_dict(self, value):
        """
        Return a Python dictionary as a data structure representing all the
        essential information about the property.
        """
        result = super().as_dict(value)
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

    def validate(self, value):
        """
        The value must be a string (or None if not a required property).

        If set, the value must be between the minimum and maximum boundaries.
        """
        if not (value is None or isinstance(value, str)):
            raise ValidationError(_("The value must be a string."))
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
        return super().validate(value)

    def as_dict(self, value):
        """
        Return a Python dictionary as a data structure representing all the
        essential information about the property.
        """
        result = super().as_dict(value)
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

    def as_dict(self, value):
        """
        Return a Python dictionary as a data structure representing all the
        essential information about the property.
        """
        result = super().as_dict(value)
        result["choices"] = self.choices
        return result


class Widget:
    """
    All widgets have these things:

    * A mandatory unique human friendly name that's meaningful in the context
      of the application.
    * A unique id (if none is given, one is automatically generated).
    * An indication of the widget's preferred position (default: top left).
    * A render_into function that takes the widget's container and renders
      itself as an HTML element into the container.
    * An optional channel name to which it broadcasts its messages (defaults to
      the id)
    """

    def __init__(self, name, id=None, position="TOP-LEFT", channel=None):
        self.name = name
        self.id = id if id else random_id()
        self.channel = channel if channel else self.id
        self.position = position
        # Reference to the HTML element (once rendered).
        self.element = None

    def render_into(self, container):
        raise NotImplementedError()  # pragma: no cover

    @property
    def properties(self):
        """
        Returns a dictionary of properties associated with the widget. The key
        is the property name, the value an instance of the relevant property
        class.
        """
        return {
            k: v
            for k, v in self.__class__.__dict__.items()
            if isinstance(v, Property)
        }

    def as_dict(self):
        """
        Return a Python dictionary as a data structure representing all the
        essential information about the widget and its properties.
        """
        result = {
            "name": self.name,
            "id": self.id,
            "channel": self.channel,
            "position": self.position,
            "properties": {},
        }
        for name, prop in self.properties.items():
            result["properties"][name] = prop.as_dict(getattr(self, name))
        return result

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
        horizontal_position, vertical_position = self.parse_position()
        # Check vertical position and adjust the container via CSS magic.
        if vertical_position == "TOP":
            container.style["align-self"] = "start"
        elif vertical_position == "MIDDLE":
            container.style["align-self"] = "center"
        elif vertical_position == "BOTTOM":
            container.style["align-self"] = "end"
        # Check the horizontal position and adjust the container.
        if horizontal_position == "LEFT":
            container.style["justify-self"] = "start"
        elif horizontal_position == "CENTER":
            container.style["justify-self"] = "center"
        elif horizontal_position == "RIGHT":
            container.style["justify-self"] = "end"
        # Ensure a vertical only position ensures a full horizontal fill.
        if not horizontal_position:
            container.style["justify-self"] = "stretch"
            self.element.style.width = "100%"
        # Ensure a horizontal only position ensures a full vertical fill.
        if not vertical_position:
            container.style["align-self"] = "stretch"
            self.element.style.height = "100%"


class Container(list):
    """
    All containers have these things:

    * A mandatory unique human friendly name that's meaningful in the context
      of the application.
    * A unique id (if none is given, one is automatically generated).
    * Is a list of children (that are either widgets or further containers).
    * A notion of relative width/height to the containing element (defaults
      100%).
    * A render function that returns an HTML element representing the
      container to insert into the DOM. Child classes override this method to
      insert the children into the container in the correct manner.
    """

    def __init__(
        self,
        name,
        id=None,
        children=None,
        width=100,
        height=100,
        background_color=None,
        border_color=None,
        border_width=None,
        border_style=None,
    ):
        self.name = name
        # To reference the div in the DOM that renders this container.
        self._container = None
        self.id = id if id else random_id()
        self.parent = None
        self.width = width
        self.height = height
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_style = border_style

    def append(self, item):
        item.parent = self
        super().append(item)

    def render(self):
        """
        Return a div element representing the container (set with the expected
        height and width).

        Sub classes should call this, then override with the specific details
        for how to add their children in a way that reflects the way they
        layout their widgets.
        """
        if not self._container:
            self._container = document.createElement("div")
            self._container.id = self.id
            self._container.style.display = "grid"
        self._container.style.height = f"{self.height}%"
        self._container.style.width = f"{self.width}%"
        self._container.style["background-color"] = self.background_color
        self._container.style["border-color"] = self.border_color
        self._container.style["border-width"] = self.border_width
        self._container.style["border-style"] = self.border_style
        # TODO: Add children via sub-class.
        return self._container


class Column(Container):
    """
    A vertical container box.
    """

    def render(self):
        super().render()
        for counter, child in enumerate(self, start=1):
            child_container = document.createElement("div")
            child_container.style["grid-column"] = 1
            child_container.style["grid-row"] = counter
            child.render_into(child_container)
            self._container.appendChild(child_container)
        return self._container


class Row(Container):
    """
    A horizontal container box.
    """

    def render(self):
        super().render()
        for counter, child in enumerate(self, start=1):
            child_container = document.createElement("div")
            child_container.style["grid-column"] = counter
            child_container.style["grid-row"] = 1
            child.render_into(child_container)
            self._container.appendChild(child_container)
        return self._container
