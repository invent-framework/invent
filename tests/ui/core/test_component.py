import upytest
from pyscript.web import div
from invent.ui import core


def test_event():
    """
    Events have a description and key/value specifications of the
    content of the messages they send.

    class MyWidget(Widget):

        name = TextProperty()
        hold = Event(
            "When the button is held",
            duration="For how long the button was pressed.",
        )

        def _handle_hold(self, e):
            self.publish("hold", duration=e.duration)

        def render(self, container):
            self.element = pyscript.web.button("Click me")
            self.element.addEventListener("click", self._handle_hold)
    """
    ev = core.Event("This is a test", foo="A foo to handle")
    assert ev.description == "This is a test"
    assert "foo" in ev.content
    assert ev.content["foo"] == "A foo to handle"


def test_event_create_message():
    """
    An Event creates the expected message.
    """
    ev = core.Event("This is a test", foo="A foo to handle")
    # Cannot include fields that have not been specified.
    with upytest.raises(ValueError):
        ev.create_message("subject", baz="This will fail")
    # Can include all the fields.
    msg = ev.create_message("subject", foo="Foo to you")
    assert msg._subject == "subject"
    assert msg.foo == "Foo to you"
    # Cannot miss an expected field.
    with upytest.raises(ValueError):
        ev.create_message("subject")


def test_event_as_dict():
    """
    The expected dictionary definition of an Event is generated.
    """
    ev = core.Event("This is a test", foo="A foo to handle")
    assert ev.as_dict() == {
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
            return div()

    tc = TestComponent(name="test1", id="12345", visible=False)
    assert tc.name == "test1"
    assert tc.id == "12345"
    assert tc.visible is False
    assert tc.parent is None


def test_component_init_with_no_values():
    """
    Initialisation with no defaults ensures they are generated for the user.
    """

    class TestComponent(core.Component):

        def render(self):
            return div()

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
        text = core.TextProperty(
            "A text property", default_value="test", required=True
        )
        integer = core.IntegerProperty("An integer property")
        val = core.FloatProperty("A float property", default_value=1.23)
        flag = core.BooleanProperty("A test property", default_value=False)

        def render(self):
            return div()

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
    with upytest.raises(core.ValidationError):
        TestComponent(text=None)

    # Cannot initialize a nonexistent property.
    with upytest.raises(AttributeError):
        TestComponent(no_such_prop=None)


def test_component_get_component_by_id():
    """
    Once a component is created, it's possible to retrieve it directly via id.
    """

    class TestComponent(core.Component):

        def render(self):
            return div()

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


def test_component_events():
    """
    A component's (widget's) events are available in a dictionary.
    """

    class MyWidget(core.Widget):
        """
        A test widget.
        """

        ping = core.Event("Send a ping.", strength="The strength of the ping.")

    mbp = MyWidget.events()
    assert isinstance(mbp["ping"], core.Event)


def test_component_definition():
    """
    A JSON serializable data structure representing the component class is
    returned. Should include the name, properties, events and icon for the
    component.
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
        bloop = core.Event(
            "Bloop the blooper", strength="The strength of the bloop."
        )

        @classmethod
        def icon(cls):
            return "<button>Click me!</button>"

        def render(self):
            return div()

    result = MyWidget.definition()
    assert "properties" in result
    assert "events" in result
    assert "icon" in result
    assert result["name"] == "MyWidget"
    assert result["properties"]["name"]["property_type"] == "TextProperty"
    assert result["properties"]["name"]["default_value"] is None
    assert result["properties"]["id"]["property_type"] == "TextProperty"
    assert result["properties"]["id"]["default_value"] is None
    assert result["properties"]["channel"]["property_type"] == "TextProperty"
    assert result["properties"]["channel"]["default_value"] is None
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
    assert result["events"]["bloop"]["description"] == "Bloop the blooper"
    assert (
        result["events"]["bloop"]["content"]["strength"]
        == "The strength of the bloop."
    )
    assert result["icon"] == "<button>Click me!</button>"


def test_component_as_dict():
    """
    Ensure the expected state of the component (widget) is returned as a Python
    dictionary.
    """

    class MyWidget(core.Component):
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
        bloop = core.Event(
            "Bloop the blooper", strength="The strength of the bloop."
        )

        @classmethod
        def icon(cls):
            return "<button>Click me!</button>"

        def render(self):
            return div()

    mw = MyWidget(foo=core.from_datastore("ds_key"), numberwang=55)
    expected = {
        "properties": {
            "favourite_colour": "black",
            "row_span": None,
            "horizontal_align": None,
            "space": None,
            "visible": True,
            "vertical_align": None,
            "name": "MyWidget 1",
            "numberwang": 55,
            "enabled": True,
            "border_color": None,
            "column_span": None,
            "border_style": None,
            "background_color": None,
            "foo": "from_datastore('ds_key')",
            "id": "invent-mywidget-1",
            "border_width": None,
        },
        "type": "MyWidget",
    }
    assert mw.as_dict() == expected, mw.as_dict()


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
            return div()

    w = MyWidget()
    # There is no attribute called "test" on the widget's element.
    assert w.element.hasAttribute("test") is False
    # Update an attribute (add it).
    w.update_attribute("test", "yes")
    assert w.element.getAttribute("test") == "yes"
    # Update an attribute (change it).
    w.update_attribute("test", "yes2")
    assert w.element.getAttribute("test") == "yes2"
    # Update an attribute (remove it because it is false-y).
    w.update_attribute("test", "")
    assert w.element.hasAttribute("test") is False


def test_component_default_icon():
    """
    The SVG image returned by the Component's icon class method (to be
    overridden by children), is the expected default safe catch-all image.
    """

    class TestComponent(core.Component):

        def render(self):
            return div()

    assert TestComponent.icon() == core._DEFAULT_ICON
