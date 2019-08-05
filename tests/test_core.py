"""
Tests for the core functionality of the PyperCard project.
"""
import os
import pytest
from unittest import mock
from pypercard.core import Card, CardApp, Inputs, palette
from kivy.uix.screenmanager import Screen, ScreenManager


def test_palette_colour_name():
    """
    If given a known colour name (e.g. "red"), return a tuple representing
    the Kivy colour.
    """
    result = palette("red")
    assert isinstance(result, tuple)


def test_palette_colour_name_capitalised():
    """
    If given a colour name (e.g. "RED"), return a tuple representing
    the Kivy colour.
    """
    result = palette("RED")
    assert isinstance(result, tuple)


def test_palette_raw_hex():
    """
    If given a raw hex value as a string (e.g. "0xFFCC99"), return a tuple
    representing a Kivy colour.
    """
    result = palette("0xFFFFFF")
    assert result == (1.0, 1.0, 1.0)


def test_palette_html_hex():
    """
    If given an HTML hex value as a string (e.g. "#FFCC99"), return a tuple
    representing a Kivy colour.
    """
    result = palette("#FFFFFF")
    assert result == (1.0, 1.0, 1.0)


def test_palette_no_such_colour():
    """
    If given an unknown colour or value that can't be converted from HEX then
    raise a ValueError.
    """
    with pytest.raises(ValueError):
        palette("foobarbaz")


def test_card_init():
    """
    Ensure that the arguments passed into the __init__ are properly "processed"
    and assigned to the instance attributes.
    """
    with mock.patch("pypercard.core.Card._verify") as mock_verify:
        title = "the card's unique title"
        text = "this is some textual content for the card."
        text_color = None  # Should default to white.
        text_size = 32
        form = Inputs.MULTICHOICE
        options = ("foo", "bar", "baz")
        sound = "boop.wav"
        sound_repeat = True
        background = "blue"
        buttons = [{"label": "Button1", "target": "Another Card"}]
        auto_advance = 1.234
        auto_target = "Another Card"
        card = Card(
            title=title,
            text=text,
            text_color=text_color,
            text_size=text_size,
            form=form,
            options=options,
            sound=sound,
            sound_repeat=sound_repeat,
            background=background,
            buttons=buttons,
            auto_advance=auto_advance,
            auto_target=auto_target,
        )
        assert card.title == title
        assert card.text == text
        assert card.text_color == (1.0, 1.0, 1.0, 1.0)  # defaults to white.
        assert card.text_size == text_size
        assert card.form == form
        assert card.options == options
        assert card.sound == sound
        assert card.sound_repeat == sound_repeat
        assert card.background == (0.0, 0.0, 1.0, 1.0)  # use colour from name.
        assert card.buttons == buttons
        assert card.auto_advance == auto_advance
        assert card.auto_target == auto_target
        mock_verify.assert_called_once_with()


def test_card_init_text_colour_background_path_no_buttons():
    """
    If the background argument is not a colour, then retain it as it should be
    a path to an image file.
    """
    with mock.patch("pypercard.core.Card._verify") as mock_verify:
        title = "the card's unique title"
        text = "this is some textual content for the card."
        text_color = "red"
        text_size = 32
        form = Inputs.MULTICHOICE
        options = ("foo", "bar", "baz")
        sound = "boop.wav"
        sound_repeat = True
        background = "filename.bmp"
        buttons = None
        auto_advance = 1.234
        auto_target = "Another Card"
        card = Card(
            title=title,
            text=text,
            text_color=text_color,
            text_size=text_size,
            form=form,
            options=options,
            sound=sound,
            sound_repeat=sound_repeat,
            background=background,
            buttons=buttons,
            auto_advance=auto_advance,
            auto_target=auto_target,
        )
        assert card.title == title
        assert card.text == text
        assert card.text_color == (1.0, 0.0, 0.0, 1.0)  # now a Kivy colour.
        assert card.text_size == text_size
        assert card.form == form
        assert card.options == options
        assert card.sound == sound
        assert card.sound_repeat == sound_repeat
        assert card.background == "filename.bmp"  # remains a file path.
        assert card.buttons == []  # an empty list of buttons.
        assert card.auto_advance == auto_advance
        assert card.auto_target == auto_target
        mock_verify.assert_called_once_with()


