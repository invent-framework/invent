"""
Provides the mechanism for a simple key / value store that behaves like a
Python dictionary and sits on top of IndexDB via PyScript.

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

from pyscript import Storage
from .channels import Message, publish


class DataStore(Storage):
    """
    A simple key/value data store.

    Wraps PyScript's storage capabilities so it looks and feels mostly like a
    Python `dict`. Publishes messages when setting or deleting items so other
    aspects of the application can observe such changes of state.
    """

    def __setitem__(self, key, value):
        """
        Set the value against the given key using PyScript's Storage class.

        Publishes a message whose type is the item's key, along with the new
        value, to the "store-data" channel.
        """
        publish(
            Message(subject=key, value=value),
            to_channel="store-data",  # TODO: datastore:set
        )
        # TODO: check if callable, extract arg names, store somewhere.
        super().__setitem__(key, value)

    def __delitem__(self, key):
        """
        Delete the item stored against the given key.

        Publishes a message whose type is the item's the key, to the
        "delete-data" channel.
        """
        publish(
            Message(subject=key), to_channel="delete-data"
        )  # datastore:delete
        super().__delitem__(key)
