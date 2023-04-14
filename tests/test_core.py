import pypercard
import pytest
from js import document
from unittest import mock


def test_card_init():
    """
    Ensure the initial state is as expected.
    """
    name = "test_card"
    template = "<p>{value}</p>"
    c = pypercard.Card(name, template)
    assert c.name == name
    assert c.auto_advance is None
    assert c.transition is None
    assert c.background is None
    assert c.background_repeat is False
    assert c.template == template
    assert c.on_show is None
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


def test_card_init_with_on_show():
    """
    Ensure the user defined on_show function is set, as expected.
    """

    def my_on_show(app, card):
        pass

    name = "test_card"
    template = "<p>{foo}</p>"
    c = pypercard.Card(name, template, on_show=my_on_show)
    assert c.name == name
    assert c.template == template
    assert c.on_show == my_on_show
    assert c._transitions == []
    assert c.content is None
    assert c.app is None


def test_card_init_valid_auto_advance_args():
    """
    If auto_advance and transition arguments are correctly given, they
    are correctly stored in the card instance.

    The transition should be either a string or function that defines the
    name of the next card.
    """
    name = "test_card"
    template = "<p>{foo}</p>"
    # Test with a string transition containing the name of the next card.
    c = pypercard.Card(name, template, auto_advance=1, transition="foo")
    assert callable(c.transition)
    assert c.transition(c, {}) == "foo"
    assert isinstance(c.auto_advance, float)
    assert c.auto_advance == 1.0

    # Rebind with a callable transition.

    def test_transition(app, card):
        return "bar"

    c = pypercard.Card(
        name,
        template,
        auto_advance=1,
        transition=test_transition,
    )
    assert callable(c.transition)
    assert c.transition(c, {}) == "bar"


def test_card_init_missing_auto_advance_args():
    """
    Both auto_advance and transition should:

    * both be None, or
    * both exist.

    If one or the other is missing, the card should raise a ValueError.
    """
    name = "test_card"
    template = "<p>{foo}</p>"
    with pytest.raises(ValueError):
        pypercard.Card(name, template, auto_advance=1)
    with pytest.raises(ValueError):
        pypercard.Card(name, template, transition="foo")


def test_card_init_invalid_auto_advance_args():
    """
    A TypeError is raised if:

    * the `auto_advance` is not a float or int, or
    * the `transition` is not a string or function.
    """
    name = "test_card"
    template = "<p>{foo}</p>"
    with pytest.raises(TypeError):
        pypercard.Card(name, template, auto_advance=123, transition=123)
    with pytest.raises(TypeError):
        pypercard.Card(name, template, auto_advance="foo", transition="foo")


def test_card_init_background_args_color():
    """
    Arguments relating to the background and tiling are correctly handled.
    """
    name = "test_card"
    template = "<p>{foo}</p>"
    with mock.patch("pypercard.core.fetch") as mock_fetch:
        c = pypercard.Card(name, template, background="red")
        # No need to pre-fetch images.
        assert mock_fetch.call_count == 0
    assert c.background == "red"
    assert c.background_repeat is False


def test_card_init_background_args_image():
    """
    Arguments relating to the background and tiling are correctly handled.
    """
    name = "test_card"
    template = "<p>{foo}</p>"
    with mock.patch("pypercard.core.fetch") as mock_fetch:
        c = pypercard.Card(
            name,
            template,
            background="examples/turner/rain_steam_speed.jpg",
            background_repeat=True,
        )
        # Pre-fetch images.
        mock_fetch.assert_called_once_with(
            "examples/turner/rain_steam_speed.jpg"
        )
    assert c.background == "examples/turner/rain_steam_speed.jpg"
    assert c.background_repeat is True


def test_card_register_app():
    """
    Registering the parent app adds a reference to it in the card.
    """
    # Given
    name = "test_card"
    template = "<p>{value}</p>"
    # When
    c = pypercard.Card(name, template)
    # Then
    assert c.app is None
    mock_app = mock.MagicMock()
    c.register_app(mock_app)
    assert c.app == mock_app


