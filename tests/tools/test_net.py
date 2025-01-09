import asyncio
import invent
import json
from invent.tools import net


# Simple utility function tests (from the user's perspective).


async def test_request_get_as_json():
    """
    Use of the simple `request` function with HTTP GET and JSON response.
    """
    url = "https://www.swapi.tech/api/people/1"  # Luke Skywalker ;-)
    result_key = "skywalker_info"
    got_result_from_website = asyncio.Event()  # Used to wait for the result.

    def handler(message):
        got_result_from_website.set()

    invent.subscribe(handler, to_channel="store-data", when_subject=result_key)

    net.request(url, json=True, result_key=result_key)

    await got_result_from_website.wait()
    assert (
        result_key in invent.datastore
    ), "Expected key not found in datastore."
    assert (
        invent.datastore[result_key]["result"]["properties"]["name"]
        == "Luke Skywalker"
    ), "Task result not stored in datastore."


async def test_request_post_as_text():
    """
    Use of the simple `request` function with HTTP POST and text response.
    """
    url = "https://httpbin.org/post"
    result_key = "echoed_payload"
    body = "Hello world!"
    got_result_from_website = asyncio.Event()  # Used to wait for the result.

    def handler(message):
        got_result_from_website.set()

    invent.subscribe(handler, to_channel="store-data", when_subject=result_key)

    net.request(url, method="POST", body=body, result_key=result_key)

    await got_result_from_website.wait()
    assert (
        result_key in invent.datastore
    ), "Expected key not found in datastore"
    # It's just a string.
    assert isinstance(
        invent.datastore[result_key], str
    ), "Task result not stored in datastore as text."
    # Check the text string contains the expected JSON.
    decoded = json.loads(invent.datastore[result_key])
    assert decoded["url"] == url, "Task result not stored in datastore."
    assert decoded["data"] == body, "Task result not stored in datastore."


async def test_websocket():
    """
    A simple test to connect to a websocket.
    """
    url = "wss://echo.websocket.org"
    result_key = "websocket_response"
    test_message_to_echo = "Hello, world!"
    got_message_from_websocket = asyncio.Event()

    def handler(message):
        if message.value == test_message_to_echo:
            got_message_from_websocket.set()

    invent.subscribe(handler, to_channel="store-data", when_subject=result_key)

    socket = net.websocket(url, result_key=result_key)
    socket.send(test_message_to_echo)
    await got_message_from_websocket.wait()
    assert (
        invent.datastore[result_key] == test_message_to_echo
    ), invent.datastore[result_key]


# Websocket class implementation unit tests.


async def test_connect_to_websocket():
    """
    A simple test to connect to a websocket.
    """
    url = "wss://echo.websocket.org"
    result_key = "websocket_response"
    test_message_to_echo = "Hello, world!"
    got_message_from_websocket = asyncio.Event()

    def handler(message):
        if message.value == test_message_to_echo:
            got_message_from_websocket.set()

    invent.subscribe(handler, to_channel="store-data", when_subject=result_key)

    socket = net._WebSocket(url, result_key)
    socket.send(test_message_to_echo)
    await got_message_from_websocket.wait()
    assert (
        invent.datastore[result_key] == test_message_to_echo
    ), invent.datastore[result_key]


async def test_connect_to_websocket_with_explicit_event_checks():
    """
    A simple test to connect to a websocket. All the Websocket lifecycle events
    are resolved explicitly to ensure that the websocket is connected,
    messages are sent and received as expected, and closed.
    """
    url = "wss://echo.websocket.org"
    result_key = "websocket_response"
    test_message_to_echo = "Hello, world!"
    # These events fire when different states of the lifecycle of the
    # WebSocket are reached.
    got_connecting_from_websocket = asyncio.Event()
    got_open_from_websocket = asyncio.Event()
    got_message_from_websocket = asyncio.Event()
    got_close_from_websocket = asyncio.Event()

    def handler(message):
        """
        Resolve the events when the WebSocket reaches different states.
        """
        if message.value == net.WEBSOCKET_CONNECTING:
            got_connecting_from_websocket.set()
        elif message.value == net.WEBSOCKET_OPEN:
            got_open_from_websocket.set()
        elif message.value == net.WEBSOCKET_CLOSE:
            got_close_from_websocket.set()
        elif message.value == test_message_to_echo:
            got_message_from_websocket.set()

    invent.subscribe(handler, to_channel="store-data", when_subject=result_key)

    socket = net._WebSocket(url, result_key)

    await got_connecting_from_websocket.wait()
    await got_open_from_websocket.wait()
    socket.send(test_message_to_echo)
    await got_message_from_websocket.wait()
    assert (
        invent.datastore[result_key] == test_message_to_echo
    ), invent.datastore[result_key]
    socket.close()
    await got_close_from_websocket.wait()
    assert invent.datastore[result_key] == net.WEBSOCKET_CLOSE
