import pytest
from pyscript import document
from unittest import mock
from invent.ui import core
from invent.ui.properties import (
    BooleanProperty,
    FloatProperty,
    IntegerProperty,
    TextProperty,
    ValidationError,
)


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


def test_component_init_with_given_values():
    """
    Given a name and id, these are reflected in the resulting object.
    """

    class TestComponent(core.Component):

        def render(self):
            return document.createElement("div")

    tc = TestComponent(name="test1", id="12345", position="TOP-LEFT")
    assert tc.name == "test1"
    assert tc.id == "12345"
    assert tc.position == "TOP-LEFT"
    assert tc.parent is None


def test_component_init_with_no_values():
    """
    Initialisation with no defaults ensures they are generated for the user.
    """

    class TestComponent(core.Component):

        def render(self):
            return document.createElement("div")

    tc = TestComponent()
    assert tc.name == "TestComponent 1"
    assert tc.id is not None
    tc2 = TestComponent()
    assert tc2.name == "TestComponent 2"
    assert tc2.id is not None


def test_component_init_with_properties():
    """
    Properties can be initialized with constructor keyword arguments.
    """

    class TestComponent(core.Component):
        text = TextProperty(
            "A text property", default_value="test", required=True
        )
        integer = IntegerProperty("An integer property")
        val = FloatProperty("A float property", default_value=1.23)
        flag = BooleanProperty("A test property", default_value=False)

        def render(self):
            return document.createElement("div")

    tc = TestComponent(text="bar", integer=123, val=123.4, flag=True)
    assert tc.text == "bar"
    assert tc.integer == 123
    assert tc.val == 123.4
    assert tc.flag is True

    # Uninitialized properties will be set to defaults.
    tc = TestComponent()
    assert tc.text == "test"
    assert tc.integer is None
    assert tc.val == 1.23
    assert tc.flag is False

    # Cannot initialize a required property with None.
    with pytest.raises(ValidationError):
        TestComponent(text=None)


def test_component_get_component_by_id():
    """
    Once a component is created, it's possible to retrieve it directly via id.
    """

    class TestComponent(core.Component):

        def render(self):
            return document.createElement("div")

    tc = TestComponent()
    assert TestComponent.get_component_by_id(tc.id) == tc


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
        def icon(cls):
            return "<button>Click me!</button>"

    result = MyWidget.blueprint()
    assert result["properties"]["name"]["property_type"] == "TextProperty"
    assert result["properties"]["name"]["default_value"] is None
    assert result["properties"]["id"]["property_type"] == "TextProperty"
    assert result["properties"]["id"]["default_value"] is None
    assert result["properties"]["channel"]["property_type"] == "TextProperty"
    assert result["properties"]["channel"]["default_value"] is None
    assert result["properties"]["position"]["property_type"] == "TextProperty"
    assert result["properties"]["position"]["default_value"] == "FILL"
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
    assert result["icon"] == "<button>Click me!</button>"


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

        def render(self):
            return document.createElement("div")

    w = MyWidget()
    result = w.as_dict()
    assert result["type"] == "MyWidget"
    assert result["properties"]["foo"] == "bar"
    assert result["properties"]["numberwang"] == 42
    assert result["properties"]["favourite_colour"] == "black"


def test_component_update_attribute():
    """
    Ensure the referenced attribute is updated and removed as expected.
    """

    class MyWidget(core.Widget):
        """
        A test widget.
        """

        foo = core.TextProperty("This is a foo", default_value="bar")

        def render(self):
            return document.createElement("div")

    w = MyWidget()
    # There is no attribute called "test" on the widget's element.
    w.element.removeAttribute("id")
    w.element.removeAttribute("name")
    assert w.element.hasAttributes() is False
    # Update an attribute (add it).
    w.update_attribute("test", "yes")
    assert w.element.getAttribute("test") == "yes"
    # Update an attribute (change it).
    w.update_attribute("test", "yes2")
    assert w.element.getAttribute("test") == "yes2"
    # Update an attribute (remove it because it is false-y).
    w.update_attribute("test", "")
    assert w.element.hasAttributes() is False


def test_component_default_icon():
    """
    The SVG image returned by the Component's icon class method (to be
    overridden by children), is the expected default safe catch-all image.
    """

    class TestComponent(core.Component):

        def render(self):
            return document.createElement("div")

    assert TestComponent.icon() == core._DEFAULT_ICON


def test_widget_init_defaults():
    """
    Ensure an instance of a Widget class has a default id, position and
    channel.
    """

    class MyWidget(core.Widget):

        def render(self):
            return document.createElement("div")

    w = MyWidget(name="test")
    # There is a default id of the expected default "shape".
    assert w.id is not None
    assert w.id.startswith("invent-")
    assert len(w.id[7:]) == 10
    # The default position is FILL.
    assert w.position == "FILL"
    # The default channel for widget related messages is None.
    assert w.channel is None


def test_widget_init_override():
    """
    It's possible to override the default values for id, position and channel.
    """

    class MyWidget(core.Widget):

        def render(self):
            return document.createElement("div")

    w = MyWidget(
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

        def render(self):
            return document.createElement("div")

    with mock.patch("invent.publish") as mock_publish:
        w = MyWidget()
        w.channel = "my_channel"
        w.publish("ping", strength=100)
        assert mock_publish.call_count == 1


def test_widget_parse_position():
    """
    Any valid definition of a widget's position should result in the correct
    horizontal and vertical values.
    """

    class MyWidget(core.Widget):

        def render(self):
            return document.createElement("div")

    w = MyWidget(name="test widget")
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

    class MyWidget(core.Widget):

        def render(self):
            return document.createElement("div")

    w = MyWidget(position="FILL")
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

    class MyWidget(core.Widget):

        def render(self):
            return document.createElement("div")

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
            w = MyWidget()
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


def test_container_on_content_changed():
    """
    The children are re-rendered when the content list is changed.
    """
    pass  # TODO: Finish me.