def test_card_render():
    """
    Returns the expected and correctly rendered card as an HTML div element.
    """
    name = "test_card1"
    # Check this is called when the card is shown to the user.
    my_on_show = mock.MagicMock()
    # Ensure this value is inserted into the template.
    ds = pypercard.DataStore(foo="bar")
    # A simple template with a place to insert data, and an element to
    # dispatch an event.
    template = "<p id='id1'>{foo}</p><buton id='id2'>Click me</button>"
    # Make the card.
    c1 = pypercard.Card(name, template, on_show=my_on_show)
    # Make a next card.
    c2 = pypercard.Card("test_card2", "<p>test card 2</p>")
    app = pypercard.App(cards=[c1, c2], datastore=ds)
    # Register a transition to be attached to the element/event rendered in
    # the result.
    my_transition = mock.MagicMock(return_value="test_card2")

    @app.transition(name, "click", id="id2")
    def test_transition(app, card):
        return my_transition()

    # Render the card (on app start).
    app.start()

    # The on_show function was called with the expected objects.
    my_on_show.assert_called_once_with(app, c1)
    # The Python formatting into the template inserted the expected value from
    # the app.datastore.
    assert document.querySelector("#id1").innerText == "bar"
    # The button, when clicked, dispatches to the expected transition handler.
    button = document.querySelector("#id2")
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
    # Check this is called when the card is hidden from the user.
    my_on_hide = mock.MagicMock()
    c = pypercard.Card(name, template, on_hide=my_on_hide)
    app = pypercard.App(
        cards=[
            c,
        ],
        datastore=ds,
    )
    assert c.content is None
    app.start()  # will render the card
    assert c.content is not None
    c.hide()
    assert c.content.style.display == "none"

    # The on_show function was called with the expected objects.
    my_on_hide.assert_called_once_with(app, c)


def test_card_get_by_id():
    """
    If the card has been rendered, then the get_by_id function returns the
    element with the given id.
    """
    ds = pypercard.DataStore(foo="bar")
    name = "test_card"
    template = "<p id='id1'>{foo}</p>"
    c = pypercard.Card(name, template)
    app = pypercard.App(
        cards=[
            c,
        ],
        datastore=ds,
    )
    assert app.started is False
    # Not rendered, so return None.
    assert c.get_by_id("id1") is None
    # Now rendered, returns the expected element.
    c.show()
    el = c.get_by_id("id1")
    assert el.outerHTML == '<p id="id1">bar</p>'
    # Non-existent element returns None
    assert c.get_by_id("not-there") is None


def test_card_get_element():
    """
    If the card has been rendered, then the get_element function returns the
    referenced element.
    """
    ds = pypercard.DataStore(foo="bar")
    name = "test_card"
    template = "<p id='id1'>{foo}</p>"
    c = pypercard.Card(name, template)
    app = pypercard.App(
        cards=[
            c,
        ],
        datastore=ds,
    )
    assert app.started is False
    # Not rendered, so return None.
    assert c.get_element("#id1") is None
    # Now rendered, returns the expected element.
    c.show()
    el = c.get_element("#id1")
    assert el.outerHTML == '<p id="id1">bar</p>'
    # Non-existent element returns None
    assert c.get_element("#not-there") is None


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
    app = pypercard.App(
        cards=[
            c,
        ],
        datastore=ds,
    )
    assert app.started is False
    # Not rendered, so return an empty list.
    assert c.get_elements(".test") == []
    # Now rendered, returns the expected element.
    c.show()
    result = c.get_elements(".test")
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].outerHTML == '<p class="test">bar</p>'
    assert result[1].outerHTML == '<p class="test">Test</p>'
    # Non-existent element returns empty list.
    assert c.get_elements(".not-there") == []


def test_app_default_init():
    """
    Given default args, the app is set-up as expected.
    """
    test_name = "this is a test"
    document.querySelector("title").innerText = test_name
    app = pypercard.App()
    assert document.querySelector("title").innerText == app.name
    app_placeholder = document.querySelector("pyper-app")
    assert app_placeholder.parentNode == document.body
    # The empty app as picked up the card from the DOM.
    assert len(app.stack) == 1


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
        name="Custom name", datastore=ds, cards=card_list, sounds=sounds
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
    app.show_card(c)
    assert document.activeElement == c.get_by_id("test")
    app_placeholder = document.querySelector("pyper-app")
    assert app_placeholder.firstChild == c.content


