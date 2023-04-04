import pypercard
import pytest
from pyodide import ffi
from js import document, localStorage
from unittest import mock


@pytest.fixture(autouse=True)
def before_tests():
    """
    Ensure browser storage is always reset to empty. Remove the app
    placeholder. Reset the page title.
    """
    localStorage.clear()
    app_placeholder = document.querySelector("pyper-app")
    if app_placeholder:
        app_placeholder.remove()
    document.querySelector("title").innerText = "PyperCard PyTest Suite"


def test_datastore_default_init():
    """
    localStorage is used.
    """
    ds = pypercard.DataStore()
    assert ds.store == pypercard.localStorage


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


def test_card_init():
    """
    Ensure the initial state is as expected.
    """
    name = "test_card"
    template = "<p>{value}</p>"
    c = pypercard.Card(name, template)
    assert c.name == name
    assert c.auto_advance is None
    assert c.auto_advance_after is None
    assert c.template == template
    assert c.on_render is None
    assert c._transitions == []
    assert c.content is None
    assert c.app is None


def test_card_init_element_template():
    """
    If there is no template given, the template is populated from the innerHTML
    of the template element in the dom with the id of the name of the card.
    """
    c = pypercard.Card("test_card_with_element_template")
    assert c.template.strip() == "<p>This is a test. {foo}</p>"


def test_card_init_no_template():
    """
    If no template is given, and there's no matching template element in the
    DOM, then a RuntimeError happens.
    """
    with pytest.raises(RuntimeError):
        pypercard.Card("does_not_exist_in_the_dom")


def test_card_init_with_on_render():
    """
    Ensure the user defined on_render function is set, as expected.
    """

    def my_on_render(card, datastore):
        pass

    name = "test_card"
    template = "<p>{foo}</p>"
    c = pypercard.Card(name, template, on_render=my_on_render)
    assert c.name == name
    assert c.template == template
    assert c.on_render == my_on_render
    assert c._transitions == []
    assert c.content is None
    assert c.app is None


def test_card_init_valid_auto_advance_args():
    """
    If auto_advance and auto_advance_after arguments are correctly given, they
    are correctly stored in the card instance.

    The auto_advance should be either a string or function that defines the
    name of the next card.
    """
    name = "test_card"
    template = "<p>{foo}</p>"
    # Test with a string auto_advance containing the name of the next card.
    c = pypercard.Card(
        name, template, auto_advance="foo", auto_advance_after=1
    )
    assert callable(c.auto_advance)
    assert c.auto_advance(c, {}) == "foo"
    assert isinstance(c.auto_advance_after, float)
    assert c.auto_advance_after == 1.0
    # Rebind with a callable auto_advance.

    def test_advance_transition(card, datastore):
        return "bar"

    c = pypercard.Card(
        name,
        template,
        auto_advance=test_advance_transition,
        auto_advance_after=1,
    )
    assert callable(c.auto_advance)
    assert c.auto_advance(c, {}) == "bar"


def test_card_init_missing_auto_advance_args():
    """
    Both auto_advance and auto_advance_after should:

    * both be None, or
    * both exist.

    If one or the other is missing, the card should raise a ValueError.
    """
    name = "test_card"
    template = "<p>{foo}</p>"
    with pytest.raises(ValueError):
        pypercard.Card(name, template, auto_advance="foo")
    with pytest.raises(ValueError):
        pypercard.Card(name, template, auto_advance_after=1.2)


def test_card_init_invalid_auto_advance_args():
    """
    A TypeError is raised if:

    * the `auto_advance` is not a string or function, or
    * the `auto_advance_after` is not a float or int.
    """
    name = "test_card"
    template = "<p>{foo}</p>"
    with pytest.raises(TypeError):
        pypercard.Card(
            name, template, auto_advance=123, auto_advance_after=123
        )
    with pytest.raises(TypeError):
        pypercard.Card(
            name, template, auto_advance="foo", auto_advance_after="foo"
        )


def test_card_register_app():
    """
    Registering the parent app adds a reference to it in the card.
    """
    name = "test_card"
    template = "<p>{value}</p>"
    c = pypercard.Card(name, template)
    assert c.app is None
    mock_app = mock.MagicMock()
    c.register_app(mock_app)
    assert c.app == mock_app


