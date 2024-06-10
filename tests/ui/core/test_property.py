import pytest
from unittest import mock
from invent.ui.core import (
    BooleanProperty,
    ChoiceProperty,
    FloatProperty,
    IntegerProperty,
    ListProperty,
    NumericProperty,
    Property,
    TextProperty,
    ValidationError,
    from_datastore,
)


def test_from_datastore():
    """
    Ensure this signal class has a key attribute and optional with_function,
    that is repr'd correctly into code.
    """

    def test_fn(val):
        return val

    fds = from_datastore("foo", with_function=test_fn)
    assert fds.key == "foo"
    assert fds.with_function == test_fn
    assert repr(fds) == 'from_datastore("foo", with_function=test_fn)'


def test_property_init():
    """
    The property is initialised with a description, and optional value
    and required flag.
    """
    p = Property("A test property")
    assert p.description == "A test property"
    # Has a private name against which to store the value
    assert p.default_value is None
    assert p.required is False


def test_property_required_field_needs_default_value():
    """
    If a property is marked as required, a default value must also be supplied.
    """
    with pytest.raises(ValidationError):
        # Fail with a ValidationError if no default value.
        Property("A test property", required=True)
    # Default value and required is OK.
    p = Property("A test property", default_value="test", required=True)
    assert p.description == "A test property"
    assert p.default_value == "test"
    assert p.required is True

    class FakeWidget:
        my_property = Property(
            "A test property", default_value="test", required=True
        )

    # The default value is used.
    t = FakeWidget()
    assert t.my_property == "test"
    # Trying to set the value as None results in a ValidationError.
    with pytest.raises(ValidationError):
        t.my_property = None


def test_property_from_datastore():
    """
    If the property is set a value from_datastore, the expected reactor
    function is subscribed to the correct datastore key.
    """

    class FakeWidget:
        my_property = Property("A test property")

    test_fn = mock.MagicMock()
    fw = FakeWidget()
    with mock.patch("invent.subscribe") as mock_sub:
        fw.my_property = from_datastore("test", with_function=test_fn)
        assert mock_sub.call_args[1]["to_channel"] == "store-data"
        assert mock_sub.call_args[1]["when_subject"] == "test"
        assert mock_sub.call_count == 1
        test_fn.assert_called_once_with(None)


def test_property_react_on_change():
    """
    If the property is given a map_to_attribute and the parent object has an
    on_FOO_changed method, both situations are handled so the new value set
    against the property is propagated as expected.
    """

    class FakeWidget:
        my_property = Property("A test", map_to_attribute="test")

        def on_my_property_changed(self):
            pass

    fw = FakeWidget()
    # Mock to check the methods are called.
    fw.on_my_property_changed = mock.MagicMock()
    fw.update_attribute = mock.MagicMock()
    fw.element = mock.MagicMock()
    # Set the property to a new value.
    fw.my_property = "yes"
    # The element's attribute to which the property is mapped has been updated.
    fw.update_attribute.assert_called_once_with("test", "yes")
    # The on_FOO_changed function for the property has been called.
    fw.on_my_property_changed.assert_called_once_with()


def test_property_map_to_style():
    """
    If the property is given a map_to_style, any value is set as a CSS style.
    """
    class FakeWidget:
        my_property = Property("A test", map_to_style="hyphenated-name")

    fw = FakeWidget()
    fw.element = mock.Mock()
    fw.my_property = "the value"
    fw.element.style.setProperty.assert_called_once_with(
        "hyphenated-name", "the value"
    )


def test_property_as_dict():
    """
    The expected JSON serializable Python dictionary defining the property's
    structure and attributes is returned.
    """
    p = Property("A test property", default_value="test", required=True)
    assert p.as_dict() == {
        "property_type": "Property",
        "description": "A test property",
        "required": True,
        "default_value": "test",
    }


def test_numeric_property_defaults_no_min_or_max():
    """
    By default the bounds for minimum and maximum value are None.
    """
    np = NumericProperty("A test property")
    assert np.minimum is None
    assert np.maximum is None


