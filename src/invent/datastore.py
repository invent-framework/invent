"""
Provides the mechanism for a simple key / value store that behaves like a
Python dictionary. The resulting data store can sit on top of various data
backends, that are also specified in this module, depending on the use
case.

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

import json
from pyscript import Storage, window
from .channels import Message, publish


class DataBackend:
    """
    Defines the behaviour of a backend provider for the DataStore class. This
    mostly looks like a Python dictionary. The following methods must be
    implemented by any subclass: `clear`, `keys`, `sync`, `__setitem__`,
    `__getitem__`, and `__delitem__`.
    """

    def clear(self):
        """
        Clear data from the backend.
        """
        raise NotImplementedError

    def copy(self):
        """
        Returns a Python `dict` copy of the data store.
        """
        return {k: v for k, v in self.items()}

    def get(self, key, default=None):
        """
        Return the value of the item with the specified key.
        """
        if key in self:
            return self[key]
        return default

    def items(self):
        """
        Yield over the key/value pairs in the data store.
        """
        for key in self.keys():
            value = self[key]
            yield (key, value)

    def keys(self):
        """
        Get the keys of the data store.
        """
        raise NotImplementedError

    def pop(self, key, default=None):
        """
        Pop the specified item from the data store and return the associated
        value.
        """
        if key in self:
            result = self[key]
            del self[key]
        else:
            result = default
        return result

    def popitem(self):
        """
        Raises a `NotImplementedError` because it doesn't make sense in this
        context.
        """
        raise NotImplementedError()

    def setdefault(self, key, value=None):
        """
        Returns the value of the item with the specified key.

        If the key does not exist, insert the key, with the specified value.

        Default value is `None`.
        """
        if key in self:
            return self[key]
        self[key] = value
        return value

    async def sync(self):
        """
        Synchronise the data store with the backend.
        """
        raise NotImplementedError()

    def update(self, *args, **kwargs):
        """
        For each key/value pair in the iterable, insert them into the
        data store.
        """
        new_items = {}
        for arg in args:
            if isinstance(arg, dict):
                new_items.update(arg)
        new_items.update(kwargs)
        for key, value in new_items.items():
            self[key] = value

    def values(self):
        """
        Return a list of the values stored in the data store.
        """
        result = []
        for key in self.keys():
            result.append(self[key])
        return result

    def __len__(self):
        """
        The number of items in the data store.
        """
        return len(list(self.keys()))

    def __setitem__(self, key, value):
        """
        Set the value against the given key.
        """
        raise NotImplementedError

    def __getitem__(self, key):
        """
        Get the value stored against the given key.
        """
        raise NotImplementedError

    def __delitem__(self, key):
        """
        Delete the item stored against the given key.
        """
        raise NotImplementedError

    def __iter__(self):
        """
        Return an iterator over the keys.
        """
        return (key for key in self.keys())

    def __contains__(self, key):
        """
        Checks if a key is in the datastore.
        """
        return key in self.keys()


class _FakeStorage(dict):
    """
    A Python dict with some JavaScript method shims. This is used if
    window.localStorage is not available due to the security context in which
    Invent finds itself.

    This localStorage lasts only as long as the page.
    """

    @property
    def length(self):
        return len(self)

    def key(self, i):
        return list(self.keys())[i]

    def getItem(self, key):
        return self[key]

    def setItem(self, key, value):
        self[key] = value

    def removeItem(self, key):
        del self[key]


class LocalStorageBackend(DataBackend):
    """
    A simple key/value data store using the browser's `localStorage`. If the
    browser's `localStorage` is not available, a Python dict based solution
    based upon _FakeStorage is used instead.

    Wraps a JavaScript `Storage` object for browser based data storage. Looks
    and feels mostly like a Python `dict` but has the same characteristics
    as a JavaScript `localStorage` object.

    For more information see:

    <https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API>
    """

    def __init__(self, **kwargs):
        """
        The underlying `Storage` object is an instance of `Window.localStorage`
        (it persists between browser opening/closing). Any `**kwargs` are added
        to the dictionary. All keys are silently prepended with the value of
        self.namespace.
        """
        self.namespace = "invent-"
        try:
            self.store = window.localStorage
        except ImportError:  # pragma: no cover
            # If the browser's localStorage isn't available, fall back to a Python
            # dict based solution. Such a situation may arise in certain security
            # contexts or if the app is served inside an iFrame.
            self.store = _FakeStorage()
        if kwargs:
            self.update(kwargs)

    def clear(self):
        """
        Removes all items from the data store.
        """
        return self.store.clear()

    def keys(self):
        """
        Returns a list of keys stored by the user.
        """
        result = []
        namespace_slice = len(self.namespace)
        for i in range(0, self.store.length):
            key = self.store.key(i)
            if key.startswith(self.namespace):
                real_key = key[namespace_slice:]
                result.append(real_key)
        return result

    async def sync(self):
        """
        No need to sync `localStorage` as it's always up to date.
        """
        return

    def _namespace_key(self, key):
        """
        Convenience method to create a properly namespaced key.
        """
        return f"{self.namespace}{key}"

    def __getitem__(self, key):
        """
        Get and JSON deserialize the item stored against the given key.
        """
        if key in self:
            return json.loads(self.store.getItem(self._namespace_key(key)))
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        """
        Set the value (as a JSON string) against the given key.

        The underlying JavaScript Storage only stored values as strings.
        """
        result = self.store.setItem(
            self._namespace_key(key), json.dumps(value)
        )
        return result

    def __delitem__(self, key):
        """
        Delete the item stored against the given key.
        """
        if key in self:
            result = self.store.removeItem(self._namespace_key(key))
            return result
        else:
            raise KeyError(key)


class IndexDBBackend(Storage, DataBackend):
    """
    A simple key/value data store using the browser's `indexedDB` via
    PyScript's own Storage class.

    Wraps a JavaScript `IDBDatabase` object for browser based data storage.
    Looks and feels mostly like a Python `dict` but has the same characteristics
    as a JavaScript `indexedDB` object.

    For more information see:

    <https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API>
    """

    ...


class RemoteStorageBackend(DataBackend):
    """
    A simple key/value data store using a remote server.

    Wraps a remote server for data storage. Looks and feels mostly like a Python
    `dict` but uses a simple API to store and retrieve data via background
    HTTP requests.
    """

    # TODO: Implement this class to store data remotely.

    ...


class DataStore(DataBackend):
    """
    A simple key/value data store for the Invent platform.

    Wraps PyScript's storage capabilities so it looks and feels mostly like a
    Python `dict`. Publishes messages when setting or deleting items so other
    aspects of the application can observe such changes of state.

    The DataStore can sit on top of various data backends, that are also
    specified in this module, depending on the use case. If no backend is
    provided, a default `LocalStorageBackend` is used.
    """

    #: Channel name to indicate a value has been set in the datastore.
    DATASTORE_SET_CHANNEL = "datastore:set"
    #: Channel name to indicate a value has been deleted from the datastore.
    DATASTORE_DELETE_CHANNEL = "datastore:delete"

    def __init__(self, _backend=None, **kwargs):
        """
        Create a new data store with the given _backend. If no _backend is
        provided, a default `LocalStorageBackend` is used.

        Any `**kwargs` are passed to the backend.
        """
        if _backend is None:
            _backend = LocalStorageBackend(**kwargs)
        else:
            _backend.update(**kwargs)
        self.backend = _backend

    def clear(self):
        """
        Clear all data from the data store.
        """
        self.backend.clear()

    def keys(self):
        """
        Get the keys of the data store.
        """
        return self.backend.keys()

    async def sync(self):
        """
        Synchronise with the backend provider.
        """
        await self.backend.sync()

    def __getitem__(self, key):
        """
        Get the value stored against the given key.
        """
        return self.backend[key]

    def __setitem__(self, key, value):
        """
        Set the value against the given key.

        Publishes a message whose type is the item's key, along with the new
        value, to the self.DATASTORE_SET_CHANNEL channel.
        """
        self.backend[key] = value
        publish(
            Message(subject=key, value=value),
            to_channel=self.DATASTORE_SET_CHANNEL,
        )

    def __delitem__(self, key):
        """
        Delete the item stored against the given key.

        Publishes a message whose type is the item's the key, to the
        "delete-data" channel.
        """
        del self.backend[key]
        publish(
            Message(subject=key),
            to_channel=self.DATASTORE_DELETE_CHANNEL,
        )
