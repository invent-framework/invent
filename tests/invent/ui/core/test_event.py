import upytest
from pyscript.web import div
from invent.ui import core


def test_event():
    """
    Events have a description and key/value specifications of the
    content of the messages they send.
    """

    class TestWidget(core.Widget):
        hold = core.Event(
            "When the button is held",
            duration="For how long the button was pressed.",
        )

        def render(self):
            return div()

    tw = TestWidget()
    assert tw.hold._event_name == "hold"
    assert tw.hold.description == "When the button is held"
    assert "duration" in tw.hold.content
    assert (
        tw.hold.content["duration"] == "For how long the button was pressed."
    )


def test_event_create_message():
    """
    An Event creates the expected message.
    """

    class TestWidget(core.Widget):
        hold = core.Event(
            "When the button is held",
            duration="For how long the button was pressed.",
        )

        def render(self):
            return div()

    tw = TestWidget()
    # Cannot include fields that have not been specified.
    with upytest.raises(ValueError) as exc:
        tw.hold.create_message(tw, baz="This will fail")
        assert exc.exception.args[0] == "Unknown field in event subject: baz"
    # Can include all the fields.
    msg = tw.hold.create_message(tw, duration="Foo to you")
    assert msg.source == tw  # Will be reference to the widget.
    assert msg._subject == tw.hold._event_name
    assert msg.duration == "Foo to you"
    # Cannot miss an expected field.
    with upytest.raises(ValueError) as exc:
        tw.hold.create_message(tw)
        assert (
            exc.exception.args[0]
            == "Field missing from event subject: duration"
        )


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
