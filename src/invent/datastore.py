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

    #: Channel name to indicate a value has been set in the datastore.
    DATASTORE_SET_CHANNEL = "datastore:set"
    #: Channel name to indicate a value has been deleted from the datastore.
    DATASTORE_DELETE_CHANNEL = "datastore:delete"

    def __setitem__(self, key, value):
        """
        Set the value against the given key using PyScript's Storage class.

        Publishes a message whose type is the item's key, along with the new
        value, to the invent.datastore.DATASTORE_SET_CHANNEL channel.
        """
        publish(
            Message(subject=key, value=value),
            to_channel=self.DATASTORE_SET_CHANNEL
        )
        super().__setitem__(key, value)

    def __delitem__(self, key):
        """
        Delete the item stored against the given key.

        Publishes a message whose type is the item's the key, to the
        invent.datastore.DATASTORE_DELETE_CHANNEL channel.
        """
        publish(Message(subject=key), to_channel=self.DATASTORE_DELETE_CHANNEL)
        super().__delitem__(key)
