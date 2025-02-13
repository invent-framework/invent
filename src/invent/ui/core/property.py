"""
The core Property class and its children, used for defining the properties of
UI components in the Invent framework.

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

import datetime
import json
import invent
from invent.i18n import _


class ValidationError(ValueError):
    """
    Raised when a component's property is set to an invalid value.
    """

    ...


class from_datastore:  # NOQA
    """
    Instances of this class signal that a property is bound to a datastore
    value identified by the key.

    If a with_function is provided, it is called when the value in the
    datastore changes. The function is passed the new value from the datastore
    and should return the value to be set on the property.

    Implementation detail: snake case is used for this class, rather than the
    orthodox capitalised camel case, for aesthetic reasons. ;-)
    """

    def __init__(self, key, with_function=None):
        """
        The key identifies the value in the datastore. The with_function, if
        supplied, is called when the value in the datastore changes.
        """
        self.key = key
        self.with_function = with_function

    def __repr__(self):
        """
        Create the expression for a property that gets its value from the
        datastore. Used for serialiszation purposes.
        """
        expression = f"from_datastore({self.key!r}"
        if self.with_function:
            expression += f", with_function={self.with_function.__name__}"
        expression += ")"

        return expression


class Property:
    """
    An instance of a child of this class represents a property of a Widget. Do
    not use this class directly. Instead, use one of its children.

    This class implements the Python descriptor protocol. See:

    https://docs.python.org/3/howto/descriptor.html

    Using a Property class allows easier introspection and dynamic handling of
    properties in a way that works with MicroPython.
    """

    _property_counter = 0

    def __init__(
        self,
        description,
        default_value=None,
        required=False,
        map_to_attribute=None,
        map_to_style=None,
        group=None,
    ):
        """
        All properties must have a description. They may have a default value,
        a flag indicating if it is a required property and an indication of the
        HTML or CSS attribute of the parent object's element to which to map
        its value. The optional group attribute should be a string and is used
        to group properties together into meaningful categories (for example,
        "layout" or "style") used by external tooling to create Invent
        applications.
        """
        self.description = description
        self.required = required
        self.default_value = self.validate(default_value)
        self.map_to_attribute = map_to_attribute
        self.map_to_style = map_to_style
        self.group = group

    def __set_name__(self, owner, name):
        """
        Helps with the descriptor protocol, as it provides a name against
        which to store the descriptor's value.
        """
        self.name = name
        self.private_name = f"_{name}"
        self.from_datastore_name = f"_{name}_from_datastore"

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

        # If this property has already been bound to the datastore then we need
        # to set the value *in* the datastore. This will then trigger the
        # property's reactor. This is used when any "input" properties are
        # changed on a widget (e.g. a value setting on a slider).
        binding = self.get_from_datastore(obj)
        if binding and not isinstance(value, from_datastore):
            validated_value = self.validate(value)
            invent.datastore[binding.key] = validated_value
            return

        if isinstance(value, from_datastore):
            # The from_datastore's with_function takes the original  value and
            # returns a new "post-processed" value.
            with_function = value.with_function

            def reactor(message):  # pragma: no cover
                """
                Set the value in the widget and call the optional
                "on_FOO_changed" to ensure the update is visible to the user.
                """
                if with_function is not None:
                    message_value = with_function(message.value)
                else:
                    message_value = message.value
                setattr(obj, self.private_name, self.validate(message_value))
                self._react_on_change(obj, self.private_name)

            # Attach the "from_datastore" instance to the object.
            self.set_from_datastore(obj, value, reactor)

            # Update value to the actual value from the datastore.
            value = invent.datastore.get(value.key, self.default_value)

            # Ensure the raw value is handled by the from_datastore's
            # with_function.
            if with_function is not None:
                value = with_function(value)

        # Set the value in the widget.
        setattr(obj, self.private_name, self.validate(value))
        self._react_on_change(obj, self.private_name)

    def get_from_datastore(self, obj):
        return getattr(obj, self.from_datastore_name, None)

    def set_from_datastore(self, obj, value, reactor=None):
        reactor_prop = f"_{self.name}_reactor"
        old_value = self.get_from_datastore(obj)
        if old_value:
            invent.unsubscribe(
                getattr(obj, reactor_prop),
                invent.datastore.DATASTORE_SET_CHANNEL,
                old_value.key,
            )
            delattr(obj, reactor_prop)

        setattr(obj, self.from_datastore_name, value)
        if value:
            invent.subscribe(
                reactor, invent.datastore.DATASTORE_SET_CHANNEL, value.key
            )
            setattr(obj, reactor_prop, reactor)

    def _react_on_change(self, obj, property_name):
        """
        Ensure any reactive behaviour relating to the setting of the property
        is enacted. This involves two steps:

        1. If the property has a map_to_attribute or map_to_style value, ensure
           the new value is directly set on the object's element.
        2. Call the object's on_changed handler for the specified property
           name, if it exists.
        """
        # Map the value to an HTML attribute whose name is the value of
        # map_to_attribute.
        if self.map_to_attribute and obj.element:
            obj.update_attribute(
                self.map_to_attribute, getattr(obj, self.private_name)
            )

        # Map the value to a CSS property.
        if self.map_to_style and obj.element:
            obj.element.style[self.map_to_style] = getattr(
                obj, self.private_name
            )

        # Handle the existence of an on_FOO_changed function.
        on_changed = getattr(obj, "on" + property_name + "_changed", None)
        if on_changed:
            on_changed()

    def coerce(self, value):
        """
        Return value as an acceptable type (or raise an exception while doing
        so).
        """
        return value

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
            "group": self.group,
        }


class NumericProperty(Property):
    """
    A numeric property, with an optional maximum and minimum, for a Widget.
    """

    def __init__(
        self,
        description,
        default_value=None,
        minimum=None,
        maximum=None,
        **kwargs,
    ):
        """
        In addition to the Property related attributes, the min and max
        define the bounds of a valid value. If set to None, these won't be
        checked during validation.
        """
        self.minimum = minimum
        self.maximum = maximum
        super().__init__(description, default_value, **kwargs)

    def coerce(self, value):
        """
        Try to convert to some sort of valid numeric value.
        """
        # Don't attempt to coerce None, since it could be a valid value.
        if value is None:
            return None

        # Best effort heuristics...
        if "." in str(value):
            # It could be a float.
            try:
                result = float(value)
                return result
            except ValueError:  # pragma: no cover
                pass  # Handle below
        else:
            # Let's try an int instead...
            try:
                result = int(value)
                return result
            except ValueError:  # pragma: no cover
                pass  # Handle below
        raise ValueError(_("Not a valid number: ") + value)

    def validate(self, value):
        """
        The value must be a number (None is allowed if the property is not
        required).

        If set, the value must be between the minimum and maximum boundaries.
        """
        value = super().validate(self.coerce(value))
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

    def coerce(self, value):
        """
        Convert to an int.
        """
        return int(value) if value is not None else None


class FloatProperty(NumericProperty):
    """
    A floating point (a number with a decimal point) property for a Widget.
    """

    def coerce(self, value):
        """
        Convert to a float.
        """
        return float(value) if value is not None else None


class TextProperty(Property):
    """
    A textual property for a Widget.
    """

    def __init__(
        self,
        description,
        default_value=None,
        min_length=None,
        max_length=None,
        **kwargs,
    ):
        """
        In addition to the Property related attributes, the min_length and
        max_length define the bounds of the length of a valid value. If set to
        None, these won't be checked during validation.
        """
        self.min_length = min_length
        self.max_length = max_length
        super().__init__(description, default_value, **kwargs)

    def coerce(self, value):
        """
        Coerce to a string.
        """
        # Don't coerce None because None may be a valid value.
        return str(value) if value is not None else None

    def validate(self, value):
        """
        The value must be a string (or None if not a required property).

        If set, the value must be between the minimum and maximum boundaries.
        """
        value = super().validate(self.coerce(value))
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

    def coerce(self, value):
        return bool(value) if value is not None else None


class ListProperty(Property):
    """
    A list like container property for a Widget.
    """

    def __init__(
        self,
        description,
        default_value=None,
        **kwargs,
    ):
        super().__init__(description, default_value or list(), **kwargs)

    def coerce(self, value):
        if value is None:
            return []

        return list(value)


class JSONProperty(Property):
    """
    A container property for a widget whose value is a JSON serializable data
    structure.
    """

    def coerce(self, value):
        if isinstance(value, str):
            # If the value is a string, we assume it's a JSON string, so just
            # convert it to a Python object.
            value = json.loads(value)
        return value

    def validate(self, value):
        value = super().validate(self.coerce(value))
        # Attemp to convert the value to a JSON string to ensure it's
        # serializable. If it isn't it'll raise a ValueError.
        if type(value) not in (str, int, float, bool, list, dict, type(None)):
            raise ValidationError(_("The value is not JSON serializable."))
        return value


class ChoiceProperty(Property):
    """
    A property for a Widget whose value can only be from a pre-determined set
    of choices.
    """

    def __init__(
        self,
        description,
        choices,
        **kwargs,
    ):
        """
        In addition to the Property related attributes, the choices enumerate
        a set of valid values.
        """
        self.choices = choices
        super().__init__(description, **kwargs)

    def validate(self, value):
        """
        Ensure the property's value is in the set of valid choices. This check
        is case insensitive if the passed in value is a string.
        """
        if isinstance(value, str):
            lower_choices = [
                c.lower() for c in self.choices if isinstance(c, str)
            ]
            if value.lower() in lower_choices:
                return super().validate(value)
        elif value in self.choices or value is None:
            return super().validate(value)
        raise ValidationError(
            _("The value is not one of the valid choices."),
            value,
            self.choices,
        )

    def as_dict(self):
        """
        Return a Python dictionary as a data structure representing all the
        essential information about the property.
        """
        result = super().as_dict()
        result["choices"] = self.choices
        return result


class DateProperty(Property):
    """
    A property for a Widget that represents a date. The date is assigned as
    a datetime.Date instance, a string in the format "YYYY-MM-DD" or None.

    The date is stored as a datetime.Date instance. If a minimum or maximum
    date is set, the value must be within the range.
    """

    def __init__(
        self,
        description,
        default_value=None,
        minimum=None,
        maximum=None,
        **kwargs,
    ):
        """
        In addition to the Property related attributes, the min and max
        define the bounds of a valid value. If set to None, these won't be
        checked during validation.
        """
        self.minimum = self.coerce(minimum)
        self.maximum = self.coerce(maximum)
        super().__init__(description, default_value, **kwargs)

    def coerce(self, value):
        if isinstance(value, datetime.date):
            return value
        elif isinstance(value, str):
            # MicroPython doesn't support strptime, so we have to do this.
            try:
                return datetime.date(*map(int, value.split("-")))
            except Exception:
                raise ValidationError(_("Not a valid date."), value)
        elif value is None:
            return None
        raise ValidationError(_("Not a valid date."), value)

    def validate(self, value):
        value = super().validate(self.coerce(value))
        if value is not None:
            if self.minimum and value < self.minimum:
                raise ValidationError(
                    _("The date is less than the minimum allowed."),
                    value,
                    self.minimum,
                )
            if self.maximum and value > self.maximum:
                raise ValidationError(
                    _("The date is greater than the maximum allowed."),
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
        result["default_value"] = str(self.default_value)
        result["minimum"] = str(self.minimum)
        result["maximum"] = str(self.maximum)
        return result

    def __str__(self):
        """
        Return a string representation of the date object
        """
        return str(self.value)


class TimeProperty(Property):
    """
    A property for a Widget that represents a time. The time is assigned as
    a datetime.Time instance, a string in the format "HH:MM:SS" or None.

    The time is stored as a datetime.Time instance. If a minimum or maximum
    time is set, the value must be within the range.
    """

    def __init__(
        self,
        description,
        default_value=None,
        minimum=None,
        maximum=None,
        **kwargs,
    ):
        """
        In addition to the Property related attributes, the min and max
        define the bounds of a valid value. If set to None, these won't be
        checked during validation.
        """
        self.minimum = self.coerce(minimum)
        self.maximum = self.coerce(maximum)
        super().__init__(description, default_value, **kwargs)

    def coerce(self, value):
        if isinstance(value, datetime.time):
            return value
        elif isinstance(value, str):
            # MicroPython doesn't support strptime, so we have to do this.
            try:
                return datetime.time(*map(int, value.split(":")))
            except Exception:
                raise ValidationError(_("Not a valid time."), value)
        elif value is None:
            return None
        raise ValidationError(_("Not a valid time."), value)

    def validate(self, value):
        value = super().validate(self.coerce(value))
        if value is not None:
            if self.minimum and value < self.minimum:
                raise ValidationError(
                    _("The time is less than the minimum allowed."),
                    value,
                    self.minimum,
                )
            if self.maximum and value > self.maximum:
                raise ValidationError(
                    _("The time is greater than the maximum allowed."),
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
        result["default_value"] = str(self.default_value)
        result["minimum"] = str(self.minimum)
        result["maximum"] = str(self.maximum)
        return result

    def __str__(self):
        """
        Return a string representation of the time object
        """
        return str(self.value)


class DatetimeProperty(Property):
    """
    A property for a Widget that represents a datetime. The datetime is
    assigned as a datetime.Datetime instance, a string in the format
    "YYYY-MM-DD HH:MM:SS" or None.

    The datetime is stored as a datetime.Datetime instance. If a minimum or
    maximum datetime is set, the value must be within the range.
    """

    def __init__(
        self,
        description,
        default_value=None,
        minimum=None,
        maximum=None,
        **kwargs,
    ):
        """
        In addition to the Property related attributes, the min and max
        define the bounds of a valid value. If set to None, these won't be
        checked during validation.
        """
        self.minimum = self.coerce(minimum)
        self.maximum = self.coerce(maximum)
        super().__init__(description, default_value, **kwargs)

    def coerce(self, value):
        if isinstance(value, datetime.datetime):
            return value
        elif isinstance(value, str):
            # MicroPython doesn't support strptime, so we have to do this.
            try:
                date_section, time_section = value.split(" ")
                return datetime.datetime(
                    *map(int, date_section.split("-")),
                    *map(int, time_section.split(":")),
                )
            except Exception:
                raise ValidationError(_("Not a valid datetime."), value)
        elif value is None:
            return None
        raise ValidationError(_("Not a valid datetime."), value)

    def validate(self, value):
        value = super().validate(self.coerce(value))
        if value is not None:
            if self.minimum and value < self.minimum:
                raise ValidationError(
                    _("The datetime is less than the minimum allowed."),
                    value,
                    self.minimum,
                )
            if self.maximum and value > self.maximum:
                raise ValidationError(
                    _("The datetime is greater than the maximum allowed."),
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
        result["default_value"] = str(self.default_value)
        result["minimum"] = str(self.minimum)
        result["maximum"] = str(self.maximum)
        return result

    def __str__(self):
        """
        Return a string representation of the datetime value represented by the
        property.
        """
        return str(self.value)
