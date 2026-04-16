"""
Defines tasks for connecting to the outside world via web requests, websocket
connections, web serial and BLE.

```
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
```
"""

import asyncio
import json
import pyscript
import invent

#: Flag for the datastore to indicate an error status.
WEB_ERROR = "_WEB_ERROR"

#: Active websocket connections, keyed by URL.
WEBSOCKET_CONNECTIONS = {}

#: Valid HTTP response formats for the `request` function.
VALID_RESULT_FORMATS = {
    "text",  # Default, parses the response as a string.
    "json",  # Parses the response from JSON into a Python object.
    "bytes",  # Parses the response as raw bytes.
}


def web_request(url, result_key, response_format="text", *args, **kwargs):
    """
    Make a web request to a URL and store the result in the datastore
    via the `result_key`.

    The `response_format` argument controls how the response is parsed
    before being stored. It can be one of "text", "json", or "bytes"
    (default is "text"). If an invalid format is provided, a ValueError
    is raised. The "json" format will attempt to parse the response as
    JSON and store the resulting Python object. The "bytes" format will
    read the response as a byte stream and store it as raw bytes.
    The "text" format will read the response as a string.

    If the response is not `OK`, a `WEB_ERROR` flag is stored in the
    datastore at the `result_key`, along with contextual information.

    This is an Invent-friendly wrapper around the standard
    `pyscript.fetch` API, which is a direct binding to the browser's
    own Fetch API (https://docs.pyscript.net/latest/api/fetch/).

    Example usage:

    ```python
    # Make a GET request and store the JSON response in the datastore.
    connect.web_request(
        url="https://api.example.com/data",
        result_key="api_data",
        response_format="json",
    )

    # Make a POST request with a text body and store the response as text.
    connect.web_request(
        url="https://api.example.com/submit",
        result_key="submit_response",
        method="POST",
        body="Hello, world!",
    )

    # Make a GET request and store the response as bytes.
    connect.web_request(
        url="https://api.example.com/file.mp3",
        result_key="music_data",
        response_format="bytes",
    )
    ```
    """

    if response_format not in VALID_RESULT_FORMATS:
        raise ValueError(
            f"Invalid response_format '{response_format}'. "
            f"Must be one of: {', '.join(VALID_RESULT_FORMATS)}."
        )

    async def wrapper():
        response = await pyscript.fetch(url, *args, **kwargs)
        if response.ok:
            if response_format == "json":
                result = await response.json()
            elif response_format == "bytes":
                # The bytearray will be stored in the datastore as a type of
                # bytes, which is supported by the custom JSON encoding /
                # decoding in the datastore.
                result = await response.bytearray()
            else:
                result = await response.text()
        else:
            result = WEB_ERROR + f": {response.status} {response.statusText}"
        invent.datastore[result_key] = result

    asyncio.create_task(wrapper())


class _InventWebSocket:
    """
    Manage a websocket connection bound to a channel.

    Opens a websocket connection to the given URL and binds it to
    the specified channel(s).

    The channel argument can be a single channel name string or a
    list of channel name strings.

    All communication with the websocket is via the channel(s):

    - Publish a message with subject "send" and a `.data` attribute
      to forward data through the websocket.
    - Publish a message with subject "close" to close the
      connection and clean up.
    - Subscribe to the channel(s) with a subject "message" to
      receive incoming data (arrives as `.data` on the message).
    - Subscribe to the channel(s) with a subject "status" to receive
      connection state changes (arrives as `.status` on the message,
      one of: "connecting", "open", "error", "closed").

    Messages published with subject "send" before the connection is
    open will be queued and sent automatically once the connection
    is ready.

    Example usage:

    ```python
    # Connect to a websocket and bind to a channel.
    net.websocket("wss://example.com/socket", "my_channel")

    # Send a message through the websocket.
    invent.publish(
        message=invent.Message("send", data="Hello, world!"),
        to_channel="my_channel",
    )

    # Subscribe to receive messages from the websocket.
    def on_message(message):
        print("Received:", message.data)

    invent.subscribe(
        handler=on_message,
        to_channel="my_channel",
        when_subject="message",
    )

    # Subscribe to connection status updates.
    def on_status(message):
        print("Status:", message.status)

    invent.subscribe(
        handler=on_status,
        to_channel="my_channel",
        when_subject="status",
    )

    # Close the connection when done.
    invent.publish(
        message=invent.Message("close"),
        to_channel="my_channel",
    )
    ```
    """

    def __init__(self, url, channel):
        """
        Initialise the connection and bind to the channel[s].
        """
        if url in WEBSOCKET_CONNECTIONS:
            raise ValueError(f"Already connected to '{url}'.")
        WEBSOCKET_CONNECTIONS[url] = self
        self.url = url
        self.channel = channel
        self._ready = asyncio.Event()
        # Connect and bind the JS websocket callbacks.
        self._connection = pyscript.WebSocket(url=url)
        self._connection.onopen = self._on_open
        self._connection.onmessage = self._on_message
        self._connection.onerror = self._on_error
        self._connection.onclose = self._on_close
        # Subscribe to the channel for send and close commands.
        invent.subscribe(
            handler=self._handle_send,
            to_channel=channel,
            when_subject="send",
        )
        invent.subscribe(
            handler=self._handle_close,
            to_channel=channel,
            when_subject="close",
        )
        # Publish the initial connecting status.
        self._publish_status("connecting")

    def _publish_status(self, status):
        """
        Publish a status message to the channel.
        """
        invent.publish(
            message=invent.Message("status", status=status),
            to_channel=self.channel,
        )

    def _send(self, data):
        """
        Serialise and send data through the websocket.
        """
        if not isinstance(data, str):
            data = json.dumps(data)
        self._connection.send(data)

    def _cleanup(self):
        """
        Remove from the registry and unsubscribe handlers.
        """
        WEBSOCKET_CONNECTIONS.pop(self.url, None)
        invent.unsubscribe(
            handler=self._handle_send,
            from_channel=self.channel,
            when_subject="send",
        )
        invent.unsubscribe(
            handler=self._handle_close,
            from_channel=self.channel,
            when_subject="close",
        )

    def _handle_send(self, message):
        """
        Forward a message through the websocket. If the connection
        is not yet open, queue the send until it is ready.
        """
        if self._ready.is_set():
            self._send(message.data)
        else:

            async def _wait_and_send():
                """
                Wait for readiness then send.
                """
                await self._ready.wait()
                self._send(message.data)

            asyncio.create_task(_wait_and_send())

    def _handle_close(self, message):
        """
        Close the websocket connection.
        """
        if self._connection:
            self._connection.close()

    def _on_open(self, event):
        """
        Signal readiness and publish the open status.
        """
        self._ready.set()
        self._publish_status("open")

    def _on_message(self, event):
        """
        Publish received data to the channel.
        """
        invent.publish(
            message=invent.Message("message", data=event.data),
            to_channel=self.channel,
        )

    def _on_error(self, event):
        """
        Publish the error status to the channel.
        """
        self._publish_status("error")

    def _on_close(self, event):
        """
        Tidy up and publish the closed status.
        """
        self._cleanup()
        self._publish_status("closed")


# Expose the class as a module-level function for ease of use.
web_socket = _InventWebSocket
