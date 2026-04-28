"""
Connect an Invent app to the outside world.

This module gives four ways out of the browser: one-shot web requests,
long-lived websocket connections, a serial port on a physically
attached device, and a characteristic on a Bluetooth Low Energy
device. The first is a direct call-and-store operation; the other
three are Invent channels, so the rest of the app interacts with them
by publishing and subscribing in the usual way.

Public names:

- `web_request` - fetch a URL and store the response in the datastore
  under a chosen key. Supports text, JSON, and raw bytes.
- `web_socket` - open a websocket and bind it to a channel. Messages
  published on the channel are sent through the socket; messages
  arriving from the socket are published back on the channel.
- `serial_connection` - open a serial port (prompting the user once
  via the browser's port picker) and bind it to a channel. Line-mode
  and raw-bytes mode are both supported.
- `ble_connection` - bind a channel to a single characteristic on a
  Bluetooth Low Energy device. One channel per characteristic;
  multiple channels may share the same underlying device.
- `serial_ports` and `ble_ports` - functions that list the serial
  ports and BLE devices the user has already authorised, into the
  datastore.

Developers reach for the specific function or class for the rest.
Error flags stored in the datastore on failure are `WEB_ERROR`,
`SERIAL_ERROR`, and `BLE_ERROR`.

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
from pyscript.ffi import to_js
import invent

#: Flag for the datastore to indicate a web request error.
WEB_ERROR = "_WEB_ERROR"

#: Flag for the datastore to indicate a serial connection error.
SERIAL_ERROR = "_SERIAL_ERROR"

#: Flag for the datastore to indicate a BLE error.
BLE_ERROR = "_BLE_ERROR"

#: Active websocket connections, keyed by URL.
WEBSOCKET_CONNECTIONS = {}

#: Active serial connections, keyed by individual channel name.
SERIAL_CONNECTIONS = {}

#: Active BLE channel bindings, keyed by channel name.
BLE_CONNECTIONS = {}

#: Shared BLE device connections, keyed by BluetoothDevice.id.
BLE_DEVICES = {}

#: Valid HTTP response formats for the `request` function.
VALID_RESULT_FORMATS = {
    "text",  # Default, parses the response as a string.
    "json",  # Parses the response from JSON into a Python object.
    "bytes",  # Parses the response as raw bytes.
}

#: Valid serial connection modes.
VALID_SERIAL_MODES = {
    "line",  # Default, decoded text split on the newline delimiter.
    "raw",  # Raw bytes in and out.
}


def web_request(url, result_key, response_format="text", *args, **kwargs):
    """
    Fetch a URL and store the response in the datastore at
    `result_key`.

    The `response_format` argument controls how the response body is
    parsed before being stored: `"text"` (the default) stores a string,
    `"json"` parses the body as JSON and stores the resulting Python
    object, and `"bytes"` stores the raw byte stream. Any other value
    raises `ValueError`.

    The request runs asynchronously; this function returns immediately
    and the datastore is updated when the response arrives. If the
    response status is not OK, the `WEB_ERROR` flag is stored at
    `result_key` along with the HTTP status and message, so a
    subscriber can distinguish success from failure by inspecting the
    stored value. Extra positional and keyword arguments are forwarded
    to the underlying fetch call (e.g. `method="POST"`, `body=...`,
    headers, and so on). See the
    [PyScript fetch API](https://docs.pyscript.net/latest/api/fetch/)
    for the full list.

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
                # NOTE: The bytearray will be stored in the datastore as
                # a type of bytes, which is supported by the custom JSON
                # encoding / decoding in the datastore.
                result = await response.bytearray()
            else:
                result = await response.text()
        else:
            result = WEB_ERROR + f": {response.status} {response.message}"
        invent.datastore[result_key] = result

    asyncio.create_task(wrapper())


def serial_ports(result_key):
    """
    List the serial ports the user has already authorised, storing the
    result as a list of dicts in the datastore at `result_key`.

    Each entry mirrors the browser's `SerialPort.getInfo()` result and
    typically contains `usbVendorId` and `usbProductId` keys (plus
    `bluetoothServiceClassId` for Bluetooth RFCOMM ports). Keys are
    JS-style camelCase to match the underlying browser API.

    Authorisation is per-origin and persists across visits, so an
    already-authorised port will reappear here without the user being
    prompted again. To prompt the user for a new port, use
    `serial_connection` instead. On failure, the `SERIAL_ERROR` flag
    is stored at `result_key` along with a description of the error.

    Example usage:

    ```python
    # Discover already-authorised serial ports.
    connect.serial_ports(result_key="my_ports")
    # Later, invent.datastore["my_ports"] might be:
    # [{"usbVendorId": 0x2341, "usbProductId": 0x0043}]
    ```
    """

    async def wrapper():
        try:
            ports = await pyscript.window.navigator.serial.getPorts()
            result = [_port_info(port) for port in ports]
        except Exception as ex:
            result = SERIAL_ERROR + f": {ex}"
        invent.datastore[result_key] = result

    asyncio.create_task(wrapper())


def _port_info(port):
    """
    Convert a `SerialPort.getInfo()` result into a Python dict using
    JS-style key names. Keys whose values are undefined are omitted.
    """
    info = port.getInfo()
    result = {}
    for key in ("usbVendorId", "usbProductId", "bluetoothServiceClassId"):
        value = getattr(info, key, None)
        if value is not None:
            result[key] = value
    return result


def ble_ports(result_key):
    """
    List the BLE devices the user has already authorised, storing the
    result as a list of dicts in the datastore at `result_key`.

    Each entry contains `id` and `name` keys, mirroring the relevant
    fields of the browser's `BluetoothDevice` object. Keys are
    JS-style camelCase to match the underlying browser API.

    Authorisation is per-origin and persists across visits, so an
    already-authorised device will reappear here without the user
    being prompted again. To prompt the user for a new device, use
    `ble_connection` instead. On failure, the `BLE_ERROR` flag is
    stored at `result_key` along with a description of the error.

    Example usage:

    ```python
    # Discover already-authorised BLE devices.
    connect.ble_ports(result_key="my_devices")
    # Later, invent.datastore["my_devices"] might be:
    # [{"id": "abc123...", "name": "micro:bit"}]
    ```
    """

    async def wrapper():
        try:
            devices = await pyscript.window.navigator.bluetooth.getDevices()
            result = [_device_info(device) for device in devices]
        except Exception as ex:
            result = BLE_ERROR + f": {ex}"
        invent.datastore[result_key] = result

    asyncio.create_task(wrapper())


def _device_info(device):
    """
    Convert a JavaScript `BluetoothDevice` into a plain Python dict
    with its `id` and (when present) `name`.
    """
    result = {"id": device.id}
    name = getattr(device, "name", None)
    if name is not None:
        result["name"] = name
    return result


class _InventWebSocket:
    """
    A websocket connection expressed as an Invent channel.

    An instance of this class holds open one websocket to a given URL
    and routes all traffic between the socket and a named channel. The
    developer does not call methods on the instance directly; they
    publish to and subscribe to the channel in the usual Invent way.

    The class handles the ordinary messiness of a websocket (the
    connection has to open before it can be written to; either end may
    close it; errors may arrive asynchronously) so the developer sees
    a channel whose behaviour is predictable from one message to the
    next. Messages published with subject `"send"` before the socket
    is open are queued and dispatched as soon as the connection is
    ready.

    Messages that flow through the channel:

    - Publish with subject `"send"` and a `.data` attribute to forward
      data through the socket.
    - Publish with subject `"close"` to close the socket and clean up.
    - Subscribe with subject `"message"` to receive incoming data; it
      arrives as `.data` on the message.
    - Subscribe with subject `"status"` to receive connection state
      changes; the new state arrives as `.status`, one of
      `"connecting"`, `"open"`, `"error"`, or `"closed"`.

    Example usage:

    ```python
    # Connect to a websocket and bind to a channel.
    connect.web_socket("wss://example.com/socket", "my_channel")

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
        Open a websocket to `url` and bind it to `channel`. The socket
        opens asynchronously; subscribe to the channel with subject
        `"status"` to track its state. Raises `ValueError` if a
        websocket for this URL is already open in the current session.
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


class _InventSerial:
    """
    A connection to a serial port, expressed as an Invent channel.

    An instance of this class holds open one serial port and routes
    all traffic between the port and one or more named channels. The
    developer does not call methods on the instance directly; they
    publish to and subscribe to the channel(s) in the usual Invent
    way. Binding to more than one channel is occasionally useful when
    separate parts of an app want to observe the same port through
    their own names; a single channel is the common case.

    On first use in a session the browser prompts the user to pick a
    port via its port-picker dialog. This prompt requires a user
    gesture (typically a click) to open. On later uses, if the user
    has previously authorised a matching port, the browser reconnects
    silently without showing the picker again.

    Messages that flow through the channel(s):

    - Publish with subject `"send"` and a `.data` attribute to forward
      data through the port.
    - Publish with subject `"close"` to close the port and clean up.
    - Subscribe with subject `"message"` to receive incoming data; it
      arrives as `.data` on the message.
    - Subscribe with subject `"status"` to receive connection state
      changes; the new state arrives as `.status`, one of
      `"connecting"`, `"open"`, `"error"`, `"closed"`, or
      `"reconnecting"`. An `"error"` status may carry a `.reason`
      attribute describing the cause.

    Messages published with subject `"send"` before the port is open
    are queued and dispatched as soon as the connection is ready.

    Two modes are available, chosen at construction time:

    - `"line"` (the default): incoming bytes are buffered, decoded
      with the configured encoding, and published as text once the
      newline delimiter is seen. The delimiter is retained on each
      emitted line. Outgoing strings are encoded with the configured
      encoding, and the delimiter is appended if not already present.
    - `"raw"`: incoming data is published as raw bytes and outgoing
      data is sent as-is. Strings are still encoded to bytes using
      the configured encoding.

    If `auto_reconnect` is left on (the default), the class will try
    to re-open the port on an unexpected loss, up to
    `reconnect_attempts` times, waiting `reconnect_delay` seconds
    between attempts. A deliberate close (via the `"close"` message)
    does not trigger reconnection.

    Example usage:

    ```python
    # Open a serial connection to an Arduino Uno and bind to a channel.
    connect.serial_connection(
        channels="my_device",
        filters=[{"usbVendorId": 0x2341, "usbProductId": 0x0043}],
    )

    # Send a line of text.
    invent.publish(
        message=invent.Message("send", data="Hello, device!"),
        to_channel="my_device",
    )

    # Receive data line by line.
    def on_message(message):
        print("Received:", message.data)

    invent.subscribe(
        handler=on_message,
        to_channel="my_device",
        when_subject="message",
    )

    # Subscribe to connection status updates.
    def on_status(message):
        print("Status:", message.status)

    invent.subscribe(
        handler=on_status,
        to_channel="my_device",
        when_subject="status",
    )

    # Close the connection when done.
    invent.publish(
        message=invent.Message("close"),
        to_channel="my_device",
    )
    ```
    """

    def __init__(
        self,
        channels,
        baud_rate=115200,
        encoding="utf-8",
        newline="\n",
        auto_reconnect=True,
        reconnect_delay=2,
        reconnect_attempts=3,
        mode="line",
        filters=None,
        data_bits=8,
        stop_bits=1,
        parity="none",
        buffer_size=255,
        flow_control="none",
    ):
        """
        Configure the connection and start opening it asynchronously.

        `channels` is the channel name (or list of channel names) the
        port is bound to; every `"send"`, `"close"`, `"message"`, and
        `"status"` message flows through it. A single string is
        accepted as a convenience when there is only one channel;
        list normalisation is handled downstream by `invent.subscribe`.
        `baud_rate` is the line speed in bits per second and must
        match whatever the attached device expects; `115200` is a
        common default. `encoding` is applied when converting between
        strings and bytes in either direction, and `newline` is the
        line delimiter used in `"line"` mode.

        `auto_reconnect`, `reconnect_delay`, and `reconnect_attempts`
        together control what happens if the port drops unexpectedly:
        whether to try again, how long to wait between tries, and how
        many tries to make before giving up. `mode` selects between
        `"line"` (text, delimited) and `"raw"` (bytes); an unknown
        value raises `ValueError`.

        `filters` narrows which ports are considered for silent
        reconnection and what the picker will show the user on first
        use. It uses the JS-style camelCase format from the Web Serial
        API, e.g. `[{"usbVendorId": 0x2341, "usbProductId": 0x0043}]`.
        With no filters, any already-authorised port is accepted and
        the picker (if needed) shows every serial device in reach.

        `data_bits`, `stop_bits`, `parity`, `buffer_size`, and
        `flow_control` are forwarded to the browser's `port.open()`
        call unchanged; the defaults suit most devices. See the
        [Web Serial API](https://developer.mozilla.org/en-US/docs/Web/API/SerialPort/open)
        for the permitted values.

        The connection itself opens asynchronously: subscribe to the
        channel with subject `"status"` to track its state. Raises
        `ValueError` if any requested channel is already bound to a
        serial connection.
        """
        if mode not in VALID_SERIAL_MODES:
            raise ValueError(
                f"Invalid mode '{mode}'. Must be one of: "
                f"{', '.join(sorted(VALID_SERIAL_MODES))}."
            )
        # Normalise to a list of channel names for registry checks.
        self._channels = channels if isinstance(channels, list) else [channels]
        for ch in self._channels:
            if ch in SERIAL_CONNECTIONS:
                raise ValueError(
                    f"Channel '{ch}' is already bound to a "
                    f"serial connection."
                )
        for ch in self._channels:
            SERIAL_CONNECTIONS[ch] = self
        self._encoding = encoding
        self._newline_bytes = newline.encode(encoding)
        self._auto_reconnect = auto_reconnect
        self._reconnect_delay = reconnect_delay
        self._reconnect_attempts_max = reconnect_attempts
        self._mode = mode
        self._filters = filters or []
        # Open options forwarded to port.open() in JS-style names.
        self._open_options = {
            "baudRate": baud_rate,
            "dataBits": data_bits,
            "stopBits": stop_bits,
            "parity": parity,
            "bufferSize": buffer_size,
            "flowControl": flow_control,
        }
        self._port = None
        self._reader = None
        self._writer = None
        self._read_buffer = bytearray()
        self._ready = asyncio.Event()
        self._closing = False
        self._reconnect_count = 0
        # Subscribe to the channel(s) for send and close commands.
        invent.subscribe(
            handler=self._handle_send,
            to_channel=self._channels,
            when_subject="send",
        )
        invent.subscribe(
            handler=self._handle_close,
            to_channel=self._channels,
            when_subject="close",
        )
        # Publish the initial connecting status, then start.
        self._publish_status("connecting")
        asyncio.create_task(self._connect())

    def _publish_status(self, status, reason=None):
        """
        Publish a status message to the channel(s).
        """
        invent.publish(
            message=invent.Message("status", status=status, reason=reason),
            to_channel=self._channels,
        )

    def _publish_message(self, data):
        """
        Publish received data to the channel(s).
        """
        invent.publish(
            message=invent.Message("message", data=data),
            to_channel=self._channels,
        )

    def _cleanup(self):
        """
        Remove from the registry and unsubscribe handlers.
        """
        for ch in self._channels:
            SERIAL_CONNECTIONS.pop(ch, None)
        invent.unsubscribe(
            handler=self._handle_send,
            from_channel=self._channels,
            when_subject="send",
        )
        invent.unsubscribe(
            handler=self._handle_close,
            from_channel=self._channels,
            when_subject="close",
        )

    async def _connect(self):
        """
        Select a port (matching authorised first, picker fallback),
        open it, and start the read loop. On unexpected failure,
        attempt to reconnect if configured.
        """
        try:
            self._port = await self._select_port()
            if self._port is None:
                # User cancelled the picker or no port available.
                self._publish_status(
                    "error", reason="No port available or picker cancelled."
                )
                self._cleanup()
                return
            await self._open_port()
            self._publish_status("open")
            await self._read_loop()
        except Exception as e:
            self._publish_status(
                "error", reason=f"Unexpected error during connection. {e}"
            )
        if not self._closing:
            await self._maybe_reconnect()

    async def _select_port(self):
        """
        Return the first already-authorised port matching the
        filters; otherwise prompt the user via the browser picker.
        Returns `None` if the picker is cancelled.
        """
        ports = await pyscript.window.navigator.serial.getPorts()
        for port in ports:
            if self._port_matches(port):
                return port
        # No existing match: open the picker. Requires a user gesture.
        request_options = {}
        if self._filters:
            request_options["filters"] = self._filters
        try:
            return await pyscript.window.navigator.serial.requestPort(
                to_js(request_options)
            )
        except Exception:
            return None

    def _port_matches(self, port):
        """
        True if the port's `getInfo()` matches any of the filters; with
        no `self._filters`, every port matches.
        """
        if not self._filters:
            return True
        info = port.getInfo()
        for filter_dict in self._filters:
            if all(
                getattr(info, key, None) == value
                for key, value in filter_dict.items()
            ):
                return True
        return False

    async def _open_port(self):
        """
        Open the port with the configured options and acquire a
        writer. Marks the connection as ready and resets the
        reconnection budget.
        """
        await self._port.open(to_js(self._open_options))
        self._writer = self._port.writable.getWriter()
        self._ready.set()
        self._reconnect_count = 0

    async def _read_loop(self):
        """
        Read continuously from the port and dispatch incoming data.
        Exits cleanly on close or when the port becomes unreadable.
        """
        while self._port and self._port.readable and not self._closing:
            self._reader = self._port.readable.getReader()
            try:
                while True:
                    result = await self._reader.read()
                    if result.done:
                        break
                    self._handle_incoming(bytes(result.value))
            except Exception:
                # Stream error: exit and let reconnect logic handle.
                break
            finally:
                try:
                    self._reader.releaseLock()
                except Exception:
                    pass
                self._reader = None

    def _handle_incoming(self, chunk):
        """
        Dispatch a chunk of incoming bytes according to the mode.
        """
        if self._mode == "raw":
            self._publish_message(chunk)
            return
        # Line mode: buffer and split on the newline delimiter,
        # retaining the delimiter on each emitted line. Uses find()
        # and slicing rather than partition() because MicroPython's
        # bytearray does not support partition().
        self._read_buffer.extend(chunk)
        delimiter = self._newline_bytes
        dlen = len(delimiter)
        pos = self._read_buffer.find(delimiter)
        while pos != -1:
            line = bytes(self._read_buffer[: pos + dlen])
            self._read_buffer = bytearray(self._read_buffer[pos + dlen :])
            text = line.decode(self._encoding)
            self._publish_message(text)
            pos = self._read_buffer.find(delimiter)

    def _handle_send(self, message):
        """
        Forward a message through the serial port. If the connection
        is not yet open, queue the send until it is ready.
        """
        if self._ready.is_set():
            asyncio.create_task(self._send(message.data))
        else:

            async def _wait_and_send():
                """
                Wait for readiness then send.
                """
                await self._ready.wait()
                await self._send(message.data)

            asyncio.create_task(_wait_and_send())

    async def _send(self, data):
        """
        Encode data as bytes (via the configured encoding for str
        input) and write to the serial port. In line mode the
        newline delimiter is appended if not already present.
        """
        if isinstance(data, str):
            payload = data.encode(self._encoding)
        else:
            payload = bytes(data)
        if self._mode == "line" and not payload.endswith(self._newline_bytes):
            payload = payload + self._newline_bytes
        buffer = pyscript.window.Uint8Array.new(len(payload))
        for index, byte_value in enumerate(payload):
            buffer[index] = byte_value
        try:
            await self._writer.write(buffer)
        except Exception as e:
            # Write failed (e.g. device unplugged). The read loop
            # will detect the disconnect and trigger reconnection.
            self._publish_status("error", reason=f"Write failed. {e}")

    def _handle_close(self, message):
        """
        Begin tearing down the serial connection.
        """
        if self._closing:
            return
        self._closing = True
        asyncio.create_task(self._close_port())

    async def _close_port(self):
        """
        Cancel the reader, close the writer, close the port, and
        publish the closed status. Each step is independently
        guarded so a partial failure still completes teardown.
        """
        try:
            if self._reader:
                await self._reader.cancel()
        except Exception:
            pass
        try:
            if self._writer:
                await self._writer.close()
        except Exception:
            pass
        try:
            if self._port:
                await self._port.close()
        except Exception:
            pass
        self._cleanup()
        self._publish_status("closed")

    async def _maybe_reconnect(self):
        """
        Attempt to reconnect after an unexpected loss, up to the
        configured number of attempts. Gives up and publishes
        "closed" if all attempts fail or auto-reconnect is disabled.
        """
        if self._closing:
            return
        if (
            not self._auto_reconnect
            or self._reconnect_count >= self._reconnect_attempts_max
        ):
            self._cleanup()
            self._publish_status("closed")
            return
        self._reconnect_count += 1
        self._publish_status("reconnecting")
        # Reset readiness so further sends queue until re-open.
        self._ready.clear()
        try:
            if self._writer:
                self._writer.releaseLock()
        except Exception:
            pass
        self._writer = None
        await asyncio.sleep(self._reconnect_delay)
        if self._closing:
            return
        try:
            await self._open_port()
            self._publish_status("open")
            await self._read_loop()
        except Exception:
            pass
        if not self._closing:
            await self._maybe_reconnect()


class _InventBLEDevice:
    """
    A shared GATT (Generic ATTribute Profile) server connection to a
    single physical BLE device. Multiple channels may be bound to
    characteristics on the same device; this class is the single
    point at which the GATT connection is opened, observed, and torn
    down.

    Lifecycle is reference-counted against the channel instances
    using it: when the last channel detaches, the GATT server is
    disconnected and the device entry is removed from `BLE_DEVICES`.
    The class also listens for unexpected disconnects at the device
    level and notifies every bound channel so they can update their
    state accordingly.

    This is hidden plumbing; developers interact only with
    `_InventBLE` via channels.
    """

    def __init__(self, device):
        """
        Wrap a BluetoothDevice and prepare for GATT connection.
        """
        self.device = device
        self.server = None
        self._channels = set()
        # Listen for and cleanly handle unexpected disconnects at the
        # device level.
        self.device.addEventListener(
            "gattserverdisconnected", self._on_disconnected
        )

    async def connect_server(self):
        """
        Connect to the GATT server if not already connected. Safe to
        call repeatedly; returns the connected server either way.
        """
        if self.server is None or not self.server.connected:
            self.server = await self.device.gatt.connect()
        return self.server

    def attach(self, channel_instance):
        """
        Register a channel instance as using this device.
        """
        self._channels.add(channel_instance)

    def detach(self, channel_instance):
        """
        Remove a channel instance from the set of channels in use.
        If no channels remain, disconnect the GATT server and remove
        the device from the registry.
        """
        self._channels.discard(channel_instance)
        if not self._channels:
            self._teardown()

    def _teardown(self):
        """
        Disconnect the GATT server and remove from the registry.
        Guarded so a partial failure still completes cleanup.
        """
        try:
            if self.server and self.server.connected:
                self.device.gatt.disconnect()
        except Exception:
            pass
        BLE_DEVICES.pop(self.device.id, None)

    def _on_disconnected(self, event):
        """
        Handle an unexpected GATT disconnect. Notify every bound
        channel that it has closed and remove the device entry. The
        developer may reconnect by calling `ble_connection` again.
        """
        for channel_instance in self._channels:
            channel_instance._on_device_disconnected()
        self._channels.clear()
        BLE_DEVICES.pop(self.device.id, None)


class _InventBLE:
    """
    Bind a channel to a single BLE characteristic on a device. One
    `_InventBLE` instance manages one characteristic; multiple
    instances may share an underlying `_InventBLEDevice` when their
    characteristics live on the same physical device.

    BLE terminology, briefly:

    - A *device* is a single physical BLE peripheral (for example a
      micro:bit). Devices have an ID and usually a name.
    - A *service* is a named group of related functionality on a
      device, identified by a UUID. A device typically offers
      several (a micro:bit has separate services for its
      temperature sensor, buttons, accelerometer, LED display,
      and so on). A service groups the things you can read from,
      write to, or be notified by.
    - A *characteristic* is a single named data point within a
      service, identified by a UUID. This is where the bytes live:
      the value you read, write, or receive updates from.
    - *Capabilities* (or *properties*) are the operations a
      characteristic allows: *read* (pull its current value),
      *write* (push a new value), and *notify* (the device pushes
      updates without being asked). A characteristic may support
      any combination of the three.

    **An Invent channel binds to exactly one characteristic.** The
    `service` and `characteristic` UUIDs given to `ble_connection`
    locate it; everything else is done via the channel.

    How a channel finds its device: the UUIDs address a location
    *inside* a device, not the device itself. On first use in a
    session, the browser opens a device-picker dialog and the user
    chooses which device to connect to. This requires a user
    gesture (typically a click) to open. On subsequent uses, if the
    user has previously authorised a matching device, the browser
    reconnects to it silently without opening the picker. The
    optional `filters` argument narrows the picker so the user
    only sees relevant devices, and enables the silent-reconnect
    match on later visits.

    Messages that flow through the channel:

    - Publish with subject `"send"` and a `.data` attribute to write
      bytes to the characteristic (requires the characteristic to
      support write).
    - Publish with subject `"read"` and a `.result_key` attribute to
      trigger a one-shot read; the value is stored in the datastore
      at `result_key`. The first `"read"` message on a channel must
      include `result_key`; subsequent reads may omit it to reuse the
      last key, or supply a new key to rebind.
    - Publish with subject `"close"` to close this channel. Other
      channels on the same device remain open; the GATT connection is
      only torn down when the last channel closes.
    - Subscribe with subject `"message"` to receive notifications from
      the characteristic; data arrives as `.data` on the message, as
      raw bytes.
    - Subscribe with subject `"status"` to receive connection state
      changes; the new state arrives as `.status`, one of
      `"connecting"`, `"open"`, `"error"`, or `"closed"`. An
      `"error"` status carries a `.reason` attribute describing the
      cause.

    Characteristic capability is auto-detected at connect time: if the
    characteristic supports notify, notifications are started and
    incoming values publish as `"message"`. Attempting `"send"` on a
    characteristic that does not support write, or `"read"` on one
    that does not support read, publishes an `"error"` status.

    BLE is packet-based: values are always raw bytes. Strings passed
    to `"send"` are encoded using the configured `encoding`.

    **Web Bluetooth works only in Chromium-based browsers** (Chrome,
    Edge, Opera, Samsung Internet, and so on). Firefox and Safari do
    not support it.

    Example usage:

    ```python
    # Bind a channel to a characteristic on any device the user
    # picks. The browser will open its device-picker dialog on
    # first use and show every nearby BLE device.
    connect.ble_connection(
        channel="temperature",
        service="e95d6100-251d-470a-a062-fa1922dfa9a8",
        characteristic="e95d9250-251d-470a-a062-fa1922dfa9a8",
    )

    # The same binding, but restricted to micro:bit devices only.
    # The picker will only show devices whose name starts with
    # "BBC micro:bit". `namePrefix` is usually the friendliest
    # filter: a specific `name` filter would require matching the
    # exact five-letter suffix on each micro:bit (e.g. "BBC
    # micro:bit [zuvat]"), whereas `namePrefix` catches any
    # micro:bit the user has to hand.
    connect.ble_connection(
        channel="temperature",
        service="e95d6100-251d-470a-a062-fa1922dfa9a8",
        characteristic="e95d9250-251d-470a-a062-fa1922dfa9a8",
        filters=[{"namePrefix": "BBC micro:bit"}],
    )

    # Receive notifications (if the characteristic supports notify).
    def on_message(message):
        print("Temperature bytes:", message.data)

    invent.subscribe(
        handler=on_message,
        to_channel="temperature",
        when_subject="message",
    )

    # Request a one-shot read into the datastore.
    invent.publish(
        message=invent.Message("read", result_key="temperature_now"),
        to_channel="temperature",
    )

    # Close the channel when done.
    invent.publish(
        message=invent.Message("close"),
        to_channel="temperature",
    )
    ```

    For further background on Web Bluetooth, see
    [Chrome's Web Bluetooth guide](https://developer.chrome.com/docs/capabilities/bluetooth)
    or the
    [MDN Web Bluetooth reference](https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API).
    """

    def __init__(
        self,
        channel,
        service,
        characteristic,
        filters=None,
        optional_services=None,
        encoding="utf-8",
    ):
        """
        Configure the channel binding and start connecting
        asynchronously.

        `channel` is the name the characteristic is bound to; every
        `"send"`, `"read"`, `"close"`, `"message"`, and `"status"`
        message flows through it. `service` and `characteristic` are
        the UUIDs that locate the specific piece of data within the
        chosen device; both are required. `filters` narrows the
        browser's picker (for example to devices whose name starts
        with `"BBC micro:bit"`) and enables silent reconnection on
        later visits when a matching device has been authorised
        before.

        `optional_services` lists additional service UUIDs the app
        may need permission to read on the chosen device, beyond the
        one named in `service`. It is rarely needed; the `service`
        argument is always permitted automatically. `encoding` is
        applied when a string is passed to `"send"` so that it can
        be turned into bytes for the characteristic.

        The connection itself opens asynchronously; subscribe to the
        channel with subject `"status"` to track its state. Raises
        `ValueError` if the channel is already bound to a BLE
        connection.
        """
        if channel in BLE_CONNECTIONS:
            raise ValueError(
                f"Channel '{channel}' is already bound to a BLE "
                f"connection."
            )
        BLE_CONNECTIONS[channel] = self
        self.channel = channel
        self._service_uuid = service
        self._characteristic_uuid = characteristic
        self._encoding = encoding
        self._filters = filters
        # Auto-inject the service into optional_services so
        # requestDevice grants access even if the developer filtered
        # on name or manufacturerData rather than services.
        services = list(optional_services or [])
        if service not in services:
            services.append(service)
        self._optional_services = services
        self._device = None
        self._characteristic = None
        self._properties = None
        self._read_key = None
        self._closing = False
        # Subscribe to the channel for send, read, and close.
        invent.subscribe(
            handler=self._handle_send,
            to_channel=channel,
            when_subject="send",
        )
        invent.subscribe(
            handler=self._handle_read,
            to_channel=channel,
            when_subject="read",
        )
        invent.subscribe(
            handler=self._handle_close,
            to_channel=channel,
            when_subject="close",
        )
        # Publish the initial connecting status, then start.
        self._publish_status("connecting")
        asyncio.create_task(self._connect())

    def _publish_status(self, status, reason=None):
        """
        Publish a status message to the channel.
        """
        invent.publish(
            message=invent.Message("status", status=status, reason=reason),
            to_channel=self.channel,
        )

    def _publish_message(self, data):
        """
        Publish received data to the channel.
        """
        invent.publish(
            message=invent.Message("message", data=data),
            to_channel=self.channel,
        )

    def _cleanup(self):
        """
        Remove from the channel registry and unsubscribe handlers.
        Does not touch the device; the caller handles device detach.
        """
        BLE_CONNECTIONS.pop(self.channel, None)
        invent.unsubscribe(
            handler=self._handle_send,
            from_channel=self.channel,
            when_subject="send",
        )
        invent.unsubscribe(
            handler=self._handle_read,
            from_channel=self.channel,
            when_subject="read",
        )
        invent.unsubscribe(
            handler=self._handle_close,
            from_channel=self.channel,
            when_subject="close",
        )

    async def _connect(self):
        """
        Select a device (matching authorised first, picker fallback),
        share or create its GATT connection, fetch the characteristic,
        and start notifications if supported. On unrecoverable failure
        publishes "error" and cleans up.
        """
        try:
            device = await self._select_device()
            if device is None:
                self._publish_status(
                    "error",
                    reason="No device available or picker cancelled.",
                )
                self._cleanup()
                return
            # Find or create the shared device wrapper.
            ble_device = BLE_DEVICES.get(device.id)
            if ble_device is None:
                ble_device = _InventBLEDevice(device)
                BLE_DEVICES[device.id] = ble_device
            self._device = ble_device
            ble_device.attach(self)
            server = await ble_device.connect_server()
            service = await server.getPrimaryService(self._service_uuid)
            self._characteristic = await service.getCharacteristic(
                self._characteristic_uuid
            )
            self._properties = self._characteristic.properties
            if getattr(self._properties, "notify", False):
                self._characteristic.addEventListener(
                    "characteristicvaluechanged",
                    self._on_characteristic_changed,
                )
                await self._characteristic.startNotifications()
            self._publish_status("open")
        except Exception as e:
            self._publish_status(
                "error", reason=f"Unexpected error during connection. {e}"
            )
            if self._device:
                self._device.detach(self)
                self._device = None
            self._cleanup()

    async def _select_device(self):
        """
        Return the first already-authorised device matching the
        filters; otherwise prompt the user via the browser picker.
        Returns `None` if the picker is cancelled.
        """
        bluetooth = pyscript.window.navigator.bluetooth
        try:
            devices = await bluetooth.getDevices()
            for device in devices:
                if self._device_matches(device):
                    return device
        except Exception:
            # getDevices() may be unsupported; fall through to picker.
            pass
        # No existing match: open the picker. Requires a user gesture.
        request_options = {"optionalServices": self._optional_services}
        if self._filters:
            request_options["filters"] = self._filters
        else:
            # No developer filters: default to the channel's service.
            request_options["filters"] = [{"services": [self._service_uuid]}]
        try:
            return await bluetooth.requestDevice(to_js(request_options))
        except Exception:
            return None

    def _device_matches(self, device):
        """
        True if the device matches any of the developer's filters.
        Web Bluetooth does not expose service UUIDs on
        already-authorised devices without a GATT connection, so
        matching is by name only when filters specify a name; with
        no filters or only service filters we do not match (the
        picker will be opened instead to ensure user consent).
        """
        if not self._filters:
            return False
        name = getattr(device, "name", None)
        for filter_dict in self._filters:
            wanted_name = filter_dict.get("name")
            if wanted_name and name == wanted_name:
                return True
            prefix = filter_dict.get("namePrefix")
            if prefix and name and name.startswith(prefix):
                return True
        return False

    def _on_characteristic_changed(self, event):
        """
        Handle a notification from the characteristic. The value is
        a DataView; convert to bytes and publish on the channel.
        """
        value = event.target.value
        # DataView: read each byte via getUint8.
        length = value.byteLength
        data = bytes(value.getUint8(i) for i in range(length))
        self._publish_message(data)

    def _handle_send(self, message):
        """
        Write the message's data to the characteristic. Publishes an
        "error" status if the characteristic does not support write
        or if the write itself fails.
        """
        if not getattr(self._properties, "write", False) and not getattr(
            self._properties, "writeWithoutResponse", False
        ):
            self._publish_status(
                "error",
                reason="Characteristic does not support write.",
            )
            return
        asyncio.create_task(self._send(message.data))

    async def _send(self, data):
        """
        Encode data as bytes and write to the characteristic. Strings
        are encoded via the configured encoding.
        """
        if isinstance(data, str):
            payload = data.encode(self._encoding)
        else:
            payload = bytes(data)
        buffer = pyscript.window.Uint8Array.new(len(payload))
        for index, byte_value in enumerate(payload):
            buffer[index] = byte_value
        try:
            await self._characteristic.writeValue(buffer)
        except Exception as e:
            self._publish_status("error", reason=f"Write failed. {e}")

    def _handle_read(self, message):
        """
        Trigger a one-shot read of the characteristic. The result is
        stored in the datastore at `message.result_key` if supplied,
        or at the last-supplied key for this channel. Publishes an
        "error" if no key has ever been supplied, if the
        characteristic does not support read, or if the read fails.
        """
        key = getattr(message, "result_key", None)
        if key is not None:
            self._read_key = key
        if self._read_key is None:
            self._publish_status(
                "error",
                reason="No result_key supplied for read.",
            )
            return
        if not getattr(self._properties, "read", False):
            reason = "Characteristic does not support read."
            self._publish_status("error", reason=reason)
            invent.datastore[self._read_key] = BLE_ERROR + f": {reason}"
            return
        asyncio.create_task(self._read(self._read_key))

    async def _read(self, result_key):
        """
        Perform a one-shot read and store the value in the datastore.
        On failure, publishes "error" on the channel and stores the
        BLE_ERROR flag at the result key.
        """
        try:
            value = await self._characteristic.readValue()
            length = value.byteLength
            data = bytes(value.getUint8(i) for i in range(length))
            invent.datastore[result_key] = data
        except Exception as e:
            reason = f"Read failed. {e}"
            self._publish_status("error", reason=reason)
            invent.datastore[result_key] = BLE_ERROR + f": {reason}"

    def _handle_close(self, message):
        """
        Close this channel. The underlying device connection is torn
        down only if this is the last channel bound to it.
        """
        if self._closing:
            return
        self._closing = True
        asyncio.create_task(self._close_channel())

    async def _close_channel(self):
        """
        Stop notifications if running, detach from the shared device,
        publish "closed", and clean up the channel registry.
        """
        try:
            if self._characteristic and getattr(
                self._properties, "notify", False
            ):
                await self._characteristic.stopNotifications()
        except Exception:
            pass
        if self._device:
            self._device.detach(self)
            self._device = None
        self._cleanup()
        self._publish_status("closed")

    def _on_device_disconnected(self):
        """
        Called by the shared device wrapper when the GATT server has
        unexpectedly disconnected. Publishes "closed" with a reason
        and cleans up the channel. The developer may reconnect by
        calling `ble_connection` again.
        """
        self._closing = True
        self._device = None
        self._cleanup()
        self._publish_status(
            "closed", reason="Device disconnected unexpectedly."
        )


# Public aliases for the internal connection classes.
web_socket = _InventWebSocket
serial_connection = _InventSerial
ble_connection = _InventBLE