def test_card_verify_form_no_text():
    """
    If there is a form, there must also be text (to act as the form's label /
    instructions).
    """
    title = "title"
    form = Inputs.TEXTBOX
    with pytest.raises(ValueError):
        Card(title=title, form=form)
    # Check the good case.
    Card(title=title, form=form, text="Label for the form.")


def test_card_verify_multichoice_options():
    """
    If the form is a multi-choice picker, there must be a list of options to
    select.
    """
    title = "title"
    text = "Instructions for the form."
    form = Inputs.MULTICHOICE
    with pytest.raises(ValueError):
        Card(title=title, text=text, form=form)


def test_card_verify_multichoice_options_not_strings():
    """
    If the form is a multi-choice picker, the available options MUST be
    strings.
    """
    title = "title"
    text = "Instructions for the form."
    form = Inputs.MULTICHOICE
    options = ("foo", "bar", 123)
    with pytest.raises(ValueError):
        Card(title=title, text=text, form=form, options=options)
    # Check the good case.
    options = ("foo", "bar", "baz")
    Card(title=title, text=text, form=form, options=options)


def test_card_verify_select_options():
    """
    If the form is a single item selector, there must be a list of options
    from which to choose an item.
    """
    title = "title"
    text = "Instructions for the form."
    form = Inputs.SELECT
    with pytest.raises(ValueError):
        Card(title=title, text=text, form=form)


def test_card_verify_select_options_not_strings():
    """
    If the form is a single item selector, the available options MUST be
    strings.
    """
    title = "title"
    text = "Instructions for the form."
    form = Inputs.SELECT
    options = ("foo", "bar", 123)
    with pytest.raises(ValueError):
        Card(title=title, text=text, form=form, options=options)
    # Check the good case.
    options = ("foo", "bar", "baz")
    Card(title=title, text=text, form=form, options=options)


def test_card_verify_slider_options():
    """
    If the form is a slider, there must be an options list containing the
    min, max and (optional) step values.
    """
    title = "title"
    text = "Instructions for the form."
    form = Inputs.SLIDER
    with pytest.raises(ValueError):
        Card(title=title, text=text, form=form)


def test_card_verify_slider_options_size():
    """
    If the form is a slider, the options must contain the correct number of
    items (at least two, no more than three).
    """
    title = "title"
    text = "Instructions for the form."
    form = Inputs.SLIDER
    options = (1,)
    with pytest.raises(ValueError):
        Card(title=title, text=text, form=form, options=options)
    options = (1, 2, 3, 4)
    with pytest.raises(ValueError):
        Card(title=title, text=text, form=form, options=options)
    # Check the good case.
    options = (1, 100, 10)
    Card(title=title, text=text, form=form, options=options)


def test_card_verify_slider_options_numeric():
    """
    If the form is a slider, the options must contain values that are numeric.
    """
    title = "title"
    text = "Instructions for the form."
    form = Inputs.SLIDER
    options = (1, 100, "hello")
    with pytest.raises(ValueError):
        Card(title=title, text=text, form=form, options=options)
    options = (0.1, 0.9, "hello")
    with pytest.raises(ValueError):
        Card(title=title, text=text, form=form, options=options)
    # Check the good case.
    options = (0.1, 1)
    Card(title=title, text=text, form=form, options=options)


def test_card_verify_buttons_not_dict():
    """
    The definitions of buttons must be expressed as dictionaries.
    """
    title = "title"
    buttons = ["not a dictionary"]
    with pytest.raises(ValueError):
        Card(title=title, buttons=buttons)


def test_card_verify_buttons_missing_attributes():
    """
    Each dictinary definition of a button MUST contain a label and target
    attribute.
    """
    title = "title"
    buttons = [{"label": "Hello"}]
    with pytest.raises(ValueError):
        Card(title=title, buttons=buttons)
    buttons = [{"target": "Target Card"}]
    with pytest.raises(ValueError):
        Card(title=title, buttons=buttons)
    # Check the good case.
    buttons = [{"label": "Hello", "target": "Target Card"}]
    Card(title=title, buttons=buttons)