def test_card_render():
    """
    Returns the expected and correctly rendered card as an HTML div element.
    """
    name = "test_card"
    # Check this is called when rendering.
    my_on_render = mock.MagicMock()
    # Ensure this value is inserted into the template.
    ds = pypercard.DataStore(foo="bar")
    # A simple template with a place to insert data, and an element to
    # dispatch an event.
    template = "<p id='id1'>{foo}</p><buton id='id2'>Click me</button>"
    # Make the card.
    c = pypercard.Card(name, template, my_on_render)
    # Register a transition to be attached to the element/event rendered in
    # the result.
    my_transition = mock.MagicMock(return_value="baz")
    c.register_transition("id2", "click", my_transition)

    # RENDER!
    result = c.render(ds)

    # The on_render function was called with the expected objects.
    my_on_render.assert_called_once_with(c, ds)
    # The Python formatting into the template inserted the expected value from
    # the datastore.
    assert result.querySelector("#id1").innerText == "bar"
    # The button, when clicked, dispatches to the expected transition handler.
    button = result.querySelector("#id2")
    assert my_transition.call_count == 0
    button.click()
    assert my_transition.call_count == 1


def test_card_hide():
    """
    The card's content is reset to None after it was created while
    rendering.
    """
    ds = pypercard.DataStore(foo="bar")
    name = "test_card"
    template = "<p id='id1'>{foo}</p><buton id='id2'>Click me</button>"
    c = pypercard.Card(name, template)
    assert c.content is None
    c.render(ds)
    assert c.content is not None
    c.hide()
    assert c.content is None


def test_card_register_transition():
    """
    Ensure the passed in transition is dealt stored, in readiness to be
    applied later when the card is rendered.
    """
    name = "test_card"
    template = "<p id='id1'>{foo}</p><buton id='id2'>Click me</button>"
    c = pypercard.Card(name, template)

    def my_transition(card, ds):
        return "another_card_name"

    c.register_transition("id2", "click", my_transition)
    assert len(c._transitions) == 1
    assert c._transitions[0]["selector"] == "#id2"
    assert c._transitions[0]["event_name"] == "click"
    # The my_transition function has been converted to a JsProxy object.
    assert isinstance(c._transitions[0]["handler"], ffi.JsProxy)


def test_card_get_by_id():
    """
    If the card has been rendered, then the get_by_id function returns the
    element with the given id.
    """
    ds = pypercard.DataStore(foo="bar")
    name = "test_card"
    template = "<p id='id1'>{foo}</p>"
    c = pypercard.Card(name, template)
    # Not rendered, so return None.
    assert c.get_by_id("id1") is None
    # Now rendered, returns the expected element.
    c.render(ds)
    el = c.get_by_id("id1")
    assert el.outerHTML == '<p id="id1">bar</p>'
    # Non-existent element returns None
    assert c.get_by_id("not-there") is None
    # Hide the card, the element no longer exists.
    c.hide()
    assert c.get_by_id("id1") is None


def test_card_get_element():
    """
    If the card has been rendered, then the get_element function returns the
    referenced element.
    """
    ds = pypercard.DataStore(foo="bar")
    name = "test_card"
    template = "<p id='id1'>{foo}</p>"
    c = pypercard.Card(name, template)

    # Not rendered, so return None.
    assert c.get_element("#id1") is None
    # Now rendered, returns the expected element.
    c.render(ds)
    el = c.get_element("#id1")
    assert el.outerHTML == '<p id="id1">bar</p>'
    # Non-existent element returns None
    assert c.get_element("#not-there") is None
    # Hide the card, the element no longer exists.
    c.hide()
    assert c.get_element("#id1") is None


def test_card_get_elements():
    """
    If the card has been rendered, then the get_elements function returns the
    elements that match the given selector. If no elements match, an empty list
    is returned.
    """
    ds = pypercard.DataStore(foo="bar")
    name = "test_card"
    template = "<p class='test'>{foo}</p><p class='test'>Test</p>"
    c = pypercard.Card(name, template)

    # Not rendered, so return an empty list.
    assert c.get_elements(".test") == []
    # Now rendered, returns the expected element.
    c.render(ds)
    result = c.get_elements(".test")
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].outerHTML == '<p class="test">bar</p>'
    assert result[1].outerHTML == '<p class="test">Test</p>'
    # Non-existent element returns empty list.
    assert c.get_elements(".not-there") == []
    # Hide the card, the elements no longer exist.
    c.hide()
    assert c.get_elements(".test") == []


def test_card_play_sound():
    """
    Ensure the Audio object for the named sound is retrieved, processed and
    played as expected. Rather difficult to test without the aid of ears...
    hence the use of mocking.
    """
    name = "test_card"
    template = "<p class='test'>{foo}</p><p class='test'>Test</p>"
    c = pypercard.Card(name, template)

    mock_app = mock.MagicMock()
    mock_audio = mock.MagicMock()
    mock_audio.currentTime = 1
    mock_app.get_sound.return_value = mock_audio
    c.register_app(mock_app)
    c.pause_sound = mock.MagicMock()

    c.play_sound("test", loop=True)

    # The loop flag has been set correctly.
    assert mock_audio.loop is True
    # Because the position of the sound was not at the start, it was reset via
    # the pause method.
    c.pause_sound.assert_called_once_with("test")
    # The JavaScript Audio object was play()-ed.
    mock_audio.play.assert_called_once_with()


