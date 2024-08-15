import asyncio
import invent
import upytest
import umock


def test_message_str():
    """
    The user friendly string representation of a message is the type of the
    message followed by a str() of the dict from the **kwargs.
    """
    m = invent.Message("message", data="foo")
    assert str(m) == "message {'data': 'foo'}"


def test_message_attributes():
    """
    Arbitrary kwarg values passed into a message become message attributes.
    """
    m = invent.Message("message", data="foo")
    assert m.data == "foo"


def test_subject():
    """
    The message's _subject is the subject passed in as the first argument
    when instantiating the Message class.
    """
    m = invent.Message("message", data="test")
    assert m._subject == "message"


def test_subscribe_and_publish_single_channel_and_subject():
    """
    Subscribe to a single channel and message subject with a handler.

    Ensure it works because the handler is called when the expected message is
    published to the right channel.
    """
    handler = umock.Mock()
    invent.subscribe(handler, to_channel="testing", when_subject="test")
    m1 = invent.Message(subject="test", data="Test")
    # This should succeed and cause the handler to fire.
    invent.publish(m1, to_channel="testing")
    # This will not succeed, because it's the wrong channel.
    invent.publish(m1, to_channel="wrong_channel")
    # This will not succeed, because it's the wrong message type.
    m2 = invent.Message(subject="wrong_type", data="Test")
    invent.publish(m2, to_channel="testing")
    # The handler is correctly subscribed because it has only been called for
    # the single occassion when both the channel and message type matched the
    # subscription specification.
    handler.assert_called_once_with(m1)


def test_subscribe_and_publish_multi_channel_and_subject():
    """
    Subscribe to multiple channels and message types with a single handler.

    Ensure it works because the handler is called when the expected message is
    published to the right channel.
    """
    handler = umock.Mock()
    invent.subscribe(
        handler,
        to_channel=[
            "testing1",
            "testing2",
        ],
        when_subject=[
            "test1",
            "test2",
        ],
    )
    m1 = invent.Message(subject="test1", data="Test")
    m2 = invent.Message(subject="test2", data="Test")
    # These should succeed and cause the handler to fire four times.
    invent.publish(m1, to_channel="testing1")
    invent.publish(m1, to_channel="testing2")
    invent.publish(m2, to_channel="testing1")
    invent.publish(m2, to_channel="testing2")
    # This will not succeed, because it's the wrong channel.
    invent.publish(m1, to_channel="wrong_channel")
    # This will not succeed, because it's the wrong message type.
    m3 = invent.Message("wrong_type", data="Test")
    invent.publish(m3, to_channel="testing1")
    invent.publish(m3, to_channel="testing2")
    # The handler is correctly subscribed because it has been called for the
    # four occassions when both the channel and message type matched the
    # subscription specifications.
    assert handler.call_count == 4


async def test_subscribe_and_publish_task_and_awaitable():
    """
    Ensure that if a Task instance or a Python awaitable is subscribed, they
    are handled correctly.
    """
    mock_await = umock.Mock()

    async def an_awaitable_for_a_task():
        """
        An asynchronous function to be wrapped in a Task.
        """
        mock_await()
        return

    # A task instance to subscribe to something.
    t = invent.Task(an_awaitable_for_a_task)

    async def an_awaitable(message):
        """
        An asynchronous function to handle a message.
        """
        mock_await()
        return

    invent.subscribe(t, to_channel="testing", when_subject="test_task")
    invent.subscribe(
        an_awaitable, to_channel="testing", when_subject="test_await"
    )
    m1 = invent.Message(subject="test_task", data="Test")
    m2 = invent.Message(subject="test_await", data="Test")
    invent.publish(m1, to_channel="testing")
    invent.publish(m2, to_channel="testing")
    await asyncio.sleep(0.1)
    assert mock_await.call_count == 2, mock_await.call_count