def test_card_verify_buttons_attribute_values():
    """
    Each attribute of the button must be of a certain type:

    * labels must be strings.
    * targets must be either strings or callable.
    """
    title = "title"
    buttons = [{"label": 42, "target": "Target Card"}]
    with pytest.raises(ValueError):
        Card(title=title, buttons=buttons)
    title = "title"
    buttons = [{"label": "Hello", "target": True}]
    with pytest.raises(ValueError):
        Card(title=title, buttons=buttons)
    # Check the good case.
    buttons = [{"label": "Hello", "target": lambda x: x}]
    Card(title=title, buttons=buttons)


def test_card_verify_auto_advance():
    """
    If the auto_advance value is set, there MUST be an auto_target.
    """
    with pytest.raises(ValueError):
        Card(title="title", auto_advance=1.0)
    # Check the good case.
    Card(title="title", auto_advance=1.0, auto_target="Another card")


def test_card_screen_empty():
    """
    Ensure a relatively empty card results in the expected Screen object and
    the passed in ScreenManager instance and data_store is set for the card.
    """
    mock_screen_manager = mock.MagicMock()
    data_store = {"foo": "bar"}
    card = Card("title")
    result = card.screen(mock_screen_manager, data_store)
    assert card.screen_manager == mock_screen_manager
    assert card.data_store == data_store
    assert isinstance(result, Screen)


def test_card_screen_with_form():
    """
    A card with a form has the expected _draw_form method called to paint it
    onto the screen.
    """
    mock_screen_manager = mock.MagicMock()
    data_store = {"foo": "bar"}
    card = Card("title", form=Inputs.TEXTBOX, text="Form instructions...")
    card._draw_form = mock.MagicMock()
    card.screen(mock_screen_manager, data_store)
    card._draw_form.assert_called_once_with()


def test_card_screen_with_text_only():
    """
    If the card has only textual content, ensure the _draw_text method is
    called to paint it onto the screen.
    """
    mock_screen_manager = mock.MagicMock()
    data_store = {"foo": "bar"}
    card = Card("title", text="Textual content...")
    card._draw_text = mock.MagicMock()
    card.screen(mock_screen_manager, data_store)
    card._draw_text.assert_called_once_with()


def test_card_screen_with_sound():
    """
    Ensure that if a sound is associated with a card, that it is instantiated
    and configured correctly as part of the screen generation process.
    """
    mock_screen_manager = mock.MagicMock()
    data_store = {"foo": "bar"}
    card = Card("title", sound="music.wav", sound_repeat=True)
    mock_loader = mock.MagicMock()
    with mock.patch("pypercard.core.SoundLoader.load", mock_loader):
        card.screen(mock_screen_manager, data_store)
        mock_loader.assert_called_once_with("music.wav")
        mock_player = mock_loader()
        assert mock_player.loop is True
        assert card.player == mock_player


def test_card_screen_with_background_colour():
    """
    If a background colour is set for the card, ensure this is correctly
    configured for the layout associated with the card's screen.
    """
    mock_screen_manager = mock.MagicMock()
    data_store = {"foo": "bar"}
    card = Card("title", background="red")
    mock_layout = mock.MagicMock()
    with mock.patch(
        "pypercard.core.BoxLayout", return_value=mock_layout
    ), mock.patch("pypercard.core.Screen"), mock.patch(
        "pypercard.core.Color"
    ) as mock_colour, mock.patch(
        "pypercard.core.Rectangle"
    ) as mock_rectangle:
        card.screen(mock_screen_manager, data_store)
        mock_layout.bind.assert_called_once_with(
            size=card._update_rect, pos=card._update_rect
        )
        mock_colour.assert_called_once_with(1.0, 0.0, 0.0, 1.0)  # "red"
        mock_rectangle.assert_called_once_with(
            size=mock_layout.size, pos=mock_layout.pos
        )
        assert card.rect == mock_rectangle()


def test_card_screen_with_background_image():
    """
    If a background image is set for the card, ensure this is correctly
    configured for the layout associated with the card's screen.
    """
    mock_screen_manager = mock.MagicMock()
    data_store = {"foo": "bar"}
    card = Card("title", background="image.png")
    mock_layout = mock.MagicMock()
    with mock.patch(
        "pypercard.core.BoxLayout", return_value=mock_layout
    ), mock.patch("pypercard.core.Screen"), mock.patch(
        "pypercard.core.Rectangle"
    ) as mock_rectangle:
        card.screen(mock_screen_manager, data_store)
        mock_rectangle.assert_called_once_with(
            source="image.png", size=mock_layout.size, pos=mock_layout.pos
        )