def test_numeric_property_must_be_a_number():
    """
    A numeric property cannot hold a non-numeric value.
    """

    class FakeWidget:
        number = NumericProperty("A test property")

    widget = FakeWidget()

    # The value can be None if the property is not required.
    widget.number = None
    # The value can be an integer.
    widget.number = 42
    # The value can be a float.
    widget.number = 3.141
    # The value can be coerced to an int.
    widget.number = "1"
    # The value can be coerced into a float.
    widget.number = "1.234"
    # The value cannot be anything else.
    with pytest.raises(ValueError):
        widget.number = "test"


def test_numeric_property_with_bounds():
    """
    A numeric property with bounds cannot have a value outside those bounds.

    If the value is not required, the value could be set to None.
    """

    class FakeWidget:
        number = NumericProperty(
            "A test property", default_value=150, minimum=100, maximum=200
        )

    widget = FakeWidget()

    # The value can be None if the property is not required.
    widget.number = None
    # The value cannot be less than the minimum.
    widget.number = 100
    with pytest.raises(ValidationError):
        widget.number = 99.9
    # The value cannot be more than the maximum.
    widget.number = 200
    with pytest.raises(ValidationError):
        widget.number = 200.01

    # Now with only a minimum.

    class FakeWidgetMin:
        number = NumericProperty(
            "A test property", default_value=150, minimum=100
        )

    widget = FakeWidgetMin()

    # The value can be None if the property is not required.
    widget.number = None
    # The value cannot be less than the minimum.
    widget.number = 100
    with pytest.raises(ValidationError):
        widget.number = 99.9
    # There is no maximum boundary.
    widget.number = 999999

    # Now with only a minimum.

    class FakeWidgetMax:
        number = NumericProperty(
            "A test property", default_value=150, maximum=200
        )

    widget = FakeWidgetMax()

    # The value can be None if the property is not required.
    widget.number = None
    # No minimum boundary
    widget.number = -999999
    # The value cannot be more than the maximum.
    widget.number = 200
    with pytest.raises(ValidationError):
        widget.number = 200.01


def test_numeric_property_as_dict():
    """
    The expected JSON serializable Python dictionary defining the property's
    structure and attributes is returned.
    """
    np = NumericProperty(
        "A test property", default_value=150, minimum=100
    )
    assert np.as_dict() == {
        "property_type": "NumericProperty",
        "description": "A test property",
        "required": False,
        "default_value": 150,
        "minimum": 100,
        "maximum": None,
    }


def test_integer_property():
    """
    An integer property can only have an integer value.
    """

    class FakeWidget:
        integer = IntegerProperty(
            "A test integer property", default_value=123
        )

    fw = FakeWidget()
    assert fw.integer == 123
    # coercion works.
    fw.integer = "123"
    assert fw.integer == 123
    # Anything else causes a ValueError
    with pytest.raises(ValueError):
        fw.integer = "forty two"


def test_float_property():
    """
    A float property can only have a floating point value.
    """

    class FakeWidget:
        val = FloatProperty("A test float property", default_value=1.23)

    fw = FakeWidget()
    assert fw.val == 1.23
    fw.val = 123.4
    assert fw.val == 123.4
    # Integers become floats.
    fw.val = 123
    assert fw.val == 123.0
    # coercion works.
    fw.val = "123.4"
    assert fw.val == 123.4
    # Anything else causes a ValueError
    with pytest.raises(ValueError):
        fw.val = "forty two"


def test_text_property_defaults():
    """
    A text property has no default minimum or maximum length.
    """
    tp = TextProperty("A test property")
    assert tp.min_length is None
    assert tp.max_length is None


def test_text_property_value_is_string():
    """
    The value must be a string or None if not a required property.
    """

    class FakeWidget:
        text = TextProperty("A test property")

    widget = FakeWidget()
    # Strings are OK.
    widget.text = "test"
    # As is None.
    widget.text = None
    # Coerce for any other non-string value.
    widget.text = 123
    assert widget.text == "123"


def test_text_property_value_is_required_string():
    """
    The value must be a string if a required property.
    """

    class FakeWidget:
        text = TextProperty(
            "A test property", default_value="test", required=True
        )

    widget = FakeWidget()
    widget.text = "another test"
    # Cannot be set to None if a required field.
    with pytest.raises(ValidationError):
        widget.text = None


