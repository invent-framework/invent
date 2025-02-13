"""
Defines a function for detecting and updating the current position of the
device.

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

import invent
from invent.i18n import _
from pyscript.ffi import create_proxy
from pyscript import window


try:
    window.navigator.geolocation
    GEOLOCATION_AVAILABLE = True
except AttributeError:
    GEOLOCATION_AVAILABLE = False


#: Flag for the datastore to indicate a pending status.
DETECTING = "_GEO_DETECTING"
#: Flag for the datastore to indicate an error status.
ERROR = "_GEO_ERROR"


def position(result_key, update=False, **options):
    """
    Detect the current position of the device and update the datastore with the
    result using the result_key. Before the position is detected, the datastore
    will be updated with a flag using the value of DETECTING.

    The position will be a dictionary with the following items:

      - latitude: a float representing the position's latitude in decimal
        degrees.
      - longitude: a float representing the position's longitude in decimal
        degrees.
      - altitude: a float representing the position's altitude in meters,
        relative to nominal sea level. This value can be None if the
        browser cannot provide the data.
      - accuracy: a float representing the accuracy of the latitude and
        longitude properties, expressed in meters.
      - altitude_accuracy: a float representing the accuracy of the altitude
        expressed in meters. This value can be None if the browser cannot
        provide the data.
      - heading: a float representing the direction in which the device is
        facing. This value, specified in degrees, indicates how far off from
        heading true north the device is. 0 degrees represents true north, and
        the direction is determined clockwise (which means that east is 90
        degrees and west is 270 degrees). If speed is 0 or the device is unable
        to provide heading information, heading is None.
      - speed: a float representing the velocity of the device in meters per
        second. This value can be None if the browser cannot provide the data.

    If the update flag is set to True, the position will be updated in the
    datastore whenever it changes.

    The options parameter can be used to specify the following:

      - enableHighAccuracy: a boolean that indicates the application would like
        to receive the best possible results. If True and if the device is able
        to provide a more accurate position, it will do so. Note that this can
        result in slower response times or increased power consumption (with a
        GPS chip on a mobile device for example). On the other hand, if False,
        the device can take the liberty of optimizing the device's power
        consumption and accuracy of the returned position. Default is True.
      - timeout: a positive long value representing the maximum length of time
        (in milliseconds) the device is allowed to take in order to return a
        position. The default value is 0, which means there is no maximum
        length of time.
      - maximumAge: a positive long value indicating the maximum age in
        milliseconds of a possible cached position that is acceptable to return.
        If set to 0, it means that the device cannot use a cached position and
        must attempt to retrieve the real current position. If set to Infinity
        the device must return a cached position regardless of its age. Default
        is 0.

    The function returns a function that can be called to stop watching the
    position. This is only relevant if the update flag is set to True.

    If the browser doesn't support geolocation, a SystemError will be raised.
    """

    if not GEOLOCATION_AVAILABLE:
        raise SystemError(
            _("Sorry, your browser doesn't support geolocation!")
        )

    def _on_position(position):
        """
        Handle the position being detected.
        """
        invent.datastore[result_key] = {
            "latitude": position.coords.latitude,
            "longitude": position.coords.longitude,
            "altitude": position.coords.altitude,
            "accuracy": position.coords.accuracy,
            "altitude_accuracy": position.coords.altitudeAccuracy,
            "heading": position.coords.heading,
            "speed": position.coords.speed,
        }

    def _on_error(error):
        """
        Handle the error.

        See: https://developer.mozilla.org/en-US/docs/Web/API/GeolocationPositionError
        """
        errors = {
            1: _("Permission denied"),
            2: _("Position unavailable"),
            3: _("Timeout"),
        }
        invent.datastore[result_key] = (
            ERROR + f": {errors[error.code]} ({error.message})."
        )

    invent.datastore[result_key] = DETECTING

    geo_options = {
        "enableHighAccuracy": True,
        "timeout": 0,
        "maximumAge": 0,
    }.update(options)

    watch_id = None
    if update:
        watch_id = window.navigator.geolocation.watchPosition(
            create_proxy(_on_position), create_proxy(_on_error), geo_options
        )
    else:
        window.navigator.geolocation.getCurrentPosition(
            create_proxy(_on_position), create_proxy(_on_error), geo_options
        )

    def _stop():
        """
        Stop watching the position.
        """
        if watch_id:
            window.navigator.geolocation.clearWatch(watch_id)

    return _stop
