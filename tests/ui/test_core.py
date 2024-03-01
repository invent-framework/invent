import pytest
from pyscript import document
from unittest import mock
from invent.ui import core


def test_message_blueprint():
    """
    MessageBlueprints have a description and key/value descriptions of the
    content of the messages they send.

    class MyWidget(Widget):

        name = TextProperty()
        hold = MessageBlueprint(
            "When the button is held",
            duration="For how long the button was pressed.",
        )

        def _handle_hold(self, event):
            self.publish("hold", duration=event.duration)

        def render(self, container):
            self.element = document.createElement("button")
            self.element.addEventListener("click", self._handle_hold)
    """
    mbp = core.MessageBlueprint("This is a test", foo="A foo to handle")
    assert mbp.description == "This is a test"
    assert "foo" in mbp.content
    assert mbp.content["foo"] == "A foo to handle"


def test_message_blueprint_create_message():
    """
    A MessageBlueprint creates the expected message.
    """
    mbp = core.MessageBlueprint("This is a test", foo="A foo to handle")
    # Cannot include fields that have not been specified.
    with pytest.raises(ValueError):
        mbp.create_message("subject", baz="This will fail")
    # Can include all the fields.
    msg = mbp.create_message("subject", foo="Foo to you")
    assert msg._subject == "subject"
    assert msg.foo == "Foo to you"
    # Cannot miss an expected field.
    with pytest.raises(ValueError):
        mbp.create_message("subject")


def test_message_blueprint_as_dict():
    """
    The expected dictionary definition of a MessageBlueprint is generated.
    """
    mbp = core.MessageBlueprint("This is a test", foo="A foo to handle")
    assert mbp.as_dict() == {
        "description": "This is a test",
        "content": {
            "foo": "A foo to handle",
        },
    }


def test_from_datastore():
    """
    Ensure this signal class has just a key attribute.
    """
    fds = core.from_datastore("foo")
    assert fds.key == "foo"


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


def test_property_from_datastore():
    """
    If the property is set a value from_datastore, the expected reactor
    function is subscribed to the correct datastore key.
    """

    class FakeWidget:
        my_property = core.Property("A test property")

    fw = FakeWidget()
    with mock.patch("invent.subscribe") as mock_sub:
        fw.my_property = core.from_datastore("test")
        assert mock_sub.call_args[1]["to_channel"] == "store-data"
        assert mock_sub.call_args[1]["when_subject"] == "test"
        assert mock_sub.call_count == 1


def test_property_as_dict():
    """
    The expected JSON serializable Python dictionary defining the property's
    structure and attributes is returned.
    """
    p = core.Property("A test property", default_value="test", required=True)
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

    class FakeWidget(core.Widget):

        integer = core.IntegerProperty(
            "A test integer property", default_value=123
        )

        def __init__(self, val):
            self.integer = val

    fw = FakeWidget(123)
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

    class FakeWidget(core.Widget):

        val = core.FloatProperty("A test float property", default_value=1.23)

        def __init__(self, val):
            self.val = val

    fw = FakeWidget(123.4)
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
    # Coerce for any other non-string value.
    widget.text = 123
    assert widget.text == "123"


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
    # Coercion to boolean works.
    widget.flag = 1
    assert widget.flag is True

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
    # Coercion works.
    widget.flag = 1
    assert widget.flag is True


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
    assert cp.as_dict() == {
        "property_type": "ChoiceProperty",
        "description": "A test property",
        "required": False,
        "default_value": None,
        "choices": [1, 2, 3],
    }


def test_component_init_with_given_values():
    """
    Given a name and id, these are reflected in the resulting object.
    """

    class TestComponent(core.Component):

        def render(self):
            return document.createElement("div")

    tc = core.TestComponent(name="test1", id="12345", position="TOP-LEFT")
    assert tc.name == "test1"
    assert tc.id == "12345"
    assert tc.position == "TOP-LEFT"


def test_component_init_with_no_values():
    """
    Initialisation with no defaults ensures they are generated for the user.
    """
    c = core.Component()
    assert c.name == "Component 1"
    assert c.id is not None
    c2 = core.Component()
    assert c2.name == "Component 2"
    assert c2.id is not None


def test_component_get_component_by_id():
    """
    Once a component is created, it's possible to retrieve it directly via id.
    """
    c = core.Component()
    assert core.Component.get_component_by_id(c.id) == c