def test_card_screen_with_buttons():
    """
    If buttons are configured for the card, ensure the expected _draw_buttons
    method is called to paint the buttons onto the screen for the card.
    """
    mock_screen_manager = mock.MagicMock()
    data_store = {"foo": "bar"}
    card = Card(
        "title", buttons=[{"label": "A Button", "target": "AnotherButton"}]
    )
    card._draw_buttons = mock.MagicMock()
    card.screen(mock_screen_manager, data_store)
    card._draw_buttons.assert_called_once_with()


def test_card_draw_text():
    """
    Ensure the expected Label object is added to the screen's layout instance.
    """
    card = Card("title", text="This is some text for the label...")
    card.layout = mock.MagicMock()
    card.font_size = "48sp"
    card._draw_text()
    card.layout.add_widget.assert_called_once_with(card.text_label)
    assert card.text_label.text == "This is some text for the label..."
    assert card.text_label.font_size == 48.0
    assert card.text_label.markup is True
    assert card.text_label.color == [1.0, 1.0, 1.0, 1.0]
    assert card.text_label.padding == [10, 10]
    assert card.text_label.valign == "middle"
    assert card.text_label.halign == "center"


def test_card_draw_form_textbox():
    """
    Ensure the expected form widget and associated label are added to the
    screen's layout instance.
    """
    card = Card("title", form=Inputs.TEXTBOX, text="Form label...")
    card.layout = mock.MagicMock()
    card.font_size = "48sp"
    card._draw_form()
    assert card.form_label.text == "Form label..."
    assert card.form_label.font_size == 48.0
    assert card.form_label.markup is True
    assert card.form_label.color == [1.0, 1.0, 1.0, 1.0]
    assert card.form_label.valign == "top"
    assert card.form_label.halign == "left"
    assert card.textbox.text == ""
    assert card.textbox.multiline is False
    assert card.textbox.font_size == 48.0


def test_card_draw_form_textarea():
    """
    Ensure the expected form widget and associated label are added to the
    screen's layout instance.
    """
    card = Card("title", form=Inputs.TEXTAREA, text="Form label...")
    card.layout = mock.MagicMock()
    card.font_size = "48sp"
    card._draw_form()
    assert card.form_label.text == "Form label..."
    assert card.form_label.font_size == 48.0
    assert card.form_label.markup is True
    assert card.form_label.color == [1.0, 1.0, 1.0, 1.0]
    assert card.form_label.valign == "top"
    assert card.form_label.halign == "left"
    assert card.textarea.text == ""
    assert card.textarea.multiline is True
    assert card.textarea.font_size == 48.0


def test_card_draw_form_multichoice():
    """
    Ensure the expected form widget and associated label are added to the
    screen's layout instance.
    """
    card = Card(
        "title",
        form=Inputs.MULTICHOICE,
        text="Form label...",
        options=["foo", "bar", "baz"],
    )
    card.layout = mock.MagicMock()
    card.font_size = "48sp"
    card._draw_form()
    assert card.form_label.text == "Form label..."
    assert card.form_label.font_size == 48.0
    assert card.form_label.markup is True
    assert card.form_label.color == [1.0, 1.0, 1.0, 1.0]
    assert card.form_label.valign == "top"
    assert card.form_label.halign == "left"
    assert len(card.multichoice) == 3
    assert card.multichoice[0].text == "foo"
    assert card.multichoice[0].group is None
    assert card.multichoice[1].text == "bar"
    assert card.multichoice[1].group is None
    assert card.multichoice[2].text == "baz"
    assert card.multichoice[2].group is None


