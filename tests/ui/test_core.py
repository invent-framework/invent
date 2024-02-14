import pytest
from invent.ui import core


def test_property_init():
    """
    The property is initialised with a description, and optional value
    and required flag.
    """
    p = core.Property("A test property")
    assert p.description == "A test property"
    # Has a private name against which to store the value
    assert p.default_value is None
    assert p.required is False


def test_property_required_field_needs_default_value():
    """
    If a property is marked as required, a default value must also be supplied.
    """
    with pytest.raises(core.ValidationError):
        # Fail with a ValidationError if no default value.
        core.Property("A test property", required=True)
    # Default value and required is OK.
    p = core.Property("A test property", default_value="test", required=True)
    assert p.description == "A test property"
    assert p.default_value == "test"
    assert p.required is True

    class FakeWidget:
        my_property = core.Property(
            "A test property", default_value="test", required=True
        )

        def __init__(self, test="test"):
            self.my_property = test

    # The default value is used.
    t = FakeWidget()
    assert t.my_property == "test"
    # A passed in value is used
    t = FakeWidget(test="bar")
    assert t.my_property == "bar"
    # Trying to set the value as None results in a ValidationError.
    with pytest.raises(core.ValidationError):
        t.my_property = None
    # Cannot instantiate with None value either.
    with pytest.raises(core.ValidationError):
        FakeWidget(test=None)


def test_property_as_dict():
    """
    The expected JSON serializable Python dictionary defining the property's
    structure and attributes is returned.
    """
    p = core.Property("A test property", default_value="test", required=True)
    assert p.as_dict("test") == {
        "property_type": "Property",
        "description": "A test property",
        "required": True,
        "value": "test",
    }


def test_numeric_property_defaults_no_min_or_max():
    """
    By default the bounds for minimum and maximum value are None.
    """
    np = core.NumericProperty("A test property")
    assert np.minimum is None
    assert np.maximum is None


def test_numeric_property_must_be_a_number():
    """
    A numeric property cannot hold a non-numeric value.
    """

    class FakeWidget:
        number = core.NumericProperty("A test property")

        def __init__(self, test=None):
            self.number = test

    widget = FakeWidget()

    # The value can be None if the property is not required.
    widget.number = None
    # The value can be an integer.
    widget.number = 42
    # The value can be a float.
    widget.number = 3.141
    # The value cannot be anything else.
    with pytest.raises(core.ValidationError):
        widget.number = "test"


def test_numeric_property_with_bounds():
    """
    A numeric property with bounds cannot have a value outside those bounds.

    If the value is not required, the value could be set to None.
    """

    class FakeWidget:
        number = core.NumericProperty(
            "A test property", default_value=150, minimum=100, maximum=200
        )

        def __init__(self, test=None):
            self.number = test

    widget = FakeWidget()

    # The value can be None if the property is not required.
    widget.number = None
    # The value cannot be less than the minimum.
    widget.number = 100
    with pytest.raises(core.ValidationError):
        widget.number = 99.9
    # The value cannot be more than the maximum.
    widget.number = 200
    with pytest.raises(core.ValidationError):
        widget.number = 200.01

    # Now with only a minimum.

    class FakeWidgetMin:
        number = core.NumericProperty(
            "A test property", default_value=150, minimum=100
        )

        def __init__(self, test=None):
            self.number = test

    widget = FakeWidgetMin()

    # The value can be None if the property is not required.
    widget.number = None
    # The value cannot be less than the minimum.
    widget.number = 100
    with pytest.raises(core.ValidationError):
        widget.number = 99.9
    # There is no maximum boundary.
    widget.number = 999999

    # Now with only a minimum.

    class FakeWidgetMax:
        number = core.NumericProperty(
            "A test property", default_value=150, maximum=200
        )

        def __init__(self, test=None):
            self.number = test

    widget = FakeWidgetMax()

    # The value can be None if the property is not required.
    widget.number = None
    # No minimum boundary
    widget.number = -999999
    # The value cannot be more than the maximum.
    widget.number = 200
    with pytest.raises(core.ValidationError):
        widget.number = 200.01


def test_numeric_property_as_dict():
    """
    The expected JSON serializable Python dictionary defining the property's
    structure and attributes is returned.
    """
    np = core.NumericProperty(
        "A test property", default_value=150, minimum=100
    )
    assert np.as_dict(150) == {
        "property_type": "NumericProperty",
        "description": "A test property",
        "required": False,
        "value": 150,
        "minimum": 100,
        "maximum": None,
    }


def test_integer_property():
    """
    An integer property can only have an integer value.
    """
    ip = core.IntegerProperty("A test property", default_value=123)
    assert ip.default_value == 123
    with pytest.raises(core.ValidationError):
        core.IntegerProperty("A test property", default_value=1.23)


def test_float_property():
    """
    A float property can only have a floating point value.
    """
    fp = core.FloatProperty("A test property", default_value=1.23)
    assert fp.default_value == 1.23
    with pytest.raises(core.ValidationError):
        core.FloatProperty("A test property", default_value=123)