def test_card_pause_sound():
    """
    Ensure the Audio object for the named sound is retrieved, and paused as
    expected. Rather difficult to test without the aid of ears... hence the use
    of mocking.
    """
    name = "test_card"
    template = "<p class='test'>{foo}</p><p class='test'>Test</p>"
    c = pypercard.Card(name, template)

    mock_app = mock.MagicMock()
    mock_audio = mock.MagicMock()
    mock_audio.currentTime = 1
    mock_app.get_sound.return_value = mock_audio
    c.register_app(mock_app)

    # Pause and retain place in the audio.
    c.pause_sound("test", keep_place=True)
    mock_audio.pause.assert_called_once_with()
    assert mock_audio.currentTime == 1
    mock_audio.pause.reset_mock()
    # Pause and reset back to the start of the audio (default behaviour).
    c.pause_sound("test")
    mock_audio.pause.assert_called_once_with()
    assert mock_audio.currentTime == 0


def test_app_default_init():
    """
    Given default args, the app is set-up as expected.
    """
    app = pypercard.App()
    assert document.querySelector("title").innerText == app.name
    app_placeholder = document.querySelector("pyper-app")
    assert app_placeholder.parentNode == document.body


def test_app_custom_init():
    """
    Given customisations, the app is set-up as expected.
    """
    ds = pypercard.DataStore(foo="bar")
    card = pypercard.Card("test_card", "<p>Hello</p>")
    assert card.app is None
    card_list = [
        card,
    ]
    sounds = {
        "test_audio": "examples/loosey_goosey/honk.mp3",
    }
    app = pypercard.App(
        name="Custom name", datastore=ds, card_list=card_list, sounds=sounds
    )
    assert app.name == "Custom name"
    assert app.datastore == ds
    assert "test_card" in app.stack
    assert len(app.stack) == 1
    assert app.stack["test_card"] == card
    assert card.app == app
    assert "test_audio" in app.sounds
    assert len(app.sounds) == 1
    assert document.querySelector("title").innerText == app.name


def test_app_resolve_card_as_string():
    """
    Given a string containing a card name, will raise a ValueError if the card
    is not in the app's stack. Otherwise, will return the card instance.
    """
    app = pypercard.App()
    with pytest.raises(ValueError):
        app._resolve_card("test_card")
    c = pypercard.Card("test_card", "<p>Hello</p>")
    app.add_card(c)
    assert app._resolve_card("test_card") == c


def test_app_resolve_card_as_card_instance():
    """
    Given a card instance, will raise a ValueError if the card is not in the
    app's stack. Otherwise, returns the card instance.
    """
    app = pypercard.App()
    c = pypercard.Card("test_card", "<p>Hello</p>")
    with pytest.raises(ValueError):
        app._resolve_card(c)
    app.add_card(c)
    assert app._resolve_card(c) == c


def test_app_resolve_card_wrong_type():
    """
    If the card reference isn't a string or Card, raise a ValueError.
    """
    app = pypercard.App()
    c = pypercard.Card("test_card", "<p>Hello</p>")
    app.add_card(c)
    with pytest.raises(ValueError):
        app._resolve_card(1234567)


def test_app_render_card():
    """
    The given card is rendered in the expected way. For example, autofocus is
    respected.
    """
    app = pypercard.App()
    c = pypercard.Card("test_card", "<input id='test' type='text' autofocus/>")
    app.add_card(c)
    app.render_card(c)
    assert document.activeElement == c.get_by_id("test")
    app_placeholder = document.querySelector("pyper-app")
    assert app_placeholder.firstChild == c.content


def test_app_render_card_with_auto_advance():
    """
    The given card is rendered in the expected way. However, because it has
    valid auto_advance and auto_advance_after values, JavaScript's setTimeout
    is called with the expected values (a function to call when the timeout
    occurs, and number of milliseconds to wait for the timeout to fire).

    When called, the function to call when the timeout occurs behaves as
    expected: if the card is still rendered, call the auto_advance function,
    otherwise don't do anything.
    """
    app = pypercard.App()
    c = pypercard.Card(
        "test_card",
        "<input id='test' type='text' autofocus/>",
        auto_advance=mock.MagicMock(return_value="foo"),
        auto_advance_after=1.23,
    )
    app.add_card(c)
    with mock.patch("pypercard.setTimeout") as mock_timeout:
        app.render_card(c)
        assert mock_timeout.call_count == 1
        timeout_function = mock_timeout.call_args_list[0][0][0]
        timeout_duration = mock_timeout.call_args_list[0][0][1]
        app._resolve_card = mock.MagicMock()
        app.render_card = mock.MagicMock()
        # With no content (the card isn't visible), nothing happens.
        c.content = None
        timeout_function()
        assert app._resolve_card.call_count == 0
        assert app.render_card.call_count == 0
        # But with content (the card is visible), the expected transition takes
        # place.
        c.content = "dummy content"
        timeout_function()
        app._resolve_card.assert_called_once_with("foo")
        assert app.render_card.call_count == 1
        # Translated from Python seconds, to JavaScript milliseconds.
        assert timeout_duration == 1230


