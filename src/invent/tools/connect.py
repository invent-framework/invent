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

    On failure, the `SERIAL_ERROR` flag is stored at `result_key`
    instead, along with contextual information.

    This wraps `navigator.serial.getPorts()`, which does not require a
    user gesture: it returns ports previously granted access. To
    prompt the user to authorise a new port, use `serial_connection`.

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
    Convert a SerialPort's getInfo() result into a Python dict using
    JS-style key names. Keys whose values are undefined are omitted.

    We do this to convert from a JavaScript object into a plain Python
    dict.
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
    List the BLE devices the user has already authorised, storing
    the result as a list of dicts in the datastore at `result_key`.

    Each entry contains `id` and `name` keys, mirroring the relevant
    fields of the browser's `BluetoothDevice` object. Keys are
    JS-style camelCase to match the underlying browser API.

    On failure, the `BLE_ERROR` flag is stored at `result_key`
    instead, along with contextual information.

    This wraps `navigator.bluetooth.getDevices()`, which does not
    require a user gesture: it returns devices previously granted
    access. To prompt the user to authorise a new device, use
    `ble_connection`.

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
    with the human-relevant identifying fields. The `name` field may
    be missing on some devices; in that case it is omitted.
    """
    result = {"id": device.id}
    name = getattr(device, "name", None)
    if name is not None:
        result["name"] = name
    return result


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


class _InventSerial:
    """
    Manage a connection to a serial port and binds it to the specified
    channel(s). On first use the browser will prompt the user to
    authorise a port via the picker; subsequent calls will reuse
    already-authorised ports matching the supplied USB filters.

    The channel argument can be a single channel name string or a
    list of channel name strings.

    All communication with the serial port is via the channel(s) in the
    usual Invent way:

    - Publish a message with subject "send" and a `.data` attribute
      to forward data through the serial port.
    - Publish a message with subject "close" to close the connection
      and clean up.
    - Subscribe to the channel(s) with a subject "message" to receive
      incoming data (arrives as `.data` on the message).
    - Subscribe to the channel(s) with a subject "status" to receive
      connection state changes (arrives as `.status` on the message,
      one of: "connecting", "open", "error", "closed", "reconnecting").
      If the status is "error", a `.reason` attribute may be included
      with a description of the error.

    Messages published with subject "send" before the connection is
    open will be queued and sent automatically once the connection is
    ready.

    Two connection modes are available:

    - "line" (default): incoming bytes are buffered, decoded with the
      configured encoding, and published as text once the newline
      delimiter is seen. The delimiter is retained on each emitted
      line. Outgoing strings are encoded via the configured encoding,
      and the newline delimiter is appended if not already present.
    - "raw": incoming data is published as raw bytes; outgoing data
      is sent as-is (strings are encoded to bytes via the configured
      encoding).

    USB filters use the JS-style camelCase format from the Web Serial
    API, e.g. `[{"usbVendorId": 0x2341, "usbProductId": 0x0043}]`.
    With no filter, the first already-authorised port is used; if
    none is available, the picker is shown with no constraint.

    If `auto_reconnect` is True, the connection will attempt to
    re-open on unexpected loss, up to `reconnect_attempts` times,
    waiting `reconnect_delay` seconds between attempts. A normal
    close (via the "close" message) does not trigger reconnection.

    Example usage:

    ```python
    # Open a serial connection to an Arduino Uno and bind to a channel.
    connect.serial_connection(
        channel="my_device",
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
        channel,
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
        Configure the connection and bind to the channel(s). The
        connection itself opens asynchronously: subscribe to the
        channel with subject "status" to track its state.
        """
        if mode not in VALID_SERIAL_MODES:
            raise ValueError(
                f"Invalid mode '{mode}'. Must be one of: "
                f"{', '.join(sorted(VALID_SERIAL_MODES))}."
            )
        # Normalise channel to a list for registry purposes only.
        channels = channel if isinstance(channel, list) else [channel]
        for ch in channels:
            if ch in SERIAL_CONNECTIONS:
                raise ValueError(
                    f"Channel '{ch}' is already bound to a "
                    f"serial connection."
                )
        for ch in channels:
            SERIAL_CONNECTIONS[ch] = self
        self.channel = channel
        self._channels = channels
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
        Remove from the registry and unsubscribe handlers.
        """
        for ch in self._channels:
            SERIAL_CONNECTIONS.pop(ch, None)
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
            line = bytes(self._read_buffer[:pos + dlen])
            self._read_buffer = bytearray(
                self._read_buffer[pos + dlen:]
            )
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
    Represents a shared GATT (Generic ATTribute Profile) server
    connection for a single physical BLE device. Multiple channels
    may be bound to characteristics on the same device; this class is
    the single point at which the GATT connection is opened, observed,
    and torn down.

    Lifecycle is reference-counted against the channel instances
    using it: when the last channel detaches, the GATT server is
    disconnected and the device entry is removed from BLE_DEVICES.

    This is hidden plumbing; developers interact only with
    `_InventBLE` via channels.

    Devices have characteristics (e.g. temperature, humidity), and
    characteristics can be bound to meaningfully named Invent channels.
    The channels are what the developer interacts with, and the types
    of message they publish and subscribe to on those channels are
    defined by the characteristic's properties (e.g. read, write, notify).

    This class represents the underlying connection to the single
    physical device, and manages the GATT server connection and the set
    of channels bound to it. It listens for unexpected disconnects at
    the device level, and notifies all bound channels if that happens
    so they can update their state accordingly.
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

    All communication with the characteristic is via the channel in
    the usual Invent way:

    - Publish a message with subject "send" and a `.data` attribute
      to write bytes to the characteristic (requires the
      characteristic to support write).
    - Publish a message with subject "read" and a `.result_key`
      attribute to trigger a one-shot read; the value is stored in
      the datastore at `result_key`. The first "read" message on a
      channel must include `result_key`; subsequent "read" messages
      may omit it to reuse the last key, or supply a new key to
      rebind.
    - Publish a message with subject "close" to close this channel.
      Other channels on the same device remain open; the GATT
      connection is only torn down when the last channel closes.
    - Subscribe to the channel with subject "message" to receive
      notifications from the characteristic (arrives as `.data` on
      the message, as raw bytes).
    - Subscribe to the channel with subject "status" to receive
      connection state changes (arrives as `.status`, one of:
      "connecting", "open", "error", "closed"). If the status is
      "error", a `.reason` attribute describes the cause.

    Characteristic capability is auto-detected at connect time:
    if the characteristic supports notify, notifications are started
    and incoming values publish as "message". Attempting "send" on a
    characteristic that does not support write, or "read" on one
    that does not support read, publishes an "error" status.

    BLE is packet-based: values are always raw bytes. Strings passed
    to "send" are encoded using the configured `encoding`.

    Browser support: Chrome, Edge, Opera, Samsung Internet. Not
    supported in Firefox or Safari.

    Example usage:

    ```python
    # Bind a channel to the micro:bit temperature characteristic.
    connect.ble_connection(
        channel="temperature",
        service="e95d6100-251d-470a-a062-fa1922dfa9a8",
        characteristic="e95d9250-251d-470a-a062-fa1922dfa9a8",
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
        Configure the channel binding and kick off the async
        connection. The connection itself opens asynchronously;
        subscribe to "status" to track its state.
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
            request_options["filters"] = [
                {"services": [self._service_uuid]}
            ]
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


# Expose the classes as module-level functions for ease of use.
web_socket = _InventWebSocket
serial_connection = _InventSerial
ble_connection = _InventBLE