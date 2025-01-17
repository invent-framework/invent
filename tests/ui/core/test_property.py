from pyscript.web import div
import upytest
import umock
import datetime
import json
import invent
from invent.ui.core import (
    BooleanProperty,
    ChoiceProperty,
    DateProperty,
    FloatProperty,
    IntegerProperty,
    ListProperty,
    NumericProperty,
    Property,
    TextProperty,
    TimeProperty,
    ValidationError,
    from_datastore,
    Component,
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
    assert repr(fds) == "from_datastore('foo', with_function=test_fn)"


def test_property_init():
    """
    Test that the Property class can be initialised with a description.
    """
    p = Property("A test property")
    assert p.description == "A test property"
    # Has a private name against which to store the value
    assert p.default_value is None
    assert p.required is False


def test_property_init_default():
    """
    Test that the Property class can be initialised with a default value.
    """
    p = Property("A test property", default_value=42)
    assert p.description == "A test property"
    assert p.default_value == 42
    assert p.required is False


def test_property_required_field_needs_default_value():
    """
    If a property is marked as required, a default value must also be supplied.
    """
    with upytest.raises(ValidationError):
        # Fail with a ValidationError if no default value.
        Property("A test property", required=True)
    # Default value and required is OK.
    p = Property("A test property", default_value="test", required=True)
    assert p.description == "A test property"
    assert p.default_value == "test"
    assert p.required is True

    class FakeWidget(Component):
        my_property = Property(
            "A test property", default_value="test", required=True
        )

        def render(self):
            return div()

    # The default value is used.
    t = FakeWidget()
    assert t.my_property == "test"
    # Trying to set the value as None results in a ValidationError.
    with upytest.raises(ValidationError):
        t.my_property = None


def test_property_from_datastore():
    """
    If the property is set a value from_datastore, the expected reactor
    function is subscribed to the correct datastore key.
    """

    class FakeWidget(Component):
        my_property = Property("A test property")

        def render(self):
            return div()

    test_fn = umock.Mock()
    fw = FakeWidget()
    # fmt: off
    with umock.patch(
            "invent:subscribe"
    ) as mock_sub, umock.patch("invent:unsubscribe") as mock_unsub:
        fw.my_property = from_datastore("test", with_function=test_fn)
        mock_unsub.assert_not_called()
        mock_sub.assert_called_once()
        reactor = mock_sub.call_args[0][0]
        assert callable(reactor)
        assert mock_sub.call_args[0][1] == invent.datastore.DATASTORE_SET_CHANNEL
        assert mock_sub.call_args[0][2] == "test"
        test_fn.assert_called_once_with(None)
        mock_sub.reset_mock()
        fw.my_property = from_datastore("test2")
        mock_unsub.assert_called_once_with(reactor, invent.datastore.DATASTORE_SET_CHANNEL, "test")
        reactor = mock_sub.call_args[0][0]
        assert callable(reactor)
        assert mock_sub.call_args[0][1] == invent.datastore.DATASTORE_SET_CHANNEL
        assert mock_sub.call_args[0][2] == "test2"
    # fmt: on


def test_from_datastore_react_on_change():
    """
    If the property is set a value from_datastore, subsequently setting it to
    another value should update the datastore.
    """

    class FakeWidget(Component):
        my_property = Property("A test property")

        def render(self):
            return div()

    fw = FakeWidget()
    fw.my_property = from_datastore("test")
    fw.my_property = "value1"
    assert invent.datastore["test"] == "value1"


def test_property_react_on_change():
    """
    If the property is given a map_to_attribute and the parent object has an
    on_FOO_changed method, both situations are handled so the new value set
    against the property is propagated as expected.
    """

    class FakeWidget(Component):
        my_property = Property("A test", map_to_attribute="test")

        def on_my_property_changed(self):
            pass

        def render(self):
            return div()

    fw = FakeWidget()
    # Mock to check the methods are called.
    fw.on_my_property_changed = umock.Mock()
    fw.update_attribute = umock.Mock()
    fw.element = umock.Mock()
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

    class FakeWidget(Component):
        my_property = Property("A test", map_to_style="hyphenated-name")

        def render(self):
            return div()

    fw = FakeWidget()
    fw.element = umock.Mock()
    fw.element.style = {}
    fw.my_property = "the value"
    assert fw.element.style == {"hyphenated-name": "the value"}


def test_property_as_dict():
    """
    The expected JSON serializable Python dictionary defining the property's
    structure and attributes is returned.
    """
    # With all the attributes of a property given.
    p = Property(
        "A test property", default_value="test", required=True, group="test"
    )
    assert p.as_dict() == {
        "property_type": "Property",
        "description": "A test property",
        "required": True,
        "default_value": "test",
        "group": "test",
    }
    assert json.dumps(p.as_dict())

    # Assuming the default attributes of a property.
    p = Property("A test property")
    assert p.as_dict() == {
        "property_type": "Property",
        "description": "A test property",
        "required": False,
        "default_value": None,
        "group": None,
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

    class FakeWidget(Component):
        number = NumericProperty("A test property")

        def render(self):
            return div()

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
    with upytest.raises(ValueError):
        widget.number = "test"


def test_numeric_property_with_bounds():
    """
    A numeric property with bounds cannot have a value outside those bounds.

    If the value is not required, the value could be set to None.
    """

    class FakeWidget(Component):
        number = NumericProperty(
            "A test property", default_value=150, minimum=100, maximum=200
        )

        def render(self):
            return div()

    widget = FakeWidget()

    # The value can be None if the property is not required.
    widget.number = None
    # The value cannot be less than the minimum.
    widget.number = 100
    with upytest.raises(ValidationError):
        widget.number = 99.9
    # The value cannot be more than the maximum.
    widget.number = 200
    with upytest.raises(ValidationError):
        widget.number = 200.01

    # Now with only a minimum.

    class FakeWidgetMin(Component):
        number = NumericProperty(
            "A test property", default_value=150, minimum=100
        )

        def render(self):
            return div()

    widget = FakeWidgetMin()

    # The value can be None if the property is not required.
    widget.number = None
    # The value cannot be less than the minimum.
    widget.number = 100
    with upytest.raises(ValidationError):
        widget.number = 99.9
    # There is no maximum boundary.
    widget.number = 999999

    # Now with only a minimum.

    class FakeWidgetMax(Component):
        number = NumericProperty(
            "A test property", default_value=150, maximum=200
        )

        def render(self):
            return div()

    widget = FakeWidgetMax()

    # The value can be None if the property is not required.
    widget.number = None
    # No minimum boundary
    widget.number = -999999
    # The value cannot be more than the maximum.
    widget.number = 200
    with upytest.raises(ValidationError):
        widget.number = 200.01


def test_numeric_property_as_dict():
    """
    The expected JSON serializable Python dictionary defining the property's
    structure and attributes is returned.
    """
    np = NumericProperty("A test property", default_value=150, minimum=100)
    assert np.as_dict() == {
        "property_type": "NumericProperty",
        "description": "A test property",
        "required": False,
        "default_value": 150,
        "minimum": 100,
        "maximum": None,
        "group": None,
    }


def test_integer_property():
    """
    An integer property can only have an integer value.
    """

    class FakeWidget(Component):
        integer = IntegerProperty("A test integer property", default_value=123)

        def render(self):
            return div()

    fw = FakeWidget()
    assert fw.integer == 123
    # coercion works.
    fw.integer = "123"
    assert fw.integer == 123
    # Anything else causes a ValueError
    with upytest.raises(ValueError):
        fw.integer = "forty two"


def test_float_property():
    """
    A float property can only have a floating point value.
    """

    class FakeWidget(Component):
        val = FloatProperty("A test float property", default_value=1.23)

        def render(self):
            return div()

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
    with upytest.raises(ValueError):
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

    class FakeWidget(Component):
        text = TextProperty("A test property")

        def render(self):
            return div()

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

    class FakeWidget(Component):
        text = TextProperty(
            "A test property", default_value="test", required=True
        )

        def render(self):
            return div()

    widget = FakeWidget()
    widget.text = "another test"
    # Cannot be set to None if a required field.
    with upytest.raises(ValidationError):
        widget.text = None


def test_text_property_value_with_min_max_length():
    """
    If the min and max length are defined, the length of the value must be
    within the bounds.
    """

    # Both min and max length are defined.
    class FakeWidget(Component):
        text = TextProperty("A test property", min_length=4, max_length=10)

        def render(self):
            return div()

    widget = FakeWidget()
    # A None value is ignored if it is not a required property.
    widget.text = None
    # The length of the value cannot be below the min_length.
    widget.text = "1234"
    with upytest.raises(ValidationError):
        widget.text = "123"
    # The length of the value cannot be above max_length.
    widget.text = "0123456789"
    with upytest.raises(ValidationError):
        widget.text = "0123456789+"

    # Only minimum length is defined.
    class FakeWidgetMin(Component):
        text = TextProperty("A test property", min_length=4)

        def render(self):
            return div()

    widget = FakeWidgetMin()
    # A None value is ignored if it is not a required property.
    widget.text = None
    # The length of the value cannot be below the min_length.
    widget.text = "1234"
    with upytest.raises(ValidationError):
        widget.text = "123"
    # No upper bound.
    widget.text = "0123456789+++++"

    # Only maximum length is defined.
    class FakeWidgetMax(Component):
        text = TextProperty("A test property", max_length=10)

        def render(self):
            return div()

    widget = FakeWidgetMax()
    # A None value is ignored if it is not a required property.
    widget.text = None
    # The length of the value cannot be below the min_length.
    widget.text = ""
    # The length of the value cannot be above max_length.
    widget.text = "0123456789"
    with upytest.raises(ValidationError):
        widget.text = "0123456789+"


def test_text_property_as_dict():
    """
    The expected JSON serializable Python dictionary defining the property's
    structure and attributes is returned.
    """
    tp = TextProperty("A test property", max_length=10, group="test")
    assert tp.as_dict() == {
        "property_type": "TextProperty",
        "description": "A test property",
        "required": False,
        "default_value": None,
        "min_length": None,
        "max_length": 10,
        "group": "test",
    }


def test_boolean_property_values():
    """
    If required a boolean property's value can only be True or False.

    If not required, None is also allowed. Anything else fails.
    """

    class FakeWidget(Component):
        flag = BooleanProperty(
            "A test property", default_value=True, required=True
        )

        def render(self):
            return div()

    widget = FakeWidget()
    widget.flag = False
    widget.flag = True
    # Cannot use None if a required property.
    with upytest.raises(ValidationError):
        widget.flag = None
    # Coercion to boolean works.
    widget.flag = 1
    assert widget.flag is True

    # Check behaviour of BooleanProperty if not a required field.
    class FakeWidgetNotRequired(Component):
        flag = BooleanProperty("A test property")

        def render(self):
            return div()

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

    class FakeWidget(Component):
        select = ChoiceProperty(
            "A test property",
            choices=[
                "Foo",
                "Bar",
                "Baz",
            ],
        )

        def render(self):
            return div()

    widget = FakeWidget()
    # If the property is not required, None is also valid.
    widget.select = None
    # A valid choice is a case insensitive valid value.
    widget.select = "foo"
    # Outside the valid choices is invalid.
    with upytest.raises(ValidationError):
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
        group="test",
    )
    assert cp.as_dict() == {
        "property_type": "ChoiceProperty",
        "description": "A test property",
        "required": False,
        "default_value": None,
        "group": "test",
        "choices": [1, 2, 3],
    }


def test_list_property_validation():
    """
    ListProperty works with None and lists.
    """

    class TestComponent(Component):
        content = ListProperty("The child components.")

        def render(self):
            return div()

    tc = TestComponent()
    tc.children = [
        "foo",
        "bar",
        "baz",
    ]
    tc.content = None
    with upytest.raises(TypeError):
        tc.content = False


def test_date_property_defaults_no_min_max():
    """
    By default the bounds for minimum and maximum value are None.
    """
    dp = DateProperty("A test property")
    assert dp.minimum is None
    assert dp.maximum is None


def test_date_property_value_is_date():
    """
    The value must be a date or None if not a required property.
    """

    class FakeWidget(Component):
        date = DateProperty("A test property")

        def render(self):
            return div()

    widget = FakeWidget()
    a_date = datetime.date(2021, 1, 1)
    # Dates are OK.
    widget.date = a_date
    assert widget.date == a_date
    # Dates as "YYYY-MM-DD" strings are OK.
    widget.date = str(a_date)
    assert widget.date == a_date
    # As is None.
    widget.date = None
    assert widget.date is None
    # Anything else causes a ValidationError
    with upytest.raises(ValidationError):
        widget.date = "test"


def test_date_property_with_bounds():
    """
    A date property with bounds cannot have a value outside those bounds.
    """

    class FakeWidget(Component):
        date = DateProperty(
            "A test property",
            default_value=datetime.date(2021, 1, 1),
            minimum=datetime.date(2021, 1, 1),
            maximum=datetime.date(2021, 1, 31),
        )

        def render(self):
            return div()

    widget = FakeWidget()
    a_date = datetime.date(2021, 1, 1)
    # The value can be None if the property is not required.
    widget.date = None
    # The value cannot be less than the minimum.
    widget.date = a_date
    with upytest.raises(ValidationError):
        widget.date = datetime.date(2020, 12, 31)
    # The value cannot be more than the maximum.
    widget.date = datetime.date(2021, 1, 31)
    with upytest.raises(ValidationError):
        widget.date = datetime.date(2021, 2, 1)

    # Now with only a minimum.

    class FakeWidgetMin(Component):
        date = DateProperty(
            "A test property",
            default_value=datetime.date(2021, 1, 1),
            minimum=datetime.date(2021, 1, 1),
        )

        def render(self):
            return div()

    widget = FakeWidgetMin()
    a_date = datetime.date(2021, 1, 1)
    # The value can be None if the property is not required.
    widget.date = None
    # The value cannot be less than the minimum.
    widget.date = a_date
    with upytest.raises(ValidationError):
        widget.date = datetime.date(2020, 12, 31)
    # There is no maximum boundary.
    widget.date = datetime.date(2021, 1, 31)

    # Now with only a maximum.

    class FakeWidgetMax(Component):
        date = DateProperty(
            "A test property",
            default_value=datetime.date(2021, 1, 1),
            maximum=datetime.date(2021, 1, 31),
        )

        def render(self):
            return div()

    widget = FakeWidgetMax()
    a_date = datetime.date(2021, 1, 1)
    # The value can be None if the property is not required.
    widget.date = None
    # No minimum boundary
    widget.date = datetime.date(2020, 12, 31)
    # The value cannot be more than the maximum.
    widget.date = datetime.date(2021, 1, 31)
    with upytest.raises(ValidationError):
        widget.date = datetime.date(2021, 2, 1)


def test_date_property_as_dict():
    """
    The expected JSON serializable Python dictionary defining the property's
    structure and attributes is returned.
    """
    dp = DateProperty(
        "A test property",
        default_value=datetime.date(2021, 1, 1),
        minimum=datetime.date(2021, 1, 1),
        maximum=datetime.date(2021, 1, 31),
    )
    assert dp.as_dict() == {
        "property_type": "DateProperty",
        "description": "A test property",
        "required": False,
        "default_value": str(datetime.date(2021, 1, 1)),
        "minimum": str(datetime.date(2021, 1, 1)),
        "maximum": str(datetime.date(2021, 1, 31)),
        "group": None,
    }


def test_time_property_defaults_no_min_max():
    """
    By default the bounds for minimum and maximum value are None.
    """
    tp = TimeProperty("A test property")
    assert tp.minimum is None
    assert tp.maximum is None


def test_time_property_value_is_time():
    """
    The value must be a time or None if not a required property.
    """

    class FakeWidget(Component):
        time = TimeProperty("A test property")

        def render(self):
            return div()

    widget = FakeWidget()
    a_time = datetime.time(12, 0, 0)
    # Times are OK.
    widget.time = a_time
    assert widget.time == a_time
    # Times as "HH:MM:SS" strings are OK.
    widget.time = str(a_time)
    assert widget.time == a_time
    # As is None.
    widget.time = None
    assert widget.time is None
    # Anything else causes a ValidationError
    with upytest.raises(ValidationError):
        widget.time = "test"


def test_time_property_with_bounds():
    """
    A time property with bounds cannot have a value outside those bounds.
    """

    class FakeWidget(Component):
        time = TimeProperty(
            "A test property",
            default_value=datetime.time(12, 0, 0),
            minimum=datetime.time(12, 0, 0),
            maximum=datetime.time(12, 0, 1),
        )

        def render(self):
            return div()

    widget = FakeWidget()
    a_time = datetime.time(12, 0, 0)
    # The value can be None if the property is not required.
    widget.time = None
    # The value cannot be less than the minimum.
    widget.time = a_time
    with upytest.raises(ValidationError):
        widget.time = datetime.time(11, 59, 59)
    # The value cannot be more than the maximum.
    widget.time = datetime.time(12, 0, 1)
    with upytest.raises(ValidationError):
        widget.time = datetime.time(12, 0, 2)

    # Now with only a minimum.

    class FakeWidgetMin(Component):
        time = TimeProperty(
            "A test property",
            default_value=datetime.time(12, 0, 0),
            minimum=datetime.time(12, 0, 0),
        )

        def render(self):
            return div()

    widget = FakeWidgetMin()
    a_time = datetime.time(12, 0, 0)
    # The value can be None if the property is not required.
    widget.time = None
    # The value cannot be less than the minimum.
    widget.time = a_time
    with upytest.raises(ValidationError):
        widget.time = datetime.time(11, 59, 59)
    # There is no maximum boundary.
    widget.time = datetime.time(12, 0, 1)

    # Now with only a maximum.

    class FakeWidgetMax(Component):
        time = TimeProperty(
            "A test property",
            default_value=datetime.time(12, 0, 0),
            maximum=datetime.time(12, 0, 1),
        )

        def render(self):
            return div()

    widget = FakeWidgetMax()
    a_time = datetime.time(12, 0, 0)
    # The value can be None if the property is not required.
    widget.time = None
    # No minimum boundary
    widget.time = datetime.time(11, 59, 59)
    # The value cannot be more than the maximum.
    widget.time = datetime.time(12, 0, 1)
    with upytest.raises(ValidationError):
        widget.time = datetime.time(12, 0, 2)


def test_time_property_as_dict():
    """
    The expected JSON serializable Python dictionary defining the property's
    structure and attributes is returned.
    """
    tp = TimeProperty(
        "A test property",
        default_value=datetime.time(12, 0, 0),
        minimum=datetime.time(12, 0, 0),
        maximum=datetime.time(12, 0, 1),
    )
    assert tp.as_dict() == {
        "property_type": "TimeProperty",
        "description": "A test property",
        "required": False,
        "default_value": str(datetime.time(12, 0, 0)),
        "minimum": str(datetime.time(12, 0, 0)),
        "maximum": str(datetime.time(12, 0, 1)),
        "group": None,
    }