def test_app_render_card_background_colour():
    """
    The given card is rendered with the given CSS background-color.
    """
    app = pypercard.App()
    c = pypercard.Card("test_card", "<h1>A test card</h1>", background="red")
    app.add_card(c)
    app.show_card(c)
    # Check the colour specification from the Card instance is reflected in
    # the DOM
    assert getattr(document.body.style, "background-color") == "red"
    # Reset
    app.set_background()
    assert getattr(document.body.style, "background-color") == ""


def test_app_render_card_background_image():
    """
    The given card is rendered with the given background image.
    """
    app = pypercard.App()
    c = pypercard.Card(
        "test_card",
        "<h1>A test card</h1>",
        background="examples/turner/rain_steam_speed.jpg",
    )
    app.add_card(c)
    app.show_card(c)
    # Check the background image specification from the Card instance is
    # reflected in the DOM
    assert (
        getattr(document.body.style, "background-image")
        == 'url("examples/turner/rain_steam_speed.jpg")'
    )
    assert getattr(document.body.style, "background-size") == "cover"
    assert getattr(document.body.style, "background-repeat") == "no-repeat"
    assert (
        getattr(document.body.style, "background-position") == "center center"
    )
    # Reset
    app.set_background()
    assert getattr(document.body.style, "background-image") == ""
    assert getattr(document.body.style, "background-image") == ""
    assert getattr(document.body.style, "background-size") == ""
    assert getattr(document.body.style, "background-repeat") == ""
    assert getattr(document.body.style, "background-position") == ""


def test_app_render_card_background_image_tiled():
    """
    The given card is rendered with the given background image in a tiled
    manner.
    """
    app = pypercard.App()
    c = pypercard.Card(
        "test_card",
        "<h1>A test card</h1>",
        background="examples/turner/rain_steam_speed.jpg",
        background_repeat=True,
    )
    app.add_card(c)
    app.show_card(c)
    # Check the background image specification from the Card instance is
    # reflected in the DOM
    assert (
        getattr(document.body.style, "background-image")
        == 'url("examples/turner/rain_steam_speed.jpg")'
    )
    assert getattr(document.body.style, "background-repeat") == "repeat"
    # Reset
    app.set_background()
    assert getattr(document.body.style, "background-image") == ""
    assert getattr(document.body.style, "background-repeat") == ""


def test_app_render_card_with_auto_advance():
    """
    The given card is rendered in the expected way. However, because it has
    valid auto_advance and transition values, JavaScript's setTimeout
    is called with the expected values (a function to call when the timeout
    occurs, and number of milliseconds to wait for the timeout to fire).
    """
    c1 = pypercard.Card(
        "test_card1",
        "<input id='test' type='text' autofocus/>",
        auto_advance=1.23,
        transition=lambda app, card: "test_card2",
    )
    c2 = pypercard.Card("test_card2", "<p>test card 2</p>")
    app = pypercard.App(cards=[c1, c2])

    def fake_timeout(fn, duration):
        fake_timeout.duration = duration
        fake_timeout.call_count += 1
        fn()

    fake_timeout.call_count = 0

    with mock.patch("pypercard.core.setTimeout", fake_timeout):
        app.start()
        assert fake_timeout.call_count == 1
        assert app.machine.state_name == "test_card2"
        # Translated from Python seconds, to JavaScript milliseconds.
        assert fake_timeout.duration == 1230


