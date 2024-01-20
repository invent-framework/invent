import invent
import json
from unittest import mock
from pyscript import window


def test_state_after_import():
    """
    The invent.i18n.__language defaults to window.navigator.language

    There's nothing in __translations.
    """
    assert invent.i18n.__language == window.navigator.language
    assert invent.i18n.__translations == {}


def test_load_from_default_location():
    """
    The load method uses the translations.json file in the home directory by
    default.
    """
    with open("./translations.json", "r") as tr:
        expected = json.load(tr)
    invent.i18n.load()
    assert invent.i18n.__translations == expected


def test_load_from_given_location():
    """
    The load method will use the referenced file for translations.
    """
    path = "translations.json"
    with open(path, "r") as tr:
        expected = json.load(tr)
    invent.i18n.load(path)
    assert invent.i18n.__translations == expected


def test_load_from_bad_location_is_logged_to_console():
    """
    If the translations can't be loaded, this is logged for debugging purposes
    with the message from the Python exception.
    """
    with mock.patch("invent.i18n.window.console.error") as mock_error:
        invent.i18n.load("no-such-file.json")
        assert mock_error.called_once()


def test_set_language():
    """
    Set language updates the default language and publishes the expected
    set_language message to the i18n channel.
    """
    current_lang = invent.i18n.__language
    with mock.patch("invent.i18n.publish") as mock_publish:
        invent.i18n.set_language("foo")
        assert invent.i18n.__language == "foo"
        assert invent.i18n.get_language() == "foo"
        msg = mock_publish.call_args_list[0][0][0]
        assert msg._type == "set_language"
        assert msg.to_language == "foo"
        assert mock_publish.call_args_list[0][1]["to_channel"] == "i18n"
    invent.i18n.set_language(current_lang)


def test_get_language():
    """
    Simply returns the current default language.
    """
    assert invent.i18n.get_language() == window.navigator.language
    invent.i18n.set_language("foo")
    assert invent.i18n.get_language() == "foo"


def test_():
    """
    Ensure the _ utility function for translating strings on the fly works
    as expected.
    """
    # Store this to reset at the end.
    current_lang = invent.i18n.get_language()
    # Clean state of no translations.
    invent.i18n.__translations = {}
    # No translations, so just return the string.
    assert "hello" == invent._("hello")
    # Load translations.
    invent.i18n.load()
    # No translation for the default language (en).
    invent.i18n.set_language("en")
    # So just return the string.
    assert "hello" == invent._("hello")
    # Pass in a language code, return the expected translation.
    assert "bonjour" == invent._("hello", "fr-FR")
    # Set the default language to one that is supported.
    invent.i18n.set_language("de")
    # Return the expected translation given the supported default language.
    assert "guten tag" == invent._("hello")
    # Reset and clean up the default language to the user's default.
    invent.i18n.set_language(current_lang)
