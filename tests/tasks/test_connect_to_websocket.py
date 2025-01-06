import invent
import asyncio
from invent import tasks


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

    socket = tasks.WebSocket(result_key).go(url)
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
        if message.value == tasks.WebSocket.CONNECTING:
            got_connecting_from_websocket.set()
        elif message.value == tasks.WebSocket.OPEN:
            got_open_from_websocket.set()
        elif message.value == tasks.WebSocket.CLOSE:
            got_close_from_websocket.set()
        elif message.value == test_message_to_echo:
            got_message_from_websocket.set()

    invent.subscribe(handler, to_channel="store-data", when_subject=result_key)

    socket = tasks.WebSocket(result_key).go(url)

    await got_connecting_from_websocket.wait()
    await got_open_from_websocket.wait()
    socket.send(test_message_to_echo)
    await got_message_from_websocket.wait()
    assert (
        invent.datastore[result_key] == test_message_to_echo
    ), invent.datastore[result_key]
    socket.close()
    await got_close_from_websocket.wait()
    assert invent.datastore[result_key] == tasks.WebSocket.CLOSE
