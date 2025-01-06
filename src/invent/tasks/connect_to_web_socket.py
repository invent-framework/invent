"""
Defines a task that connects to a web socket and stores messages received in the
datastore.

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


class WebSocket(Task):
    """
    Connect to a web socket and store the messages received in the datastore if
    a key is provided. Use the send() method to send messages via the websocket.
    Close the connection with the close() method.

    The soclet connection status is stored in the datastore at the given key,
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
        # Awaitable to indicate the websocket is open.
        self.ready = asyncio.Event()

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
        if self.ready.is_set():
            self._send(message)
        else:

            async def wait_for_ready():
                await self.ready.wait()
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
        self.ready.set()
        self._set_value_at_result_key(self.OPEN)
