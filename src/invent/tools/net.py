"""
Defines a task that fetches a URL and stores the result in the datastore.

Based on original pre-COVID work by [Nicholas H.Tollervey.](https://ntoll.org/)

Copyright (c) 2019-present Invent contributors.

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


#: Flag for the datastore to indicate an error status.
WEB_ERROR = "_WEB_ERROR"
#: The flag to indicate the websocket is connecting.
WEBSOCKET_CONNECTING = "_WEBSOCKET_CONNECTING"
#: The flag to indicate the websocket is open (connected).
WEBSOCKET_OPEN = "_WEBSOCKET_OPEN"
#: The flag to indicate the websocket has an error.
WEBSOCKET_ERROR = "_WEBSOCKET_ERROR"
#: The flag to indicate the websocket has closed.
WEBSOCKET_CLOSE = "_WEBSOCKET_CLOSE"


def request(url, json=False, result_key=None, *args, **kwargs):
    """
    Make a request to a URL and store the result in the datastore. If the json
    flag is set to False, returns a plain response string. If the response is
    not OK, a WEB_ERROR flag is stored in the datastore, along with contextual
    information.
    """

    async def wrapper():
        response = await pyscript.fetch(url, *args, **kwargs)
        if response.ok:
            if json:
                result = await response.json()
            else:
                result = await response.text()
            if result_key:
                invent.datastore[result_key] = result
        else:
            invent.datastore[result_key] = (
                WEB_ERROR + f": {response.status} {response.message}"
            )

    asyncio.create_task(wrapper())


class _WebSocket:
    """
    Connect to a web socket at the specified URL and store the messages
    received in the datastore via the result_key. Use the send() method on the
    instance to send messages with the websocket. Close the connection with the
    close() method.

    The socket connection status is stored in the datastore at the given
    result_key, and any messages received are stored in the datastore at the
    same key. The status flags defined as: WEBSOCKET_CONNECTING, WEBSOCKET_OPEN,
    WEBSOCKET_ERROR, and WEBSOCKET_CLOSE.
    """

    def __init__(self, url, result_key):
        # Where to store status and incoming messages in the datastore.
        self.result_key = result_key
        # The eventual websocket connection.
        self._connection = None
        # Flag to indicate the websocket is open.
        self._is_open = asyncio.Event()
        # Now go connect via the given URL.
        self._connection = pyscript.WebSocket(url=url)
        self._connection.onopen = self._on_open
        self._connection.onmessage = self._on_message
        self._connection.onerror = self._on_error
        self._connection.onclose = self._on_close
        self._set_value_at_result_key(WEBSOCKET_CONNECTING)

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
        self._set_value_at_result_key(WEBSOCKET_ERROR + f": {error.type}")

    def _on_close(self, event):
        """
        Store the close flag in the datastore.
        """
        self._set_value_at_result_key(WEBSOCKET_CLOSE)

    def _on_open(self, event):
        """
        Store the open flag in the datastore and resove the ready event.
        """
        self._is_open.set()
        self._set_value_at_result_key(WEBSOCKET_OPEN)


websocket = _WebSocket
