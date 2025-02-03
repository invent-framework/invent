import invent
import upytest
import umock
from pyscript import window
from invent.datastore import _FakeStorage, LocalStorageBackend, IndexDBBackend


# Tests for default LocalStorageBackend based datastore.


def test_fake_storage_js_methods():
    """
    The _fakeStorage class is a Python dict with some "fake" JavaScript method
    shims to make it look like a browser's localStorage object. This class is
    the fallback for when window.localStorage is not available to the Invent
    framework due to security context issues (e.g. it's running in an iframe).
    """
    faker = _FakeStorage(foo="bar")
    assert faker.length == 1
    assert faker.key(0) == "foo"
    assert faker.getItem("foo") == "bar"
    faker.setItem("baz", "qux")
    assert faker.getItem("baz") == "qux"
    faker.removeItem("baz")
    assert "baz" not in faker


def test_datastore_default_init():
    """
    localStorage is used.
    """
    ds = invent.DataStore()
    assert isinstance(ds.backend, LocalStorageBackend)


def test_datastore_init_with_values():
    """
    Initialise the dictionary with key/value arguments.
    """
    ds = invent.DataStore(foo="bar", baz="qux")
    assert ds["foo"] == "bar"
    assert ds["baz"] == "qux"
    assert len(ds) == 2, ds.keys()


def test_datastore_clear():
    """
    The clear method empties the datastore.
    """
    ds = invent.DataStore()
    ds["a"] = 1
    ds["b"] = 2
    assert len(ds) == 2
    ds.clear()
    assert len(ds) == 0


def test_datastore_copy():
    """
    The copy method returns a new Python dictionary containing the items in
    the datastore.
    """
    ds = invent.DataStore()
    ds["a"] = 1
    ds["b"] = 2
    copy_ds = ds.copy()
    assert copy_ds == {"a": 1, "b": 2}
    assert copy_ds is not ds


def test_datastore_get_with_value():
    """
    The get method returns the expected value, if the key exists.
    """
    ds = invent.DataStore()
    ds["a"] = 1
    assert ds.get("a") == 1


def test_datastore_get_missing_key_no_default():
    """
    The get method returns None by default, if the key doesn't exist.
    """
    ds = invent.DataStore()
    assert ds.get("a") is None


def test_datastore_get_missing_key_with_default():
    """
    The get method returns the given default value, if the key doesn't exist.
    """
    ds = invent.DataStore()
    assert ds.get("a", "foo") == "foo"


def test_datastore_items():
    """
    The items method makes it possible to lazily iterate over the items
    contained within the datastore.
    """
    ds = invent.DataStore()
    ds["a"] = 1
    ds["b"] = 2
    for k, v in ds.items():
        assert k in ds
        assert ds[k] == v


def test_datastore_keys():
    """
    The keys method returns a list of keys contained in the datastore.
    """
    ds = invent.DataStore()
    ds["a"] = 1
    ds["b"] = 2
    assert set(ds.keys()) == {
        "a",
        "b",
    }


def test_datastore_pop():
    """
    An existing item is popped from the datastore.
    """
    ds = invent.DataStore()
    ds["a"] = 1
    ds["b"] = 2
    val = ds.pop("a")
    assert val == 1
    assert "a" not in ds


def test_datastore_pop_no_key():
    """
    Popping a non-existent item returns None by default.
    """
    ds = invent.DataStore()
    assert ds.pop("foo") is None


def test_datastore_pop_no_key_with_default():
    """
    Popping a non-existent item returns the given default value.
    """
    ds = invent.DataStore()
    assert ds.pop("foo", True) is True


def test_datastore_popitem():
    """
    NotImplemented
    """
    ds = invent.DataStore()
    with upytest.raises(NotImplementedError):
        ds.popitem()


def test_datastore_setdefault_no_key():
    """
    If the key doesn't exist, by default returns None and sets key to an
    associated value of None.
    """
    ds = invent.DataStore()
    assert ds.setdefault("a") is None
    assert "a" in ds
    assert ds["a"] is None


def test_datastore_setdefault_has_key():
    """
    If the key exists, just return the associated value and do NOT update the
    value.
    """
    ds = invent.DataStore()
    ds["a"] = 1
    assert ds.setdefault("a") == 1
    assert ds["a"] == 1


def test_datastore_setdefault_no_key_with_default():
    """
    If the key doesn't exist, return the default value and set the key to the
    given default value.
    """
    ds = invent.DataStore()
    assert ds.setdefault("a", True) is True
    assert "a" in ds
    assert ds["a"] is True


def test_datastore_update():
    """
    Given an iterable of key/value pairs, insert them into the datastore.
    """
    to_insert = {"a": 1, "b": 2}
    ds = invent.DataStore()
    ds.update(to_insert)
    assert len(ds) == 2
    assert ds["a"] == 1
    assert ds["b"] == 2