def test_text_property_value_with_min_max_length():
    """
    If the min and max length are defined, the length of the value must be
    within the bounds.
    """

    # Both min and max length are defined.
    class FakeWidget:
        text = TextProperty(
            "A test property", min_length=4, max_length=10
        )

    widget = FakeWidget()
    # A None value is ignored if it is not a required property.
    widget.text = None
    # The length of the value cannot be below the min_length.
    widget.text = "1234"
    with pytest.raises(ValidationError):
        widget.text = "123"
    # The length of the value cannot be above max_length.
    widget.text = "0123456789"
    with pytest.raises(ValidationError):
        widget.text = "0123456789+"

    # Only minimum length is defined.
    class FakeWidgetMin:
        text = TextProperty("A test property", min_length=4)

    widget = FakeWidgetMin()
    # A None value is ignored if it is not a required property.
    widget.text = None
    # The length of the value cannot be below the min_length.
    widget.text = "1234"
    with pytest.raises(ValidationError):
        widget.text = "123"
    # No upper bound.
    widget.text = "0123456789+++++"

    # Only maximum length is defined.
    class FakeWidgetMax:
        text = TextProperty("A test property", max_length=10)

    widget = FakeWidgetMax()
    # A None value is ignored if it is not a required property.
    widget.text = None
    # The length of the value cannot be below the min_length.
    widget.text = ""
    # The length of the value cannot be above max_length.
    widget.text = "0123456789"
    with pytest.raises(ValidationError):
        widget.text = "0123456789+"


def test_text_property_as_dict():
    """
    The expected JSON serializable Python dictionary defining the property's
    structure and attributes is returned.
    """
    tp = TextProperty("A test property", max_length=10)
    assert tp.as_dict() == {
        "property_type": "TextProperty",
        "description": "A test property",
        "required": False,
        "default_value": None,
        "min_length": None,
        "max_length": 10,
    }


def test_boolean_property_values():
    """
    If required a boolean property's value can only be True or False.

    If not required, None is also allowed. Anything else fails.
    """

    class FakeWidget:
        flag = BooleanProperty(
            "A test property", default_value=True, required=True
        )

    widget = FakeWidget()
    widget.flag = False
    widget.flag = True
    # Cannot use None if a required property.
    with pytest.raises(ValidationError):
        widget.flag = None
    # Coercion to boolean works.
    widget.flag = 1
    assert widget.flag is True

    # Check behaviour of BooleanProperty if not a required field.
    class FakeWidgetNotRequired:
        flag = BooleanProperty("A test property")

    widget = FakeWidgetNotRequired()
    widget.flag = False
    widget.flag = True
    # Can use None if NOT a required property.
    widget.flag = None
    # Coercion works.
    widget.flag = 1
    assert widget.flag is True


def test_choice_property_validation():
    """
    A value set to a choice property must be one of the defined valid choices.
    """

    class FakeWidget:
        select = ChoiceProperty(
            "A test property",
            choices=[
                1,
                2,
                3,
            ],
        )

    widget = FakeWidget()
    # If the property is not required, None is also valid.
    widget.select = None
    # A valid choice is a valid value.
    widget.select = 1
    # Outside the valid choices is invalid.
    with pytest.raises(ValidationError):
        widget.select = 0


def test_choice_property_as_dict():
    """
    The expected JSON serializable Python dictionary defining the property's
    structure and attributes is returned.
    """
    cp = ChoiceProperty(
        "A test property",
        choices=[
            1,
            2,
            3,
        ],
    )
    assert cp.as_dict() == {
        "property_type": "ChoiceProperty",
        "description": "A test property",
        "required": False,
        "default_value": None,
        "choices": [1, 2, 3],
    }


def test_list_property_validation():
    """
    ListProperty works with None and lists.
    """

    class TestComponent:
        content = ListProperty("The child components.")

    tc = TestComponent()
    tc.content = [
        "foo",
        "bar",
        "baz",
    ]
    tc.content = None
    with pytest.raises(TypeError):
        tc.content = False
