import asyncio
import invent
import umock
from invent.tools import geo


async def test_position_single_detect():
    """
    Use of the simple `position` function to get a one shot indication of the
    device's current geolocation.
    """
    result_key = "current_position"
    got_detecting = asyncio.Event()  # Used to wait for the detecting event.
    got_position = asyncio.Event()  # Used to wait for the position event.

    def handler(message):
        if message.value == geo.DETECTING:
            got_detecting.set()
        elif isinstance(message.value, dict):
            got_position.set()

    invent.subscribe(
        handler,
        to_channel=invent.datastore.DATASTORE_SET_CHANNEL,
        when_subject=result_key,
    )

    geo.position(
        result_key=result_key,
        enableHighAccuracy=False,
        timeout=5000,
        maximumAge=10000,
    )

    await got_detecting.wait()
    await got_position.wait()
    assert (
        result_key in invent.datastore
    ), "Expected key not found in datastore"
    assert isinstance(
        invent.datastore[result_key], dict
    ), "Result not stored in datastore as dict."  # It's a dictionary!
    # Check the dictionary contains expected keys.
    for key in [
        "latitude",
        "longitude",
        "altitude",
        "accuracy",
        "altitude_accuracy",
        "heading",
        "speed",
    ]:
        assert (
            key in invent.datastore[result_key]
        ), "Result not stored with expected keys."


async def test_position_watch():
    """
    Use of the simple `position` function to watch the device's geolocation.

    Since we can't force the browser to change its position, this test uses
    uMock to simulate the browser's geolocation API (specifically the calls to
    `watchPosition` and `clearWatch`).
    """
    result_key = "current_position"
    got_detecting = asyncio.Event()  # Used to wait for the detecting event.
    got_position = asyncio.Event()  # Used to wait for the position event.

    def handler(message):
        if message.value == geo.DETECTING:
            got_detecting.set()
        elif isinstance(message.value, dict):
            got_position.set()

    invent.subscribe(
        handler,
        to_channel=invent.datastore.DATASTORE_SET_CHANNEL,
        when_subject=result_key,
    )

    with umock.patch("invent.tools.geo:window") as mock_window:
        stop = geo.position(
            result_key=result_key,
            enableHighAccuracy=False,
            timeout=5000,
            maximumAge=10000,
            update=True,
        )
        mock_window.navigator.geolocation.watchPosition.assert_called_once()
        stop()  # Stop watching the position.
        mock_window.navigator.geolocation.clearWatch.assert_called_once()