def test_text_property_defaults():
    """
    A text property has no default minimum or maximum length.
    """
    tp = core.TextProperty("A test property")
    assert tp.min_length is None
    assert tp.max_length is None


def test_text_property_value_is_string():
    """
    The value must be a string or None if not a required property.
    """

    class FakeWidget:
        text = core.TextProperty("A test property")

        def __init__(self, test=None):
            self.text = test

    widget = FakeWidget()
    # Strings are OK.
    widget.text = "test"
    # As is None.
    widget.text = None
    # Fail for anything else.
    with pytest.raises(core.ValidationError):
        widget.text = 123


def test_text_property_value_is_required_string():
    """
    The value must be a string if a required property.
    """

    class FakeWidget:
        text = core.TextProperty(
            "A test property", default_value="test", required=True
        )

        def __init__(self, test="test"):
            self.text = test

    widget = FakeWidget()
    widget.text = "another test"
    # Cannot be set to None if a required field.
    with pytest.raises(core.ValidationError):
        widget.text = None


def test_text_property_value_with_min_max_length():
    """
    If the min and max length are defined, the length of the value must be
    within the bounds.
    """

    # Both min and max length are defined.
    class FakeWidget:
        text = core.TextProperty(
            "A test property", min_length=4, max_length=10
        )

        def __init__(self, test="test"):
            self.text = test

    widget = FakeWidget()
    # A None value is ignored if it is not a required property.
    widget.text = None
    # The length of the value cannot be below the min_length.
    widget.text = "1234"
    with pytest.raises(core.ValidationError):
        widget.text = "123"
    # The length of the value cannot be above max_length.
    widget.text = "0123456789"
    with pytest.raises(core.ValidationError):
        widget.text = "0123456789+"

    # Only minimum length is defined.
    class FakeWidgetMin:
        text = core.TextProperty("A test property", min_length=4)

        def __init__(self, test="test"):
            self.text = test

    widget = FakeWidgetMin()
    # A None value is ignored if it is not a required property.
    widget.text = None
    # The length of the value cannot be below the min_length.
    widget.text = "1234"
    with pytest.raises(core.ValidationError):
        widget.text = "123"
    # No upper bound.
    widget.text = "0123456789+++++"

    # Only maximum length is defined.
    class FakeWidgetMax:
        text = core.TextProperty("A test property", max_length=10)

        def __init__(self, test="test"):
            self.text = test

    widget = FakeWidgetMax()
    # A None value is ignored if it is not a required property.
    widget.text = None
    # The length of the value cannot be below the min_length.
    widget.text = ""
    # The length of the value cannot be above max_length.
    widget.text = "0123456789"
    with pytest.raises(core.ValidationError):
        widget.text = "0123456789+"


def test_text_property_as_dict():
    """
    The expected JSON serializable Python dictionary defining the property's
    structure and attributes is returned.
    """
    tp = core.TextProperty("A test property", max_length=10)
    assert tp.as_dict(None) == {
        "property_type": "TextProperty",
        "description": "A test property",
        "required": False,
        "value": None,
        "min_length": None,
        "max_length": 10,
    }


def test_boolean_property_values():
    """
    If required a boolean property's value can only be True or False.

    If not required, None is also allowed. Anything else fails.
    """

    class FakeWidget:
        flag = core.BooleanProperty(
            "A test property", default_value=True, required=True
        )

        def __init__(self, test=True):
            self.flag = test

    widget = FakeWidget()
    widget.flag = False
    widget.flag = True
    # Cannot use None if a required property.
    with pytest.raises(core.ValidationError):
        widget.flag = None
    # Must be a boolean value.
    with pytest.raises(core.ValidationError):
        widget.flag = 1

    # Check behaviour of BooleanProperty if not a required field.
    class FakeWidgetNotRequired:
        flag = core.BooleanProperty("A test property")

        def __init__(self, test=True):
            self.flag = test

    widget = FakeWidgetNotRequired()
    widget.flag = False
    widget.flag = True
    # Can use None if NOT a required property.
    widget.flag = None
    # Must be a boolean value.
    with pytest.raises(core.ValidationError):
        widget.flag = 1


def test_choice_property_validation():
    """
    A value set to a choice property must be one of the defined valid choices.
    """

    class FakeWidget:
        select = core.ChoiceProperty(
            "A test property",
            choices=[
                1,
                2,
                3,
            ],
        )

        def __init__(self, test=1):
            self.select = test

    widget = FakeWidget()
    # If the property is not required, None is also valid.
    widget.select = None
    # A valid choice is a valid value.
    widget.select = 1
    # Outside the valid choices is invalid.
    with pytest.raises(core.ValidationError):
        widget.select = 0