def test_datastore_values():
    """
    Returns a list of the stored values.
    """
    ds = invent.DataStore()
    ds["a"] = 1
    ds["b"] = 2
    assert sorted(ds.values()) == [1, 2]


def test_datastore_len():
    """
    Builtin len works as expected.
    """
    ds = invent.DataStore()
    assert len(ds) == 0
    ds["a"] = 1
    assert len(ds) == 1


def test_localstoragebackend_namespace_key():
    """
    Ensure the expected namespaced key is created.
    """
    ds = invent.DataStore()
    assert ds.backend.namespace == "invent-"
    ds.backend.namespace = "test"
    result = ds.backend._namespace_key("foo")
    assert result == "testfoo"


async def test_datastore_get_set_del_item():
    """
    Getting, setting and deleting an item should work as expected.

    Setting and deleting should publish the expected messages on the
    "datastore" channel.
    """
    await invent.start_datastore()
    ds = invent.datastore
    mock_publish = umock.Mock()
    with upytest.raises(KeyError):
        ds["a"]
    with umock.patch("invent.datastore:publish", mock_publish):
        # Store the value 1 against the key "a".
        ds["a"] = 1
        # Check a message has been published on storing a value.
        assert mock_publish.call_count == 1
        # Extract the message.
        call_args = mock_publish.call_args_list[0]
        msg = call_args[0][0]
        # It's the expected "store" message with the key/value pair that was
        # just stored.
        assert msg._subject == "a"
        assert msg.value == 1
        # The message was also published to the expected "datastore" channel.
        assert (
            call_args[1]["to_channel"]
            == invent.datastore.DATASTORE_SET_CHANNEL
        )
        # Reset mock.
        mock_publish.reset_mock()
        # Check the stored value is actually in the datastore.
        assert ds["a"] == 1
        # Delete the newly created value.
        del ds["a"]
        # Check a message has now been published on deleting a value.
        assert mock_publish.call_count == 1
        # Extract the message.
        call_args = mock_publish.call_args_list[0]
        msg = call_args[0][0]
        # It's the expected "store" message with the key pair that was just
        # stored.
        assert msg._subject == "a"
        # The message was also published to the expected "datastore" channel.
        assert (
            call_args[1]["to_channel"]
            == invent.datastore.DATASTORE_DELETE_CHANNEL
        )
    with upytest.raises(KeyError):
        # Deleting via a non-existent key raises a KeyError.
        del ds["a"]


# Tests for IndexDBBackend based datastore.


async def test_index_db_default_init():
    """
    IndexDBBackend is used.
    """
    await invent.start_datastore(_backend=IndexDBBackend)
    ds = invent.datastore
    assert isinstance(ds.backend, IndexDBBackend)


async def test_index_db_init_with_values():
    """
    Initialise the dictionary with key/value arguments.
    """
    await invent.start_datastore(_backend=IndexDBBackend, foo="bar", baz="qux")
    ds = invent.datastore
    assert ds["foo"] == "bar"
    assert ds["baz"] == "qux"
    assert len(ds) == 2


async def test_index_db_clear():
    """
    The clear method empties the datastore.
    """
    await invent.start_datastore(_backend=IndexDBBackend)
    ds = invent.datastore
    ds["a"] = 1
    ds["b"] = 2
    assert len(ds) == 2
    ds.clear()
    assert len(ds) == 0


async def test_index_db_copy():
    """
    The copy method returns a new Python dictionary containing the items in
    the datastore.
    """
    await invent.start_datastore(_backend=IndexDBBackend)
    ds = invent.datastore
    ds["a"] = 1
    ds["b"] = 2
    copy_ds = ds.copy()
    assert copy_ds == {"a": 1, "b": 2}
    assert copy_ds is not ds


async def test_index_db_get_with_value():
    """
    The get method returns the expected value, if the key exists.
    """
    await invent.start_datastore(_backend=IndexDBBackend)
    ds = invent.datastore
    ds["a"] = 1
    assert ds.get("a") == 1


async def test_index_db_get_missing_key_no_default():
    """
    The get method returns None by default, if the key doesn't exist.
    """
    await invent.start_datastore(_backend=IndexDBBackend)
    ds = invent.datastore
    assert ds.get("a") is None


async def test_index_db_get_missing_key_with_default():
    """
    The get method returns the given default value, if the key doesn't exist.
    """
    await invent.start_datastore(_backend=IndexDBBackend)
    ds = invent.datastore
    assert ds.get("a", "foo") == "foo"


async def test_index_db_items():
    """
    The items method makes it possible to lazily iterate over the items
    contained within the datastore.
    """
    await invent.start_datastore(_backend=IndexDBBackend)
    ds = invent.datastore
    ds["a"] = 1
    ds["b"] = 2
    for k, v in ds.items():
        assert k in ds
        assert ds[k] == v


