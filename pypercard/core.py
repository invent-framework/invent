"""
Copyright (c) 2019 Nicholas Tollervey.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import kivy
kivy.require('1.11.1')
import json
import struct
from colours import COLOURS
from enum import Enum
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton 


def palette(name):
    """
    Given a name of a colour (e.g. "red", "green", "blue"), a hex value
    (e.g. "0xFFAACC") or an HTML hex value (e.g. "#FFAACC"), returns a tuple
    containing the colours converted to Kivy's own colour coding system.

    For a list of all the available colours see the keys in the colours.py
    module.

    :param str name: The name of the colour whose value is needed.
    :return: The colour expressed as a tuple of numbers used by Kivy.
    :raises ValueError: if the name of the colour is unknown.
    """
    def from_hex(val):
        """
        Given a raw HEX value (e.g. "FFAACC"), convert it to the colour
        encoding used by Kivy.
        """
        r, g, b = struct.unpack('BBB', bytes.fromhex(name))
        return (r // 255.0, g // 255.0, b // 255.0)

    if name in COLOURS:
        return COLOURS[name]
    elif name.startswith("0x")
        # Convert from hex to Kivy colour.
        name = name[2:]
        return from_hex(name)
    elif name.startswith("#"):
        # Convert from HTML hex to Kivy colour.
        name = name[1:]
        return from_hex(name)
    else:
        raise ValueError("No such colour called {}".format(name))


class Inputs(Enum):
    """
    Defines the available types of form control. Only one form control can
    appear in each card.
    """
    TEXTBOX = 1  #: A single line text box.
    TEXTAREA = 2  #: A multi-line text area.
    MULTICHOICE = 3  #: A multi-choice selection.
    SELECT = 4  #: A single choice selection.
    SLIDER = 5  #: A slider with a numeric min, max and step.


class Card:
    """
    Represents a "card" in the application. This is a node in a series of
    possible UI states. Transitions between states are generally facilitated by
    button presses with either an associated string containing the title of the
    target card, or a function (containing "business logic") which returns a
    string identifying the next card.

    Each node has pre-defined attributes which describe the appearance of
    the card and the behaviour for transitioning to other cards in the
    application. These are set and verified upon initialisation.
    """

    def __init__(self, title, text=None, text_color=None, text_size=48,
                 form=None, label=None, options=None, sound=None,
                 sound_repeat=False, background=None, button1="", button2="",
                 button3="", target1="", target2="", target3="",
                 auto_advance=0, auto_target=None):
        """
        Initialise and check the state of the Card. Will raise an exception if
        the passed in state is inconsistent.

        :param str title: The unique meaningful title/id of the card.
        :param str text: The textual content of the card.
        :param str text_color: The colour of the textual content of the card.
        :param int text_size: The font size of the textual content of the card.
        :param Inputs form: The form input element to display on the card.
        :param str label: The label associated with the form input element.
        :param list options: The form input element's multiple options.
        :param str sound: The path to the sound file to play with the card.
        :param bool sound_repeat: A flag to indicate if the card's sound loops.
        :param str background: Either a colour or path to background image.
        :param str button1: The text on button 1.
        :param str button2: The text on button 2.
        :param str button3: The text on button 3.
        :param target1: Either a string or function returning a string
        referencing the target card when button 1 is pressed.
        :param target2: Either a string or function returning a string
        referencing the target card when button 2 is pressed.
        :param target3: Either a string or function returning a string
        referencing the target card when button 3 is pressed.
        :param float auto_advance: The number of seconds to wait before
        advancing to the auto_target card.
        :param auto_target: Either a string or function returning a string
        referencing the target card for auto-advancement.
        :return: None
        :raises ValueError: If the states passed in are inconsistent.
        """
        self.title = title
        if text_color is None:
            self.text_color = palette("white")
        if isinstance(text_color, str):
            self.text_color = palette(text_color)
        self.text = text
        self.text_size = text_size
        self.form = form
        self.options = options
        self.label = label
        self.sound = sound
        self.sound_repeat = sound_repeat
        self.background = background
        self.button1 = button1
        self.target1 = target1
        self.button2 = button2
        self.target2 = target2
        self.button3 = button3
        self.target3 = target3
        self.auto_advance = auto_advance
        self.auto_target = auto_target
        self._verify()

    def _verify(self):
        """
        Ensure the combination of attributes given while initialising this
        class is valid. Will raise an exception if so.

        :return: None (if no problems found).
        :raises ValueError: if inconsistencies in the form's attributes are
        found.
        """
        if self.text and self.form:
            # A card can only display either text OR a form widget, not both.
            raise ValueError(f"Form '{title}' cannot contain both a "
                             "form and text.")
        if self.form and not self.label:
            # A form MUST have a descriptive label (instructions).
            raise ValueError(f"Form '{title}' must have a label.")
        if self.form == Inputs.MULTICHOICE or self.form == Inputs.SELECT:
            # There must be an options list for multichoice or select forms.
            if isinstance(self.options, tuple) or \
                    isinstance(self.options, list):
                # All options must be strings.
                if not all(isinstance(item, str) for item in self.options):
                    raise ValueError(f"Form '{title}' options must be "
                                     "strings.")
            else:
                raise ValueError(f"Form '{title}' must have an options list.")
        if self.form == Inputs.SLIDER:
            # Slider must have options containing min, max and optional step.
            if isinstance(self.options, tuple) or \
                    isinstance(self.options, list):
                length = len(self.options)
                if length == 2 or length == 3:
                    # All options must be integers.
                    if not all(isinstance(item, int) for item in self.options):
                        raise ValueError(f"Form '{title}' options must be "
                                         "integers.")
                else:
                    raise ValueError(f"Form '{title}' must have no less than "
                                     "two, or more than three options to "
                                     "define the range of slider.")
            else:
                raise ValueError(f"Form '{title}' must have options for "
                                 "min, max and step range of slider.")
        if self.button1 and not self.target1:
            # If there's a button 1, clicking it must be handled.
            raise ValueError(f"Form '{title}' must handle button 1.")
        if self.button2 and not self.target2:
            # If there's a button 2, clicking it must be handled.
            raise ValueError(f"Form '{title}' must handle button 2.")
        if self.button3 and not self.target3:
            # If there's a button 3, clicking it must be handled.
            raise ValueError(f"Form '{title}' must handle button 3.")
        if self.auto_advance and not self.auto_target:
            # If there's an auto_advance flag, there must be a target card.
            raise ValueError(f"Form '{title}' must auto-advance to a card.")

    def screen(self, screen_manager, data_store):
        """
        Return a screen instance containing all the necessary UI items that
        have been associated with the expected event handlers.

        :param kivy.uix.screenmanager.ScreenManager screen_manager: The UI
        stack of screens which controls which card is to be displayed.
        :param dict data_store: A dictionary containing application state.
        :return kivy.uix.screenmanager.Screen: A graphical representation of
        the card.
        """
        # References to app related objects.
        self.screen_manager = screen_manager
        self.data_store = data_store
        # The Kivy Screen instance used to draw the UI.
        screen = Screen(name=self.title)
        # Bind event handlers to life-cycle events.
        screen.bind(on_enter=self._enter)
        screen.bind(on_pre_enter=self._pre_enter)
        screen.bind(on_pre_leave=self._leave)
        # The main layout that defines how UI elements are drawn.
        self.layout = BoxLayout(orientation='vertical')
        screen.add_widget(layout)
        # The sound player for this card.
        self.player = None
        # Text font size for the Screen instance.
        self.font_size = "{}sp".format(self.text_size)
        if self.text:
            self._draw_text()
        elif self.form:
            self._draw_form()
        else:
            layout.add_widget(Label(text=" "))
        if self.sound:
            self.player = SoundLoader.load(self.sound)
            self.player.loop = self.sound_repeat
        if self.background:
            layout.bind(size=self._update_rect, pos=self._update_rect)
            with layout.canvas.before:
                if isinstance(self.background, tuple):
                    Color(*self.background)
                    self.rect = Rectangle(size=layout.size, pos=layout.pos)
                else:
                    self.rect = Rectangle(source=self.background,
                                          size=layout.size, pos=layout.pos)
        if self.button1 or self.button2 or self.button3:
            self._draw_buttons()
        return screen

    def _draw_text(self):
        """
        Encompasses the drawing of text onto the card.
        """
        self.text_label = Label(text=self.text, font_size=self.font_size,
                                markup=True)
        self.text_label.color = list(self.text_color)
        self.text_label.padding = 10, 10
        self.text_label.text_size = (Window.width, Window.height) 
        self.text_label.valign = "middle"
        self.text_label.halign = "center"
        self.layout.add_widget(self.text_label)

    def _draw_form(self):
        """
        Encompasses the drawing of a form onto the card.
        """
        inner_layout = BoxLayout(orientation='vertical')
        label_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.2))
        self.form_label = Label(text=self.label, font_size=self.font_size,
                                markup=True)
        self.form_label.color = list(self.text_color)
        self.form_label.valign = "top"
        self.form_label.halign = "left"
        label_layout.add_widget(self.form_label)
        form_layout = BoxLayout(orientation='vertical')
        form_layout.padding = 10
        filler = None
        if self.form == Inputs.TEXTBOX:
            self.textbox = TextInput(text='', multiline=False)
            self.textbox.font_size = self.font_size
            form_layout.size_hint = (1, 0.2)
            form_layout.add_widget(self.textbox)
            filler = BoxLayout(orientation='vertical', size_hint=(1, 0.6))
        elif self.form == Inputs.TEXTAREA:
            self.textarea = TextInput(text='')
            self.textarea.font_size = self.font_size
            form_layout.add_widget(self.textarea)
        elif self.form == Inputs.MULTICHOICE:
            self.multichoice = []
            for item in self.options:
                button = ToggleButton(text=item)
                button.font_size = self.font_size
                form_layout.add_widget(button)
                self.multichoice.append(button)
        elif self.form == Inputs.SELECT:
            self.select = []
            for item in self.options:
                button = ToggleButton(text=item, group=self.title)
                button.font_size = self.font_size
                form_layout.add_widget(button)
                self.select.append(button)
        elif self.form == Inputs.SLIDER:
            min_val = self.options[0]
            max_val = self.options[1]
            if len(self.options) == 3:
                step = self.options[2]
            else:
                step = 1
            self.slider = Slider(value_track=True, min=min_val,
                                 max=max_val, step=step)
            self.slider_label = Label(text="0", font_size=64)
            self.slider.bind(value=self._slider_change)
            form_layout.add_widget(self.slider)
            form_layout.add_widget(self.slider_label)
        inner_layout.add_widget(label_layout)
        inner_layout.add_widget(form_layout)
        if filler:
            inner_layout.add_widget(filler)
        self.layout.add_widget(inner_layout)

    def _draw_buttons(self):
        """
        Encompasses the drawing of buttons onto the card.
        """
        button_layout = BoxLayout(orientation='horizontal',
                                  size_hint=(1, 0.2))
        if self.button1:
            self.b1 = Button(text=self.button1)
            self.b1.bind(on_press=self._button_click(self.target1))
            button_layout.add_widget(self.b1)
        if self.button2:
            self.b2 = Button(text=self.button2)
            self.b2.bind(on_press=self._button_click(self.target2))
            button_layout.add_widget(self.b2)
        if self.button3:
            self.b3 = Button(text=self.button3)
            self.b3.bind(on_press=self._button_click(self.target3))
            button_layout.add_widget(self.b3)
        layout.add_widget(button_layout)

    def form_value(self):
        """
        Return the value obtained from the user via the form associated with
        this card. Return None if no form is specified.
        """
        if self.form:
            if self.form == Inputs.TEXTBOX:
                return self.textbox.text
            elif self.form == Inputs.TEXTAREA:
                return self.textarea.text
            elif self.form == Inputs.MULTICHOICE:
                return [toggle.text for toggle in self.multichoice
                        if toggle.state == "down"]
            elif self.form == Inputs.SELECT:
                for button in self.select:
                    if button.state == "down":
                        return button.text
                return None
            elif self.form == Inputs.SLIDER:
                return float(self.slider_label.text)
        else:
            return None

    def _pre_enter(self, card):
        """
        Called immediately before the card is displayed to the user. Ensure
        that all the UI elements containing textual values are formatted with
        values from the data_store dictionary.
        """
        if self.text:
            self.text_label.text = self.text.format(**self.data_store)
        if self.label:
            self.form_label.text = self.label.format(**self.data_store)
        if self.button1:
            self.b1.text = self.button1.format(**self.data_store)
        if self.button2:
            self.b2.text = self.button2.format(**self.data_store)
        if self.button3:
            self.b3.text = self.button3.format(**self.data_store)

    def _enter(self, card):
        """
        Called when the card is displayed to the user. Ensure that any sound
        associated with the card starts to play and, if necessary, auto_advance
        is scheduled.
        """
        if self.player:
            self.player.play()
            self.player.seek(0)
        if self.auto_advance:
            Clock.schedule_once(self._next_card, self.auto_advance)

    def _leave(self, card):
        """
        Called when the card is hidden from the user. Ensure that any sound
        associated with the card is stopped.
        """
        if self.player:
            self.player.stop()

    def _update_rect(self, instance, value):
        """
        Ensure that the rectangle (containing the background image, if set) is
        resized if the application is resized.
        """
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def _button_click(self, target):
        """
        Return a callable to handle a button click that correctly transitions
        to the next card given the value of the target argument.

        If target is a string, transition to the card identified by that
        string.

        If target is a callable, call the function and transition to the card
        identified by the string result.
        """
        def on_click(button):
            if callable(target):
                next_card = target(self.data_store, self.form_value())
            else:
                next_card = target
            self.screen_manager.current = next_card
        return on_click

    def _slider_change(self, slider, value):
        """
        An event handler to ensure the slider's label always displays the
        current slider value.
        """
        self.slider_label.text = str(float(value))

    def _next_card(self, time_taken):
        """
        Transition to the next card according to the value of auto_target.

        If auto_target is a string, transition to the card identified by that
        string.

        If auto_target is a callable, call the function and transition to the
        card identified by the string result.
        """
        if callable(self.auto_target):
            next_card = self.auto_target(self.data_store, self.form_value())
        else:
            next_card = self.auto_target
        self.screen_manager.current = next_card


class CardApp(App):
    """
    An app with more than a passing resemblance to HyperCard stacks. :-)
    """

    def __init__(self, name="Python Application", data_store=None):
        """
        Setup with a clean state.
        """
        super().__init__()
        # A simple key/value store for application state / data.
        if data_store is None:
            self.data_store = {}
        else:
            self.data_store = data_store
        # Contains the card objects which drive the application.
        self.cards = {}
        # Define the nature and duration of the transition between cards.
        transition = FadeTransition()
        transition.duration = 0.1
        # The screen manager containing all the screens that make up the stack
        # of cards.
        self.screen_manager = ScreenManager(transition=transition)
        # Set the window title to the app's name.
        self.title = name

    def add_card(self, card):
        """
        Given a card instance, add it to the application.
        """
        self.cards[card.title] = card
        screen = card.screen(self.screen_manager, self.data_store)
        self.screen_manager.add_widget(screen)

    def load(self, filename):
        """
        Load and instantiate a stack of cards from the referenced JSON file.
        """
        with open(filename) as f:
            stack = json.load(f)
            for card in stack:
                c = Card(card["card_id"])
                if "background_image" in card:
                    c.background = card["background_image"]
                if "text" in card:
                    c.text = card["text"]
                if "text_color" in card:
                    c.text_color = palette(card["text_color"])
                if "sound" in card:
                    c.sound = card["sound"]
                if "sound_repeat" in card:
                    c.sound_repeat = card["sound_repeat"] == True
                if "button01_text" in card:
                    c.button1 = card["button01_text"]
                if "button01_goto_card_id" in card:
                    c.target1 = card["button01_goto_card_id"]
                if "button02_text" in card:
                    c.button2 = card["button02_text"]
                if "button02_goto_card_id" in card:
                    c.target2 = card["button02_goto_card_id"]
                self.add_card(c)

    def build(self):
        """
        Called by Kivy to display something (in this case the screen manager
        containing all the screens).
        """
        return self.screen_manager
