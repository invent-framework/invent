import asyncio
import invent
import json
import upytest
from invent.tools import net

# Simple utility function tests (from the user's perspective).


def setup():
    for key, value in net.WEBSOCKET_CONNECTIONS.items():
        invent.publish(
            message=invent.Message("close"),
            to_channel=value.channel,
        )
    net.WEBSOCKET_CONNECTIONS.clear()


async def test_request_get_as_json():
    """
    Use of the simple `request` function with HTTP GET and JSON
    response.
    """
    url = "https://www.swapi.tech/api/people/1"  # Luke Skywalker ;-)
    result_key = "skywalker_info"
    got_result_from_website = asyncio.Event()

    def handler(message):
        got_result_from_website.set()

    invent.subscribe(
        handler,
        to_channel=invent.datastore.DATASTORE_SET_CHANNEL,
        when_subject=result_key,
    )

    net.request(url, result_key=result_key, response_format="json")

    await got_result_from_website.wait()
    assert (
        result_key in invent.datastore
    ), "Expected key not found in datastore."
    assert (
        invent.datastore[result_key]["result"]["properties"]["name"]
        == "Luke Skywalker"
    ), "Task result not stored in datastore."


async def test_request_get_as_bytes():
    """
    Use of the simple `request` function with HTTP GET and bytes
    response.
    """
    url = "https://placedog.net/200/200"  # A cute dog picture!
    result_key = "text_as_bytes"
    got_result_from_website = asyncio.Event()

    def handler(message):
        got_result_from_website.set()

    invent.subscribe(
        handler,
        to_channel=invent.datastore.DATASTORE_SET_CHANNEL,
        when_subject=result_key,
    )

    net.request(url, result_key=result_key, response_format="bytes")

    await got_result_from_website.wait()
    assert (
        result_key in invent.datastore
    ), "Expected key not found in datastore."
    assert isinstance(
        invent.datastore[result_key], bytes
    ), "Task result not stored in datastore as bytes."


async def test_request_post_as_text():
    """
    Use of the simple `request` function with HTTP POST and text
    response.
    """
    url = "https://httpbin.org/post"
    result_key = "echoed_payload"
    body = "Hello world!"
    got_result_from_website = asyncio.Event()

    def handler(message):
        got_result_from_website.set()

    invent.subscribe(
        handler,
        to_channel=invent.datastore.DATASTORE_SET_CHANNEL,
        when_subject=result_key,
    )

    net.request(url, result_key=result_key, method="POST", body=body)

    await got_result_from_website.wait()
    assert (
        result_key in invent.datastore
    ), "Expected key not found in datastore"
    assert isinstance(
        invent.datastore[result_key], str
    ), "Task result not stored in datastore as text."
    decoded = json.loads(invent.datastore[result_key])
    assert decoded["url"] == url, "Task result not stored in datastore."
    assert decoded["data"] == body, "Task result not stored in datastore."


async def test_websocket_send_and_receive():
    """
    Connect to a websocket echo server, send a message via the
    channel, and verify the echoed response arrives back on the
    channel.
    """
    url = "wss://ws.postman-echo.com/raw"
    channel = "test_ws_echo"
    test_message = "Hello, world!"
    got_message = asyncio.Event()
    received_data = {}

    def on_message(message):
        """Capture the echoed data."""
        received_data["value"] = message.data
        got_message.set()

    invent.subscribe(
        handler=on_message,
        to_channel=channel,
        when_subject="message",
    )

    net.websocket(url, channel)

    # Send before open — should be queued and sent when ready.
    invent.publish(
        message=invent.Message("send", data=test_message),
        to_channel=channel,
    )

    await got_message.wait()
    assert received_data["value"] == test_message

    invent.publish(
        message=invent.Message("close"),
        to_channel=channel,
    )


async def test_websocket_full_lifecycle():
    """
    Verify all websocket lifecycle statuses are published to the
    channel in order: connecting, open, then closed after an
    explicit close.
    """
    url = "wss://ws.postman-echo.com/raw"
    channel = "test_ws_lifecycle"
    test_message = "Hello, world!"

    got_connecting = asyncio.Event()
    got_open = asyncio.Event()
    got_message = asyncio.Event()
    got_closed = asyncio.Event()
    received_data = None

    def on_status(message):
        """
        Resolve events as the connection progresses.
        """
        if message.status == "connecting":
            got_connecting.set()
        elif message.status == "open":
            got_open.set()
        elif message.status == "closed":
            got_closed.set()

    def on_message(message):
        """
        Capture the echoed data.
        """
        nonlocal received_data
        received_data = message.data
        got_message.set()

    invent.subscribe(
        handler=on_status,
        to_channel=channel,
        when_subject="status",
    )
    invent.subscribe(
        handler=on_message,
        to_channel=channel,
        when_subject="message",
    )

    net.websocket(url, channel)

    await got_connecting.wait()
    await got_open.wait()

    invent.publish(
        message=invent.Message("send", data=test_message),
        to_channel=channel,
    )

    await got_message.wait()
    assert received_data == test_message

    invent.publish(
        message=invent.Message("close"),
        to_channel=channel,
    )

    await got_closed.wait()
    assert url not in net.WEBSOCKET_CONNECTIONS, "Connection not cleaned up."


async def test_websocket_json_serialisation():
    """
    Non-string data sent via the channel should be automatically
    JSON-encoded before being sent through the websocket.
    """
    url = "wss://ws.postman-echo.com/raw"
    channel = "test_ws_json"
    test_payload = {"greeting": "hello", "count": 42}
    got_message = asyncio.Event()
    received_data = None

    def on_message(message):
        """Capture the echoed data."""
        nonlocal received_data
        received_data = message.data
        got_message.set()

    invent.subscribe(
        handler=on_message,
        to_channel=channel,
        when_subject="message",
    )

    net.websocket(url, channel)

    invent.publish(
        message=invent.Message("send", data=test_payload),
        to_channel=channel,
    )

    await got_message.wait()
    decoded = json.loads(received_data)
    assert decoded == test_payload, (decoded, test_payload)
    invent.publish(
        message=invent.Message("close"),
        to_channel=channel,
    )


async def test_websocket_duplicate_url_raises():
    """
    Attempting to open a second websocket to the same URL should
    raise a ValueError.
    """
    url = "wss://ws.postman-echo.com/raw"
    channel_a = "test_ws_dup_a"
    channel_b = "test_ws_dup_b"

    net.websocket(url, channel_a)

    with upytest.raises(ValueError):
        net.websocket(url, channel_b)

    # Tidy up.
    invent.publish(
        message=invent.Message("close"),
        to_channel=channel_a,
    )


async def test_websocket_cleanup_after_close():
    """
    After closing, the connection should be removed from the
    registry.
    """
    url = "wss://ws.postman-echo.com/raw"
    channel = "test_ws_cleanup"
    got_open = asyncio.Event()
    got_closed = asyncio.Event()

    def on_status(message):
        """
        Track connection status.
        """
        if message.status == "open":
            got_open.set()
        elif message.status == "closed":
            got_closed.set()

    invent.subscribe(
        handler=on_status,
        to_channel=channel,
        when_subject="status",
    )

    net.websocket(url, channel)

    await got_open.wait()

    invent.publish(
        message=invent.Message("close"),
        to_channel=channel,
    )

    await got_closed.wait()

    assert (
        url not in net.WEBSOCKET_CONNECTIONS
    ), "Connection not removed from registry."
