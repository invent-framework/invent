"""
PyperCard is a simple HyperCard inspired framework for PyScript for building
graphical apps in Python.

Based on original pre-COVID work by [Nicholas H.Tollervey.](https://ntoll.org/)

Copyright (c) 2023 Anaconda Inc.

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
from js import localStorage


class DataStore:
    """
    A simple key/value data store.

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
        to the dictionary.
        """
        self.store = localStorage
        if kwargs:
            self.update(kwargs.items())

    def clear(self):
        """
        Removes all items from the data store.
        """
        return self.store.clear()

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
        for i in range(0, len(self)):
            key = self.store.key(i)
            value = self[key]
            yield (key, value)

    def keys(self):
        """
        Returns a list of keys stored by the user.
        """
        result = []
        for i in range(0, len(self)):
            result.append(self.store.key(i))
        return result

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
        Makes no sense given the underlying JavaScript Storage object's
        behaviour. Raises a `NotImplementedError`.
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

    def update(self, iterable):
        """
        For each key/value pair in the iterable, insert them into the
        data store.
        """
        for key, value in iterable:
            self[key] = value

    def values(self):
        """
        Return a list of the values stored in the data store.
        """
        result = []
        for i in range(0, len(self)):
            key = self.store.key(i)
            result.append(self[key])
        return result

    def __len__(self):
        """
        The number of items in the data store.
        """
        return self.store.length

    def __getitem__(self, key):
        """
        Get and JSON deserialize the item stored against the given key.
        """
        if key in self:
            return json.loads(self.store.getItem(key))
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        """
        Set the value (as a JSON string) against the given key.

        The underlying JavaScript Storage only stored values as strings.
        """
        return self.store.setItem(key, json.dumps(value))

    def __delitem__(self, key):
        """
        Delete the item stored against the given key.
        """
        if key in self:
            return self.store.removeItem(key)
        else:
            raise KeyError(key)

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