def test_card_draw_form_select():
    """
    Ensure the expected form widget and associated label are added to the
    screen's layout instance.
    """
    card = Card(
        "title",
        form=Inputs.SELECT,
        text="Form label...",
        options=["foo", "bar", "baz"],
    )
    card.layout = mock.MagicMock()
    card.font_size = "48sp"
    card._draw_form()
    assert card.form_label.text == "Form label..."
    assert card.form_label.font_size == 48.0
    assert card.form_label.markup is True
    assert card.form_label.color == [1.0, 1.0, 1.0, 1.0]
    assert card.form_label.valign == "top"
    assert card.form_label.halign == "left"
    assert len(card.select) == 3
    assert card.select[0].text == "foo"
    assert card.select[0].group == "title"
    assert card.select[1].text == "bar"
    assert card.select[1].group == "title"
    assert card.select[2].text == "baz"
    assert card.select[2].group == "title"


def test_card_draw_form_slider_with_step():
    """
    Ensure the expected form widget and associated label are added to the
    screen's layout instance.
    """
    card = Card(
        "title", form=Inputs.SLIDER, text="Form label...", options=(1, 100, 10)
    )
    card.layout = mock.MagicMock()
    card.font_size = "48sp"
    card._draw_form()
    assert card.form_label.text == "Form label..."
    assert card.form_label.font_size == 48.0
    assert card.form_label.markup is True
    assert card.form_label.color == [1.0, 1.0, 1.0, 1.0]
    assert card.form_label.valign == "top"
    assert card.form_label.halign == "left"
    assert card.slider_label.text == "0"
    assert card.slider_label.font_size == 64.0
    assert card.slider.min == 1
    assert card.slider.max == 100
    assert card.slider.step == 10
    assert card.slider.value_track is True


def test_card_draw_form_slider_default_step():
    """
    Ensure the expected form widget and associated label are added to the
    screen's layout instance.
    """
    card = Card(
        "title", form=Inputs.SLIDER, text="Form label...", options=(1, 100)
    )
    card.layout = mock.MagicMock()
    card.font_size = "48sp"
    card._draw_form()
    assert card.form_label.text == "Form label..."
    assert card.form_label.font_size == 48.0
    assert card.form_label.markup is True
    assert card.form_label.color == [1.0, 1.0, 1.0, 1.0]
    assert card.form_label.valign == "top"
    assert card.form_label.halign == "left"
    assert card.slider_label.text == "0"
    assert card.slider_label.font_size == 64.0
    assert card.slider.min == 1
    assert card.slider.max == 100
    assert card.slider.step == 1
    assert card.slider.value_track is True


def test_card_draw_buttons():
    """
    Ensure the expected buttons are created and linked to an event handler.
    """
    card = Card(
        "title", buttons=[{"label": "Button1", "target": "AnotherCard"}]
    )
    card.layout = mock.MagicMock()
    card._button_click = mock.MagicMock()
    card._draw_buttons()
    assert len(card.button_widgets) == 1
    assert card.button_widgets[0].text == "Button1"
    assert card.button_widgets[0].color == [1.0, 1.0, 1.0, 1.0]  # white.
    assert card.button_widgets[0].background_color == [
        0.7450980392156863,
        0.7450980392156863,
        0.7450980392156863,
        1.0,
    ]  # grey.
    assert card.button_widgets[0].font_size == 24.0
    card._button_click.assert_called_once_with("AnotherCard")
    assert card.layout.add_widget.call_count == 1


def test_card_draw_buttons_custom_size_colours():
    """
    Ensure that customisations to the buttons text size, text colour and
    background colour are set as expected.
    """
    card = Card(
        "title",
        buttons=[
            {
                "label": "Button1",
                "target": "AnotherCard",
                "text_size": 32,
                "text_color": "red",
                "background_color": "blue",
            }
        ],
    )
    card.layout = mock.MagicMock()
    card._button_click = mock.MagicMock()
    card._draw_buttons()
    assert len(card.button_widgets) == 1
    assert card.button_widgets[0].text == "Button1"
    assert card.button_widgets[0].font_size == 32.0
    assert card.button_widgets[0].color == [1.0, 0.0, 0.0, 1.0]
    assert card.button_widgets[0].background_color == [0.0, 0.0, 1.0, 1.0]
    card._button_click.assert_called_once_with("AnotherCard")
    assert card.layout.add_widget.call_count == 1


def test_card_form_value_no_form():
    """
    Must return None if there is no form associated with the card.
    """
    card = Card("title")
    assert card.form_value() is None