def test_component_properties():
    """
    A component's (widget's) properties are available in a dictionary.
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

    properties = MyWidget.properties()

    assert isinstance(properties["foo"], core.TextProperty)
    assert isinstance(properties["numberwang"], core.IntegerProperty)
    assert isinstance(properties["favourite_colour"], core.ChoiceProperty)


def test_component_message_blueprints():
    """
    A component's (widget's) message blueprints are available in a dictionary.
    """

    class MyWidget(core.Widget):
        """
        A test widget.
        """

        ping = core.MessageBlueprint(
            "Send a ping.", strength="The strength of the ping."
        )

    mbp = MyWidget.message_blueprints()
    assert isinstance(mbp["ping"], core.MessageBlueprint)


def test_component_blueprint():
    """
    A JSON serializable data structure representing the component (widget) and
    its properties is returned.
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
            default_value="black",
            choices=[
                "black",
                "very very dark grey",
                "deeply off white",
                "coal",
            ],
        )

        @classmethod
        def preview(cls):
            return "<button>Click me!</button>"

    result = MyWidget.blueprint()
    assert result["properties"]["name"]["property_type"] == "TextProperty"
    assert result["properties"]["name"]["default_value"] is None
    assert result["properties"]["id"]["property_type"] == "TextProperty"
    assert result["properties"]["id"]["default_value"] is None
    assert result["properties"]["channel"]["property_type"] == "TextProperty"
    assert result["properties"]["channel"]["default_value"] is None
    assert result["properties"]["position"]["property_type"] == "TextProperty"
    assert result["properties"]["position"]["default_value"] is None
    assert result["properties"]["foo"]["property_type"] == "TextProperty"
    assert result["properties"]["foo"]["default_value"] == "bar"
    assert (
        result["properties"]["numberwang"]["property_type"]
        == "IntegerProperty"
    )
    assert result["properties"]["numberwang"]["default_value"] == 42
    assert (
        result["properties"]["favourite_colour"]["property_type"]
        == "ChoiceProperty"
    )
    assert result["properties"]["favourite_colour"]["default_value"] == "black"


def test_component_as_dict():
    """
    Ensure the expected state of the component (widget) is returned as a Python
    dictionary.
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
            default_value="black",
            choices=[
                "black",
                "very very dark grey",
                "deeply off white",
                "coal",
            ],
        )

    w = MyWidget("a test widget")
    result = w.as_dict()
    assert result["type"] == "MyWidget"
    assert result["properties"]["foo"] == "bar"
    assert result["properties"]["numberwang"] == 42
    assert result["properties"]["favourite_colour"] == "black"


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
    # the widget's name.
    assert w.channel == "test"


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


def test_widget_publish():
    """
    A widget knows what channels to publish any messages to, from
    MessageBlueprints.
    """

    class MyWidget(core.Widget):

        ping = core.MessageBlueprint(
            "Send a ping.", strength="Strength of ping"
        )

    with mock.patch("invent.publish") as mock_publish:
        w = MyWidget()
        w.publish("ping", strength=100)
        x = 2
        assert mock_publish.call_count == 1


def test_widget_parse_position():
    """
    Any valid definition of a widget's position should result in the correct
    horizontal and vertical values.
    """
    w = core.Widget(name="test widget")
    w.element = document.createElement("div")
    container = document.createElement("div")
    container.appendChild(w.element)
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


def test_widget_set_position_fill():
    """
    Ensure the widget's element has the CSS width and height set to the
    expected value of 100%.
    """
    w = core.Widget(position="FILL")
    w.element = document.createElement("div")
    container = document.createElement("div")
    container.appendChild(w.element)
    w.set_position(container)
    assert w.element.style.width == "100%"
    assert w.element.style.height == "100%"


def test_widget_set_position():
    """
    The widget's container has the expected alignment/justify value set for
    each combination of the valid horizontal and vertical positions.
    """
    expected_vertical = {
        "TOP": "start",
        "MIDDLE": "center",
        "BOTTOM": "end",
        "": "stretch",
    }
    expected_horizontal = {
        "LEFT": "start",
        "CENTER": "center",
        "RIGHT": "end",
        "": "stretch",
    }
    for h_key, h_val in expected_horizontal.items():
        for v_key, v_val in expected_vertical.items():
            w = core.Widget()
            w.element = document.createElement("div")
            container = document.createElement("div")
            container.appendChild(w.element)
            if v_key and h_key:
                w.position = f"{v_key}-{h_key}"
            else:
                w.position = f"{v_key}{h_key}"
            # Ignore NoneNone
            if w.position:
                w.set_position(container)
                if v_key:
                    assert (
                        container.style.getPropertyValue("align-self") == v_val
                    )
                else:
                    assert (
                        container.style.getPropertyValue("align-self") == v_val
                    )
                    assert w.element.style.height == "100%"
                if h_key:
                    assert (
                        container.style.getPropertyValue("justify-self")
                        == h_val
                    )
                else:
                    assert (
                        container.style.getPropertyValue("justify-self")
                        == h_val
                    )
                    assert w.element.style.width == "100%"


def test_container_init():
    """
    A default initialisation results in the expected default state.
    """