def test_choice_property_as_dict():
    """
    The expected JSON serializable Python dictionary defining the property's
    structure and attributes is returned.
    """
    cp = core.ChoiceProperty(
        "A test property",
        choices=[
            1,
            2,
            3,
        ],
    )
    assert cp.as_dict(None) == {
        "property_type": "ChoiceProperty",
        "description": "A test property",
        "required": False,
        "value": None,
        "choices": [1, 2, 3],
    }


def test_widget_init_defaults():
    """
    Ensure an instance of a Widget class has a default id, position and
    channel.
    """
    w = core.Widget(name="test")
    # There is a default id of the expected default "shape".
    assert w.id is not None
    assert w.id.startswith("invent-")
    assert len(w.id[7:]) == 10
    # The default position is top left.
    assert w.position == "TOP-LEFT"
    # The default channel for widget related messages is the same as
    # the widget's id.
    assert w.channel == w.id


def test_widget_init_override():
    """
    It's possible to override the default values for id, position and channel.
    """
    w = core.Widget(
        name="test", id="foo", position="FILL", channel="test_channel"
    )
    assert w.id == "foo"
    assert w.position == "FILL"
    assert w.channel == "test_channel"


def test_widget_properties():
    """
    A widget's properties are available in a dictionary.
    """

    class MyWidget(core.Widget):
        """
        A test widget.
        """

        foo = core.TextProperty("This is a foo", default_value="bar")
        numberwang = core.IntegerProperty(
            "That's numberwang!", default_value=42
        )
        favourite_colour = core.ChoiceProperty(
            "Best colour.",
            choices=[
                "black",
                "very very dark grey",
                "deeply off white",
                "coal",
            ],
        )

    mw = MyWidget(name="test widget")
    mw.foo = "baz"
    mw.numberwang = -1
    mw.favourite_colour = "black"

    assert mw.foo == "baz"
    assert mw.numberwang == -1
    assert mw.favourite_colour == "black"
    assert isinstance(mw.properties["foo"], core.TextProperty)
    assert isinstance(mw.properties["numberwang"], core.IntegerProperty)
    assert isinstance(mw.properties["favourite_colour"], core.ChoiceProperty)


def test_widget_as_dict():
    """
    A JSON serializable data structure representing the widget and its
    properties is returned.
    """

    class MyWidget(core.Widget):
        """
        A test widget.
        """

        foo = core.TextProperty("This is a foo", default_value="bar")
        numberwang = core.IntegerProperty(
            "That's numberwang!", default_value=42
        )
        favourite_colour = core.ChoiceProperty(
            "Best colour.",
            choices=[
                "black",
                "very very dark grey",
                "deeply off white",
                "coal",
            ],
        )

    mw = MyWidget(name="test widget")
    mw.foo = "baz"
    mw.numberwang = -1
    mw.favourite_colour = "black"

    mw2 = MyWidget(name="another test widget")
    mw2.foo = "qux"
    mw2.numberwang = 666
    mw2.favourite_colour = "coal"

    result = mw.as_dict()
    assert result["name"] == "test widget"
    assert result["id"] == mw.id
    assert result["channel"] == mw.channel
    assert result["position"] == mw.position
    assert len(result["properties"]) == 3
    assert result["properties"]["foo"]["property_type"] == "TextProperty"
    assert result["properties"]["foo"]["value"] == "baz"
    assert (
        result["properties"]["numberwang"]["property_type"]
        == "IntegerProperty"
    )
    assert result["properties"]["numberwang"]["value"] == -1
    assert (
        result["properties"]["favourite_colour"]["property_type"]
        == "ChoiceProperty"
    )
    assert result["properties"]["favourite_colour"]["value"] == "black"

    result2 = mw2.as_dict()
    assert result2["name"] == "another test widget"
    assert result2["id"] == mw2.id
    assert result2["channel"] == mw2.channel
    assert result2["position"] == mw2.position
    assert len(result2["properties"]) == 3
    assert result2["properties"]["foo"]["property_type"] == "TextProperty"
    assert result2["properties"]["foo"]["value"] == "qux"
    assert (
        result2["properties"]["numberwang"]["property_type"]
        == "IntegerProperty"
    )
    assert result2["properties"]["numberwang"]["value"] == 666
    assert (
        result2["properties"]["favourite_colour"]["property_type"]
        == "ChoiceProperty"
    )
    assert result2["properties"]["favourite_colour"]["value"] == "coal"


def test_widget_parse_position():
    """
    Any valid definition of a widget's position should result in the correct
    horizontal and vertical values.
    """
    w = core.Widget(name="test widget")
    for h in core._VALID_HORIZONTALS:
        w.position = h
        assert w.parse_position() == (None, h)
        for v in core._VALID_VERTICALS:
            w.position = v
            assert w.parse_position() == (v, None)
            w.position = f"{v}-{h}"
            assert w.parse_position() == (v, h)
    with pytest.raises(ValueError):
        # Invalid position values result in a ValueError.
        w.position = "NOT-VALID"
        w.parse_position()