def test_card_form_value_textbox():
    """
    Return the current value of the textbox widget.
    """
    card = Card("title", form=Inputs.TEXTBOX, text="Form label...")
    mock_screen_manager = mock.MagicMock()
    data_store = {}
    card.screen(mock_screen_manager, data_store)
    card.textbox.text = "foobarbaz"
    assert card.form_value() == "foobarbaz"


def test_card_form_value_textarea():
    """
    Return the current value of the textarea widget.
    """
    card = Card("title", form=Inputs.TEXTAREA, text="Form label...")
    mock_screen_manager = mock.MagicMock()
    data_store = {}
    card.screen(mock_screen_manager, data_store)
    card.textarea.text = "foobarbaz"
    assert card.form_value() == "foobarbaz"


def test_card_form_value_multichoice():
    """
    Return the current value of the multichoice widget.
    """
    card = Card(
        "title",
        form=Inputs.MULTICHOICE,
        text="Form label...",
        options=["foo", "bar", "baz"],
    )
    mock_screen_manager = mock.MagicMock()
    data_store = {}
    card.screen(mock_screen_manager, data_store)
    card.multichoice[0].state = "down"
    card.multichoice[2].state = "down"
    assert card.form_value() == ["foo", "baz"]


def test_card_form_value_select():
    """
    Return the current value of the select widget.
    """
    card = Card(
        "title",
        form=Inputs.SELECT,
        text="Form label...",
        options=["foo", "bar", "baz"],
    )
    mock_screen_manager = mock.MagicMock()
    data_store = {}
    card.screen(mock_screen_manager, data_store)
    card.select[0].state = "down"
    assert card.form_value() == "foo"


def test_card_form_value_select_nothing():
    """
    Return the current value of the select widget, if none are selected (should
    return None).
    """
    card = Card(
        "title",
        form=Inputs.SELECT,
        text="Form label...",
        options=["foo", "bar", "baz"],
    )
    mock_screen_manager = mock.MagicMock()
    data_store = {}
    card.screen(mock_screen_manager, data_store)
    assert card.form_value() is None


def test_card_form_value_slider():
    """
    Return the current value of the slider widget.
    """
    card = Card(
        "title", form=Inputs.SLIDER, text="Form label...", options=[1, 100]
    )
    mock_screen_manager = mock.MagicMock()
    data_store = {}
    card.screen(mock_screen_manager, data_store)
    card.slider_label.text = "50"
    assert card.form_value() == 50.0


def test_card_pre_enter_with_form():
    """
    The _pre_enter method is called before the card is displayed to the
    user. Ensure that all textual content is updated with a formatted string
    with the data_store as potential values.
    """
    card = Card("title")
    card.text = "Hello {foo}"
    card.form = Inputs.TEXTBOX
    card.form_label = mock.MagicMock()
    card.buttons = [{"label": "Hello {foo}", "target": "AnotherCard"}]
    card.screen(mock.MagicMock(), {"foo": "world"})
    card._pre_enter(card)
    assert card.form_label.text == "Hello world"
    assert card.button_widgets[0].text == "Hello world"


def test_card_pre_enter_with_text():
    """
    The _pre_enter method is called before the card is displayed to the
    user. Ensure that all textual content is updated with a formatted string
    with the data_store as potential values.
    """
    card = Card("title")
    card.text = "Hello {foo}"
    card.text_label = mock.MagicMock()
    card.buttons = [{"label": "Hello {foo}", "target": "AnotherCard"}]
    card.screen(mock.MagicMock(), {"foo": "world"})
    card._pre_enter(card)
    assert card.text_label.text == "Hello world"
    assert card.button_widgets[0].text == "Hello world"


def test_card_enter():
    """
    The _enter method is called when the card is displayed to the user. Ensure
    that the sound player starts from position zero and the auto advance is
    scheduled.
    """
    card = Card("title")
    card.player = mock.MagicMock()
    card.auto_advance = 1.5
    with mock.patch("pypercard.core.Clock") as mock_clock:
        card._enter(card)
        mock_clock.schedule_once.assert_called_once_with(
            card._next_card, card.auto_advance
        )
        card.player.play.assert_called_once_with()
        card.player.seek.assert_called_once_with(0)


def test_card_leave():
    """
    The _leave method is called when the card is hidden from the user. Ensure
    that the sound player is stopped.
    """
    card = Card("title")
    card.player = mock.MagicMock()
    card._leave(card)
    card.player.stop.assert_called_once_with()