async def test_index_db_keys():
    """
    The keys method returns a list of keys contained in the datastore.
    """
    await invent.start_datastore(_backend=IndexDBBackend)
    ds = invent.datastore
    ds["a"] = 1
    ds["b"] = 2
    assert set(ds.keys()) == {
        "a",
        "b",
    }


async def test_index_db_pop():
    """
    An existing item is popped from the datastore.
    """
    await invent.start_datastore(_backend=IndexDBBackend)
    ds = invent.datastore
    ds["a"] = 1
    ds["b"] = 2
    val = ds.pop("a")
    assert val == 1
    assert "a" not in ds


async def test_index_db_pop_no_key():
    """
    Popping a non-existent item returns None by default.
    """
    await invent.start_datastore(_backend=IndexDBBackend)
    ds = invent.datastore
    assert ds.pop("foo") is None


async def test_index_db_pop_no_key_with_default():
    """
    Popping a non-existent item returns the given default value.
    """
    await invent.start_datastore(_backend=IndexDBBackend)
    ds = invent.datastore
    assert ds.pop("foo", True) is True


async def test_index_db_popitem():
    """
    NotImplemented
    """
    await invent.start_datastore(_backend=IndexDBBackend)
    ds = invent.datastore
    with upytest.raises(NotImplementedError):
        ds.popitem()


async def test_index_db_setdefault_no_key():
    """
    If the key doesn't exist, by default returns None and sets key to an
    associated value of None.
    """
    await invent.start_datastore(_backend=IndexDBBackend)
    ds = invent.datastore
    assert ds.setdefault("a") is None
    assert "a" in ds
    assert ds["a"] is None


async def test_index_db_setdefault_has_key():
    """
    If the key exists, just return the associated value and do NOT update the
    value.
    """
    await invent.start_datastore(_backend=IndexDBBackend)
    ds = invent.datastore
    ds["a"] = 1
    assert ds.setdefault("a") == 1
    assert ds["a"] == 1


async def test_index_db_setdefault_no_key_with_default():
    """
    If the key doesn't exist, return the default value and set the key to the
    given default value.
    """
    await invent.start_datastore(_backend=IndexDBBackend)
    ds = invent.datastore
    assert ds.setdefault("a", True) is True
    assert "a" in ds
    assert ds["a"] is True


async def test_index_db_update():
    """
    Given an iterable of key/value pairs, insert them into the datastore.
    """
    to_insert = {"a": 1, "b": 2}
    await invent.start_datastore(_backend=IndexDBBackend)
    ds = invent.datastore
    ds.update(to_insert)
    assert len(ds) == 2
    assert ds["a"] == 1
    assert ds["b"] == 2


async def test_index_db_values():
    """
    Returns a list of the stored values.
    """
    await invent.start_datastore(_backend=IndexDBBackend)
    ds = invent.datastore
    ds["a"] = 1
    ds["b"] = 2
    assert sorted(ds.values()) == [1, 2]


async def test_index_db_len():
    """
    Builtin len works as expected.
    """
    await invent.start_datastore(_backend=IndexDBBackend)
    ds = invent.datastore
    assert len(ds) == 0
    ds["a"] = 1
    assert len(ds) == 1


async def test_index_db_get_set_del_item():
    """
    Getting, setting and deleting an item should work as expected.

    Setting and deleting should publish the expected messages on the
    "datastore" channel.
    """
    await invent.start_datastore(_backend=IndexDBBackend)
    ds = invent.datastore
    mock_publish = umock.Mock()
    with upytest.raises(KeyError):
        ds["a"]
    with umock.patch("invent.datastore:publish", mock_publish):
        # Store the value 1 against the key "a".
        ds["a"] = 1
        # Check a message has been published on storing a value.
        assert mock_publish.call_count == 1
        # Extract the message.
        call_args = mock_publish.call_args_list[0]
        msg = call_args[0][0]
        # It's the expected "store" message with the key/value pair that was
        # just stored.
        assert msg._subject == "a"
        assert msg.value == 1
        # The message was also published to the expected "datastore" channel.
        assert (
            call_args[1]["to_channel"]
            == invent.datastore.DATASTORE_SET_CHANNEL
        )
        # Reset mock.
        mock_publish.reset_mock()
        # Check the stored value is actually in the datastore.
        assert ds["a"] == 1
        # Delete the newly created value.
        del ds["a"]
        # Check a message has now been published on deleting a value.
        assert mock_publish.call_count == 1
        # Extract the message.
        call_args = mock_publish.call_args_list[0]
        msg = call_args[0][0]
        # It's the expected "store" message with the key pair that was just
        # stored.
        assert msg._subject == "a"
        # The message was also published to the expected "datastore" channel.
        assert (
            call_args[1]["to_channel"]
            == invent.datastore.DATASTORE_DELETE_CHANNEL
        )
    with upytest.raises(KeyError):
        # Deleting via a non-existent key raises a KeyError.
        del ds["a"]
