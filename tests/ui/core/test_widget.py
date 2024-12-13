import umock
from pyscript.web import div
from invent.ui import core


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


def test_widget_when_with_do():
    """
    A widget's when method can be used to short-cut message subscriptions.
    """

    class TestWidget(core.Widget):

        def render(self):
            return div()

    tw = TestWidget(name="test1", id="12345")

    def my_handler(message):
        return

    # Simple case with default channel name (component's id).
    with umock.patch("invent.ui.core.component:invent.subscribe") as mock_sub:
        tw.when("push", do=my_handler)
        mock_sub.assert_called_once_with(
            handler=my_handler, to_channel="12345", when_subject="push"
        )

    # Specialised case with explicit channel name[s].
    with umock.patch("invent.ui.core.component:invent.subscribe") as mock_sub:
        tw.when("push", to_channel="test_channel", do=my_handler)
        mock_sub.assert_called_once_with(
            handler=my_handler, to_channel="test_channel", when_subject="push"
        )


def test_widget_when_as_decorator():
    """
    A widget's when method can be used to short-cut decorating handler
    functions.
    """

    class TestWidget(core.Widget):

        def render(self):
            return div()

    tw = TestWidget(name="test1", id="12345")

    # Simple case with default channel name (component's id).
    with umock.patch("invent.ui.core.component:invent.subscribe") as mock_sub:

        @tw.when("push")
        def my_first_handler(message):
            return

        assert mock_sub.call_count == 1

        mock_sub.reset_mock()

        @tw.when("push", to_channel="test_channel")
        def my_second_handler(message):
            return

        assert mock_sub.call_count == 1