def test_card_update_rect():
    """
    Called whenever the application size changes to ensure that the rectangle
    that contains the screen to be drawn is also updated in size (so the
    background colour / image is updated, if required).
    """
    card = Card("title")
    card.rect = mock.MagicMock()
    instance = mock.MagicMock()
    instance.pos = 400
    instance.size = 500
    card._update_rect(instance, 100)
    assert card.rect.pos == instance.pos
    assert card.rect.size == instance.size


def test_card_button_click_with_callable():
    """
    Ensure the function returned from the _button_click method works by
    transitioning the screen manager to the string value it returns.
    """

    def fn(data_store, form_value):
        return "AnotherCard"

    card = Card("title")
    card.data_store = {}
    card.form_value = mock.MagicMock(return_value=None)
    card.screen_manager = mock.MagicMock()
    handler = card._button_click(fn)
    assert callable(handler)
    handler(None)
    assert card.screen_manager.current == "AnotherCard"


def test_card_button_click_with_string():
    """
    Ensure the function returned from the _button_click method works by
    transitioning the screen manager to the string value it returns.
    """
    card = Card("title")
    card.data_store = {}
    card.form_value = mock.MagicMock(return_value=None)
    card.screen_manager = mock.MagicMock()
    handler = card._button_click("AnotherCard")
    assert callable(handler)
    handler(None)
    assert card.screen_manager.current == "AnotherCard"


def test_card_slider_change():
    """
    Ensure this event handler updates the slider_label with the passed in
    value.
    """
    card = Card("title")
    card.slider_label = mock.MagicMock()
    card._slider_change(None, 10)
    assert card.slider_label.text == "10.0"


def test_card_next_card_with_callable():
    """
    Ensure the string return value of the function set as the auto_target is
    used to transition the screen manager.
    """

    def fn(data_store, form_value):
        return "AnotherCard"

    card = Card("title")
    card.data_store = {}
    card.form_value = mock.MagicMock(return_value=None)
    card.auto_target = fn
    card.screen_manager = mock.MagicMock()
    card._next_card(0.1)
    assert card.screen_manager.current == "AnotherCard"


def test_card_next_card_with_string():
    """
    Ensure the string value set as the auto_target is used to transition the
    screen manager.
    """
    card = Card("title")
    card.data_store = {}
    card.form_value = mock.MagicMock(return_value=None)
    card.auto_target = "AnotherCard"
    card.screen_manager = mock.MagicMock()
    card._next_card(0.1)
    assert card.screen_manager.current == "AnotherCard"


def test_cardapp_init_no_data_store():
    """
    Ensure the CardApp instance is set up with the expected defaults.
    """
    app = CardApp()
    assert app.data_store == {}
    assert app.cards == {}
    assert isinstance(app.screen_manager, ScreenManager)
    assert app.title == "A PyperCard Application :-)"


def test_cardapp_init_title_datastore_and_stack():
    """
    Ensure the CardApp instance is set up with the expected user defined
    values.
    """
    stack = [Card("test")]
    app = CardApp("An App", {"foo": "bar"}, stack)
    assert app.data_store == {"foo": "bar"}
    assert app.cards == {"test": stack[0]}
    assert isinstance(app.screen_manager, ScreenManager)
    assert app.title == "An App"


def test_cardapp_add_card():
    """
    The referenced card should be added to the app's screen_manager instance
    and the cards dictionary.
    """
    app = CardApp()
    app.screen_manager = mock.MagicMock()
    card = Card("title")
    card.screen = mock.MagicMock()
    app.add_card(card)
    assert app.cards["title"] == card
    app.screen_manager.add_widget.assert_called_once_with(
        card.screen(None, None)
    )


def test_cardapp_load():
    """
    Ensure the referenced JSON file is used to instantiate a card and add it to
    the application.
    """
    current_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.abspath(os.path.join(current_dir, "test_stack.json"))
    app = CardApp()
    app.add_card = mock.MagicMock()
    app.load(path)
    assert app.add_card.call_count == 2


def test_cardapp_build():
    """
    Ensure the screen_manager instance is returned to display as the
    application.
    """
    app = CardApp()
    assert isinstance(app.build(), ScreenManager)