def test_app_add_card():
    """
    It's possible to add a card to the app's stack.
    """
    app = pypercard.App()
    assert len(app.stack) == 0
    c = pypercard.Card("test_card", "<p>Hello</p>")
    app.add_card(c)
    assert len(app.stack) == 1
    assert app.stack["test_card"] == c
    assert c.app == app


def test_app_add_card_duplicate():
    """
    Adding a card with a name that already exists, causes a ValueError.
    """
    app = pypercard.App()
    c = pypercard.Card("test_card", "<p>Hello</p>")
    app.add_card(c)
    with pytest.raises(ValueError):
        app.add_card(c)


def test_app_remove_card():
    """
    The named card is removed from the stack.
    """
    c = pypercard.Card("test_card", "<p>Hello</p>")
    app = pypercard.App(
        card_list=[
            c,
        ]
    )
    assert "test_card" in app.stack
    app.remove_card(c)
    assert "test_card" not in app.stack
    assert len(app.stack) == 0


def test_app_add_sound():
    """
    Ensure the expected Audio instance is added to the available audio clips
    for the application.
    """
    app = pypercard.App()
    assert app.sounds == {}
    app.add_sound("test_audio", "examples/loosey_goosey/honk.mp3")
    assert "test_audio" in app.sounds
    assert len(app.sounds) == 1
    assert app.sounds["test_audio"].src.endswith(
        "examples/loosey_goosey/honk.mp3"
    )


def test_app_get_sound():
    """
    The get_sound method returns the expected Audio instance pointing at the
    correct src. If the passed in name does not reference an audio object, a
    ValueError is raised.
    """
    app = pypercard.App()
    app.add_sound("test_audio", "examples/loosey_goosey/honk.mp3")
    audio = app.get_sound("test_audio")
    assert audio.src.endswith("examples/loosey_goosey/honk.mp3")
    with pytest.raises(ValueError):
        app.get_sound("foo")


def test_app_remove_sound():
    """
    Ensure the referenced sound is removed from the available sounds for the
    app.
    """
    app = pypercard.App()
    app.add_sound("test_audio", "examples/loosey_goosey/honk.mp3")
    assert "test_audio" in app.sounds
    app.remove_sound("test_audio")
    assert "test_audio" not in app.sounds


def test_app_transition_decorator_missing_card():
    """
    A function decorated by @app.transition cannot be registered to a card
    that isn't in the stack.
    """
    app = pypercard.App()

    with pytest.raises(ValueError):

        @app.transition("foo", "bar", "click")
        def test_trans(card, datastore):
            pass


def test_app_transition():
    """
    A function decorated by the @app.transition works correctly when the
    expected element/event happens
    """
    tc1 = pypercard.Card("test_card1", "<button id='id1'>Click me</button>")
    tc2 = pypercard.Card("test_card2", "<p>Finished!</p>")
    app = pypercard.App(card_list=[tc1, tc2])

    mock_work = mock.MagicMock()

    @app.transition(tc1, "id1", "click")
    def my_transition(card, datastore):
        mock_work(card, datastore)
        return "test_card2"

    app.start("test_card1")
    tc1.get_element("#id1").click()
    mock_work.assert_called_once_with(tc1, app.datastore)
    assert tc1.content is None
    assert tc2.content.innerHTML == "<p>Finished!</p>"


def test_app_start():
    """
    Assuming the app is configured correctly, calling start with a reference
    to the first card to display, results in the card rendered to the DOM.
    """
    tc1 = pypercard.Card("test_card1", "<button id='id1'>Click me</button>")
    tc2 = pypercard.Card("test_card2", "<p>Finished!</p>")
    app = pypercard.App(card_list=[tc1, tc2])

    mock_work = mock.MagicMock()

    @app.transition(tc1, "id1", "click")
    def my_transition(card, datastore):
        mock_work(card, datastore)
        return "test_card2"

    app.start("test_card1")

    app_placeholder = document.querySelector("pyper-app")
    assert app_placeholder.firstChild == tc1.content


def test_app_start_already_started():
    """
    If the app is already started, calling start will result in a
    RuntimeError.
    """
    app = pypercard.App()
    app.started = True
    with pytest.raises(RuntimeError):
        app.start("foo")
