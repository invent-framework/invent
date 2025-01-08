"""
Defines a task that fetches a URL and stores the result in the datastore.

Based on original pre-COVID work by [Nicholas H.Tollervey.](https://ntoll.org/)

Copyright (c) 2024 Invent contributors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import asyncio
import pyscript
import invent
import json
from ..task import Task


def request(url, json=False, result_key=None, *args, **kwargs):
    """
    Make a request to a URL and store the result in the datastore. If the json
    flag is set to False, returns a plain response string. If the response is
    not OK, raises a ConnectionError.
    """
    _WebRequest(result_key).go(url, json, *args, **kwargs)


def websocket(url, result_key=None):
    """
    Connect to a web socket and return an object representing the connection.
    Store any messages received in the datastore if a key is provided. Use the
    connection's send() method to send messages via the websocket.
    Close the connection with its close() method.

    The socket connection status is stored in the datastore at the given key,
    and any messages received are stored in the datastore at the same key. The
    status flags defined as: WebSocket.CONNECTING, WebSocket.OPEN,
    WebSocket.ERROR, and WebSocket.CLOSE.
    """
    return _WebSocket(result_key).go(url)


async def _fetch(_self, url, json=False, *args, **kwargs):
    """
    Fetch a URL and return the JSON result. If the json flag is set to False,
    returns a plain response string. If the response is not OK, raises a
    ConnectionError.
    """
    response = await pyscript.fetch(url, *args, **kwargs)
    if response.ok:
        if json:
            result = await response.json()
        else:
            result = await response.text()
        return result
    else:
        raise ConnectionError(f"Failed to fetch {url}: {response.status}")


class _WebRequest(Task):
    """
    Make a request to a URL and store the result in the datastore if a key is
    provided. Other arguments are passed to the fetch function provided by
    PyScript and documented at:

    https://docs.pyscript.net/2024.11.1/api/#pyscriptfetch
    """

    function = _fetch


class _WebSocket(Task):
    """
    Connect to a web socket and store the messages received in the datastore if
    a key is provided. Use the send() method to send messages via the websocket.
    Close the connection with the close() method.

    The socket connection status is stored in the datastore at the given key,
    and any messages received are stored in the datastore at the same key. The
    status flags defined as: WebSocket.CONNECTING, WebSocket.OPEN,
    WebSocket.ERROR, and WebSocket.CLOSE.
    """

    #: The flag to indicate the websocket is connecting.
    CONNECTING = "_WEBSOCKET_CONNECTING"
    #: The flag to indicate the websocket is open (connected).
    OPEN = "_WEBSOCKET_OPEN"
    #: The flag to indicate the websocket has an error.
    ERROR = "_WEBSOCKET_ERROR"
    #: The flag to indicate the websocket has closed.
    CLOSE = "_WEBSOCKET_CLOSE"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # The eventual websocket connection.
        self._connection = None
        # Flag to indicate the websocket is open.
        self._is_open = asyncio.Event()

    def go(self, url):
        """
        Connect to the websocket.
        """
        self._connection = pyscript.WebSocket(url=url)
        self._connection.onopen = self._on_open
        self._connection.onmessage = self._on_message
        self._connection.onerror = self._on_error
        self._connection.onclose = self._on_close
        self._set_value_at_result_key(self.CONNECTING)
        return self

    def _set_value_at_result_key(self, value):
        """
        Set the value at the result key in the datastore.
        """
        if self.result_key:
            invent.datastore[self.result_key] = value

    def send(self, message):
        """
        Send a message via the websocket. If the message is not already a string
        the message object will be automatically JSON encoded.

        If the websocket is not yet open, the message will be sent when the
        websocket is ready.
        """
        if self._is_open.is_set():
            self._send(message)
        else:

            async def wait_for_ready():
                await self._is_open.wait()
                self._send(message)

            asyncio.create_task(wait_for_ready())

    def _send(self, message):
        """
        Send a message via the websocket. If the message is not already a string
        the message object will be automatically JSON encoded.
        """
        if not isinstance(message, str):
            message = json.dumps(message)
        self._connection.send(message)

    def close(self):
        """
        Close the websocket connection.
        """
        if self._connection:
            self._connection.close()

    def _on_message(self, message):
        """
        Store the message in the datastore.
        """
        self._set_value_at_result_key(message.data)

    def _on_error(self, error):
        """
        Store the error in the datastore.
        """
        self._set_value_at_result_key(self.ERROR + ": " + str(error))

    def _on_close(self, event):
        """
        Store the close flag in the datastore.
        """
        self._set_value_at_result_key(self.CLOSE)

    def _on_open(self, event):
        """
        Store the open flag in the datastore and resove the ready event.
        """
        self._is_open.set()
        self._set_value_at_result_key(self.OPEN)
