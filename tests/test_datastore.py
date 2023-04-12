import pypercard
import pytest
from js import localStorage


def test_datastore_default_init():
    """
    localStorage is used.
    """
    ds = pypercard.DataStore()
    assert ds.store == localStorage


def test_datastore_init_with_values():
    """
    If the persist flag on __init__ is True, sessionStorage is used.
    """
    ds = pypercard.DataStore(foo="bar", baz="qux")
    assert ds["foo"] == "bar"
    assert ds["baz"] == "qux"
    assert len(ds) == 2


def test_datastore_clear():
    """
    The clear method empties the datastore.
    """
    ds = pypercard.DataStore()
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
    ds = pypercard.DataStore()
    ds["a"] = 1
    ds["b"] = 2
    copy_ds = ds.copy()
    assert copy_ds == {"a": 1, "b": 2}
    assert copy_ds is not ds


def test_datastore_get_with_value():
    """
    The get method returns the expected value, if the key exists.
    """
    ds = pypercard.DataStore()
    ds["a"] = 1
    assert ds.get("a") == 1


def test_datastore_get_missing_key_no_default():
    """
    The get method returns None by default, if the key doesn't exist.
    """
    ds = pypercard.DataStore()
    assert ds.get("a") is None


def test_datastore_get_missing_key_with_default():
    """
    The get method returns the given default value, if the key doesn't exist.
    """
    ds = pypercard.DataStore()
    assert ds.get("a", "foo") == "foo"


def test_datastore_items():
    """
    The items method makes it possible to lazily iterate over the items
    contained within the datastore.
    """
    ds = pypercard.DataStore()
    ds["a"] = 1
    ds["b"] = 2
    iterator = ds.items()
    from collections.abc import Iterable

    assert isinstance(iterator, Iterable)
    for k, v in iterator:
        assert k in ds
        assert ds[k] == v


def test_datastore_keys():
    """
    The keys method returns a list of keys contained in the datastore.
    """
    ds = pypercard.DataStore()
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
    ds = pypercard.DataStore()
    ds["a"] = 1
    ds["b"] = 2
    val = ds.pop("a")
    assert val == 1
    assert "a" not in ds


def test_datastore_pop_no_key():
    """
    Popping a non-existent item returns None by default.
    """
    ds = pypercard.DataStore()
    assert ds.pop("foo") is None


def test_datastore_pop_no_key_with_default():
    """
    Popping a non-existent item returns the given default value.
    """
    ds = pypercard.DataStore()
    assert ds.pop("foo", True) is True


def test_datastore_popitem():
    """
    NotImplemented
    """
    ds = pypercard.DataStore()
    with pytest.raises(NotImplementedError):
        ds.popitem()


def test_datastore_setdefault_no_key():
    """
    If the key doesn't exist, by default returns None and sets key to an
    associated value of None.
    """
    ds = pypercard.DataStore()
    assert ds.setdefault("a") is None
    assert "a" in ds
    assert ds["a"] is None


def test_datastore_setdefault_has_key():
    """
    If the key exists, just return the associated value and do NOT update the
    value.
    """
    ds = pypercard.DataStore()
    ds["a"] = 1
    assert ds.setdefault("a") == 1
    assert ds["a"] == 1


def test_datastore_setdefault_no_key_with_default():
    """
    If the key doesn't exist, return the default value and set the key to the
    given default value.
    """
    ds = pypercard.DataStore()
    assert ds.setdefault("a", True) is True
    assert "a" in ds
    assert ds["a"] is True


def test_datastore_update():
    """
    Given an iterable of key/value pairs, insert them into the datastore.
    """
    to_insert = (("a", 1), ("b", 2))
    ds = pypercard.DataStore()
    ds.update(to_insert)
    assert len(ds) == 2
    assert ds["a"] == 1
    assert ds["b"] == 2


def test_datastore_values():
    """
    Returns a list of the stored values.
    """
    ds = pypercard.DataStore()
    ds["a"] = 1
    ds["b"] = 2
    assert sorted(ds.values()) == [1, 2]


def test_datastore_len():
    """
    Builtin len works as expected.
    """
    ds = pypercard.DataStore()
    assert len(ds) == 0
    ds["a"] = 1
    assert len(ds) == 1


def test_datastore_get_set_del_item():
    """
    Getting an item should work as expected.
    """
    ds = pypercard.DataStore()
    with pytest.raises(KeyError):
        ds["a"]
    ds["a"] = 1
    assert ds["a"] == 1
    del ds["a"]
    with pytest.raises(KeyError):
        del ds["a"]


def test_datastore_iter():
    """
    It's possible to iterate over the keys in a datastore.
    """
    ds = pypercard.DataStore()
    ds["a"] = 1
    ds["b"] = 2
    for key in ds:
        assert key in ds


def test_datastore_contains():
    """
    It's possible to check if a key is in the datastore.
    """
    ds = pypercard.DataStore()
    ds["a"] = 1
    assert "a" in ds
