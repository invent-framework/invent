import pytest
from invent.ui import Button, core


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
    # The default pubsub channel for widget related messages is the same as
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


@pytest.mark.skip("Finish off when Widget class is figured out.")
def test_widget_set_position_fill():
    """
    Ensure the expected CSS classes are added to the self.element that's added
    to the DOM.
    """
    b = Button(name="test", label="click me")
    container = core.Column(name="test_column")
    container.append(b)
    b.set_position(container)
    assert b.element.style.width == "100%"
    assert b.element.style.height == "100%"