def test_subscribe_is_idempotent():
    """
    Multiple calls to subscribe only ever result in a single subscription.
    """
    handler = umock.Mock()
    invent.subscribe(handler, to_channel="testing", when_subject="test")
    invent.subscribe(handler, to_channel="testing", when_subject="test")
    m1 = invent.Message(subject="test", data="Test")
    invent.publish(m1, to_channel="testing")
    # The handler is correctly subscribed because it has only been called once
    # when a message is passed, despite being subscribed twice.
    handler.assert_called_once_with(m1)


def test_unsubscribe_single_channel_and_subject():
    """
    Unsubscribing from a single channel / message type ensures the message
    handler is no longer called when a matching message is sent to the channel.
    """
    handler = umock.Mock()
    invent.subscribe(handler, to_channel="testing", when_subject="test")
    m = invent.Message(subject="test", data="Test")
    # This should succeed and cause the handler to fire.
    invent.publish(m, to_channel="testing")
    # Unsubscribe.
    invent.unsubscribe(handler, from_channel="testing", when_subject="test")
    # The handler should not fire.
    invent.publish(m, to_channel="testing")
    # The handler should only have been called once.
    handler.assert_called_once_with(m)


def test_unsubscribe_multi_channel_and_subject():
    """
    Unsubscribing from multiple channels / message types ensures the message
    handler is no longer called when matching messages are sent to the
    channels.
    """
    handler = umock.Mock()
    invent.subscribe(
        handler,
        to_channel=[
            "testing1",
            "testing2",
        ],
        when_subject=[
            "test1",
            "test2",
        ],
    )
    m1 = invent.Message(subject="test1", data="Test")
    m2 = invent.Message(subject="test2", data="Test")
    # These should succeed and cause the handler to fire four times.
    invent.publish(m1, to_channel="testing1")
    invent.publish(m1, to_channel="testing2")
    invent.publish(m2, to_channel="testing1")
    invent.publish(m2, to_channel="testing2")
    # Unsubscribe.
    invent.unsubscribe(
        handler,
        from_channel=[
            "testing1",
            "testing2",
        ],
        when_subject=[
            "test1",
            "test2",
        ],
    )
    # None of these should cause the handler to fire.
    invent.publish(m1, to_channel="testing1")
    invent.publish(m1, to_channel="testing2")
    invent.publish(m2, to_channel="testing1")
    invent.publish(m2, to_channel="testing2")
    # The handler was correctly unsubscribed because it was only called for the
    # four occassions when both the channel and message type matched the
    # subscription specifications BEFORE the unsubscription.
    assert handler.call_count == 4


def test_unsubscribe_missing_subject():
    """
    Unsubscribing from a channel but missing a valid message type results in
    an error.
    """
    handler = umock.Mock()
    invent.subscribe(handler, to_channel="testing", when_subject="test")
    # Unsubscribe should fail with a ValueError.
    with upytest.raises(ValueError):
        invent.unsubscribe(
            handler, from_channel="testing", when_subject="wrong_type"
        )


def test_unsubscribe_missing_channel():
    """
    Unsubscribing from a missing channel results in an error.
    """
    handler = umock.Mock()
    # Unsubscribe should fail with a ValueError.
    with upytest.raises(ValueError):
        invent.unsubscribe(
            handler, from_channel="testing", when_subject="test"
        )


def test_when_do_handler_is_given():
    """
    The expected subscription call happens at the time "when" is called with
    an existing "do" handler function. (A "do" handler, does stuff.)
    """

    def my_handler(message):
        return

    with umock.patch("invent.channels:subscribe") as mock_sub:
        invent.when(
            subject="test_subject", to_channel="test_channel", do=my_handler
        )
        mock_sub.assert_called_once_with(
            handler=my_handler,
            to_channel="test_channel",
            when_subject="test_subject",
        )


def test_when_handler_is_decorated():
    """
    the expected subscription call happens at the time "when" decorates a given
    function.
    """

    with umock.patch("invent.channels:subscribe") as mock_sub:

        @invent.when(subject="test_subject", to_channel="test_channel")
        def my_handler(message):
            return

        assert mock_sub.call_count == 1
