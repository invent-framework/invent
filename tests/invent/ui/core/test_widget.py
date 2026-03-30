import umock
from pyscript.web import div
from invent.ui import core
from invent import channels, Message


def test_widget_init_defaults():
    """
    Ensure an instance of a Widget class has default values for id, visible and
    channel.
    """

    class MyWidget(core.Widget):

        def render(self):
            return div()

    w = MyWidget(name="test")
    # There is a default id of the expected default "shape".
    assert w.id is not None
    assert w.id.startswith("invent-")
    assert len(w.id[7:]) == 10
    # The default visibility is True.
    assert w.visible is True
    # The default channel for widget related messages is the same as its id.
    assert w.channel == w.id


def test_widget_init_with_event_handlers():
    """
    Widgets can be initialized with named event handlers.
    """

    class TestWidget(core.Widget):
        on_click = core.Event("When the widget is clicked")

        def render(self):
            return div()

    handler = umock.Mock()
    tw = TestWidget(on_click=handler)
    # The handler should be subscribed to the widget's channel, with the
    # subject of the event name.
    channels.publish(
        Message(subject="on_click"),
        to_channel=tw.channel,
    )
    handler.assert_called_once()

    # It's also possible to pass in a list of handlers for an event.
    handler2 = umock.Mock()
    handler3 = umock.Mock()
    tw2 = TestWidget(on_click=[handler2, handler3])
    channels.publish(
        Message(subject="on_click"),
        to_channel=tw2.channel,
    )
    handler2.assert_called_once()
    handler3.assert_called_once()


def test_widget_init_override():
    """
    It's possible to override the default values for id, visible and channel.
    """

    class MyWidget(core.Widget):

        def render(self):
            return div()

    w = MyWidget(name="test", id="foo", visible=False, channel="test_channel")
    assert w.id == "foo"
    assert w.visible is False
    assert w.channel == "test_channel"


def test_widget_publish():
    """
    A widget knows what channels to publish any messages to, from
    MessageBlueprints.
    """

    class MyWidget(core.Widget):

        ping = core.Event("Send a ping.", strength="Strength of ping")

        def render(self):
            return div()

    with umock.patch("invent:publish") as mock_publish:
        w = MyWidget()
        w.channel = "my_channel"
        w.publish("ping", strength=100)
        assert mock_publish.call_count == 1
