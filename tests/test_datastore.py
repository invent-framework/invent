import invent
import pytest
from unittest import mock


@pytest.mark.skip
def test_datastore_get_set_del_item():
    """
    Getting, setting and deleting an item should work as expected.

    Setting and deleting should publish the expected messages on the
    "datastore" channel.
    """
    ds = invent.DataStore()
    mock_publish = mock.MagicMock()
    with pytest.raises(KeyError):
        ds["a"]
    with mock.patch("invent.datastore.publish", mock_publish):
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
        assert call_args[1]["to_channel"] == "store-data"
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
        assert call_args[1]["to_channel"] == "delete-data"
    with pytest.raises(KeyError):
        # Deleting via a non-existent key raises a KeyError.
        del ds["a"]