def test_app_add_card():
    """
    It's possible to add a card to the app's stack.
    """
    app = pypercard.App()
    app.stack = {}
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
        cards=[
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


def test_app_play_sound():
    """
    Ensure the Audio object for the named sound is retrieved, processed and
    played as expected. Rather difficult to test without the aid of ears...
    hence the use of mocking.
    """
    app = pypercard.App()
    app.add_sound("test_audio", "examples/loosey_goosey/honk.mp3")

    mock_audio = mock.MagicMock()
    mock_audio.currentTime = 1
    app.get_sound = mock.MagicMock(return_value=mock_audio)
    app.pause_sound = mock.MagicMock()

    app.play_sound("test", loop=True)

    # The loop flag has been set correctly.
    assert mock_audio.loop is True
    # Because the position of the sound was not at the start, it was reset via
    # the pause method.
    app.pause_sound.assert_called_once_with("test")
    # The JavaScript Audio object was play()-ed.
    mock_audio.play.assert_called_once_with()


def test_card_pause_sound():
    """
    Ensure the Audio object for the named sound is retrieved, and paused as
    expected. Rather difficult to test without the aid of ears... hence the use
    of mocking.
    """
    app = pypercard.App()
    app.add_sound("test_audio", "examples/loosey_goosey/honk.mp3")

    mock_audio = mock.MagicMock()
    mock_audio.currentTime = 1
    app.get_sound = mock.MagicMock(return_value=mock_audio)

    # Pause and retain place in the audio.
    app.pause_sound("test", keep_place=True)
    mock_audio.pause.assert_called_once_with()
    assert mock_audio.currentTime == 1
    mock_audio.pause.reset_mock()
    # Pause and reset back to the start of the audio (default behaviour).
    app.pause_sound("test")
    mock_audio.pause.assert_called_once_with()
    assert mock_audio.currentTime == 0


def test_set_background():
    """
    Ensure the CSS properties for the background are added to the body tag's
    style. Using the set_background method without arguments just resets
    everything.
    """
    app = pypercard.App()
    assert getattr(document.body.style, "background-color") == ""
    app.set_background("background-color: red;")
    assert getattr(document.body.style, "background-color") == "red"
    app.set_background()
    assert getattr(document.body.style, "background-color") == ""


def test_app_transition_decorator_missing_card():
    """
    A function decorated by @app.transition cannot be registered to a card
    that isn't in the stack.
    """
    app = pypercard.App()

    with pytest.raises(ValueError):

        @app.transition("foo", "click", id="bar")
        def test_trans(app, card):
            pass


def test_app_transition_on_element_id():
    """
    A function decorated by the @app.transition works correctly when the
    expected element/event happens on the element with the specified id.
    """
    tc1 = pypercard.Card("test_card1", "<button id='id1'>Click me</button>")
    tc2 = pypercard.Card("test_card2", "<p>Finished!</p>")
    app = pypercard.App(cards=[tc1, tc2])

    call_count = mock.MagicMock()

    @app.transition("test_card1", "click", id="id1")
    def my_transition(app, card):
        call_count()
        return "test_card2"

    app.start("test_card1")
    button = tc1.get_element("#id1")
    button.click()
    assert call_count.call_count == 1
    assert tc1.content.style.display == "none"
    assert tc2.content.innerHTML == "<p>Finished!</p>"


def test_app_transition_on_card():
    """
    A function decorated by the @app.transition works correctly when the
    expected event happens anywhere inside the card.
    """
    tc1 = pypercard.Card("test_card1", "<button id='id1'>Click me</button>")
    tc2 = pypercard.Card("test_card2", "<p>Finished!</p>")
    app = pypercard.App(cards=[tc1, tc2])

    call_count = mock.MagicMock()

    @app.transition("test_card1", "click")
    def my_transition(app, card):
        call_count()
        return "test_card2"

    app.start("test_card1")
    button = tc1.get_element("#id1")
    button.click()
    assert call_count.call_count == 1
    assert tc1.content.style.display == "none"
    assert tc2.content.innerHTML == "<p>Finished!</p>"


def test_app_start():
    """
    Assuming the app is configured correctly, calling start with a reference
    to the first card to display, results in the card rendered to the DOM.
    """
    tc1 = pypercard.Card("test_card1", "<button id='id1'>Click me</button>")
    tc2 = pypercard.Card("test_card2", "<p>Finished!</p>")
    app = pypercard.App(cards=[tc1, tc2])

    mock_work = mock.MagicMock()

    @app.transition(tc1, "click", id="id1")
    def my_transition(app, card):
        mock_work(app, card)
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
