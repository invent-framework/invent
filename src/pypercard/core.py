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
import collections
import functools
import inspect
from pyodide import ffi
from js import document, CSS, clearTimeout, setTimeout, Audio, fetch
from pypercard.state_machine import Machine, State, Transition
from pypercard.datastore import DataStore


class Card:
    """
    Represents a card in the application. A card defines what is presented to
    the user.

    The app ensures that only one card is ever displayed at once. Each card
    has a `name` and an HTML `template` that defines how it looks on the page.

    Cards may also have optional `auto_advance` and `transition`
    attributes for transitioning to a target card after a given period of time.

    Cards are rendered from the `template` in the `show` method. The first time
    `show` is called it creates a `pyper-card` HTML element for the app to
    insert into the DOM.

    Bespoke behaviour for rendering can be defined by the user. This should
    be passed in as the optional `on_show` argument when initialising the
    card. It will be called, at the end of the card's `show` function, but
    before the element to insert into the DOM is returned to the app. The
    `on_show` function is called with the same arguments as a transition
    function: a reference to the app and the current card.

    The `hide` method hides card's HTML element, but leaves it in the DOM.

    Card's can optionally take some action each time a card is hidden using the
    `on_hide` method. The `on_hide` method is called with the same arguments as
    a transition function: a reference to the app and the current card.

    It's also possible to use the `register_transition` method to register a
    user defined function to handle events dispatched by elements found in the
    card's HTML. These transition the app to new cards.

    The convenience functions called `get_by_id`, `get_element` and
    `get_elements` return individual or groups of matching HTML elements
    rendered by this card, given a valid id or CSS selector (comments attached
    to the functions explain the specific behaviours).

    Cards can optionally define the nature of their background, via the
    `background` and `background_repeat` attributes. The `background` should
    either be a valid CSS color or a URL to an image. If the `background` is
    an image, the `background_repeat` flag will indicate if the image will
    fill the whole screen or repeat in a tiled fashion (the default is to
    fill the whole screen).
    """

    def __init__(
        self,
        name,
        template=None,
        on_show=None,
        on_hide=None,
        auto_advance=None,
        transition=None,
        sound=None,
        sound_loop=False,
        background=None,
        background_repeat=False,
    ):
        """
        Initialise the card with a `name` unique within the application in
        which it is used.

        The following optional arguments are available to customize the card's
        appearance and behaviour.

        The string content of the `template` argument is used to render the
        card. If not given, the card will attempt to extract the `innerHTML`
        from a `template` tag with an id of the given name of the card.
        Otherwise, the card will raise a `RuntimeError`.

        The `on_show` function is called every time the card is shown. It
        should take `app` and `card` arguments (just like transitions)
        and be used for customising the rendered card.

        The `on_hide` function is called every time the card is hidden. It
        should take `app` and `card` arguments (just like transitions)
        and be used for stopping actions (sounds etc.).

        The `auto_advance` is the number of seconds, as a `float` or
        `int`, to wait until the `transition` is evaluated to discern the
        next card to which to automatically transition.

        The `transition` can be either a string containing the name of the
        card to which to automatically transition, or a transition function to
        call that returns a string containing the name of the next card.

        Either both `auto_advance` and `transition` need to be given,
        or both need to be `None`. Otherwise, the card will raise a
        `ValueError`. If the `transition` is not a string or function or the
        `auto_advance` is not an integer or float, a `TypeError` will be
        raised.

        The optional `background` argument can either contain a valid CSS
        `color` or a URL to an image to display as the background.

        The optional `background_repeat` flag defines if the `background`
        image fills the whole screen (the default) or repeats in a tiled
        fashion (if the flag is set to `True`).
        """
        self.name = name
        self.auto_advance = None
        self.transition = None
        self.sound = sound
        self.sound_loop = sound_loop
        self.background = background
        self.background_repeat = background_repeat
        # Template handling / validation.
        if template:
            self.template = template
        else:
            templateElement = document.querySelector("template#" + self.name)
            if templateElement:
                self.template = templateElement.innerHTML
            else:
                raise RuntimeError(
                    f"Unable to find template for card '{self.name}'."
                )
        # Check both values are a pair: either both truth-y or both false-y.
        if bool(auto_advance) != bool(transition):
            raise ValueError("Both auto_advance AND transition are required.")
        # Auto advance/target setup and validation.
        if auto_advance:
            if isinstance(auto_advance, float) or isinstance(
                auto_advance, int
            ):
                # Python counts time in seconds (that may be floats to indicate
                # fractions-of-a-second, or integers).
                self.auto_advance = float(auto_advance)
            else:
                raise TypeError(
                    "Please use a number of seconds for auto_advance."
                )
        if transition:
            if isinstance(transition, str):
                self.transition = lambda app, card: transition
            elif callable(transition):
                self.transition = transition
            else:
                raise TypeError(
                    "The transition must be either a string or function."
                )
        # Pre-fetch/cache background image.
        if self.background and not CSS.supports("color", self.background):
            fetch(self.background)
        self.on_show = on_show
        self.on_hide = on_hide
        self._transitions = []  # To hold transitions acting on the card.
        self.content = None  # Will reference the rendered element in the DOM.
        self.app = None  # Will reference the parent application.
        self._auto_advance_timer = (
            None  # Will reference a timer for auto-advancing.
        )

    def register_app(self, app):
        """
        Add a reference to the hosting app, of which this card is a part.
        """
        self.app = app

    def show(self):
        """
        Show the card (i.e. make it visible to the user).

        If this is the first time the card has been shown a `pyper-card`
        element will be created for it and inserted into the DOM (as a child
        of the app's `pyper-app` element).

        If the card has already been shown then we simply make it visible by
        setting the element's display attribute to "block".

        Ensures the template is `.format`-ed with the self.app.datastore
        dictionary (so named custom values can be inserted into the template).

        Rebinds any user defined transitions to the newly rendered elements
        created by the card.
        """
        # Create the card's content element if it doesn't already exist.
        if not self.content:
            self.content = document.createElement("pyper-card")

        html = self.template.format(**self.app.datastore)
        self.content.innerHTML = html

        # Set an auto-advance timer if required.
        if self.auto_advance is not None:

            def on_timeout():
                """Called when the card timer has timed-out!"""

                self.app.machine.next({"event": "timeout", "card": self})

            # Python sleeps in seconds, JavaScript in milliseconds :)
            self._auto_advance_timer = setTimeout(
                ffi.create_proxy(on_timeout), int(self.auto_advance * 1000)
            )

        # Add DOM event listeners for any transitions added via
        # "app.transition".
        for transition in self._transitions:
            if transition["selector"] == "pyper-card":
                target_elements = [self.content]

            else:
                target_elements = self.get_elements(transition["selector"])

            for element in target_elements:

                def handler(transition, evt):
                    self.app.machine.next(
                        {"event": transition["event_name"], "dom_event": evt}
                    )

                handler_proxy = ffi.create_proxy(
                    functools.partial(handler, transition)
                )
                transition["handler"] = handler_proxy

                element.addEventListener(
                    transition["event_name"], transition["handler"]
                )

        # Ensure user-supplied "on_show" is called.
        if self.on_show:
            self.on_show(self.app, self)

        # And finally... show the card content!
        self.content.style.display = "block"

        return self.content

    def hide(self):
        """
        Hide the card (i.e. make it invisible to the user!).

        This leaves the card in the DOM but just sets 'display' to None, and
        removes any DOM event listeners.
        """
        self.content.style.display = "none"

        # Clear the auto-advance timer if necessary.
        if self._auto_advance_timer:
            clearTimeout(self._auto_advance_timer)

        # Remove any DOM event listeners that were hooked up when the card was
        # shown.
        for transition in self._transitions:
            target_elements = self.get_elements(transition["selector"])
            for element in target_elements:
                element.removeEventListener(
                    transition["event_name"], transition["handler"]
                )

        # Ensure user-supplied "on_hide" is called.
        if self.on_hide:
            self.on_hide(self.app, self)

    def register_transition(self, event_name, element_id=None):
        """
        `event_name` - e.g. "click"
        `element_id` - the unique ID identifying the target element.
        """
        # Card level...
        if element_id is None:
            selector = "pyper-card"

        elif element_id is not None:
            selector = "#" + element_id

        else:
            raise ValueError("We don't have no query yet!")

        self._transitions.append(
            {
                "event_name": event_name,
                "selector": selector,
            }
        )

    def get_by_id(self, element_id):
        """
        Convenience function for getting a child element by id. Returns `None`
        if no element is found.
        """
        return self.get_element("#" + element_id)

    def get_element(self, selector):
        """
        Convenience function for getting a child element that matches the
        passed in CSS selector. Returns `None` if no element is found.
        """
        if self.content:
            return self.content.querySelector(selector)

    def get_elements(self, selector):
        """
        Convenience function for getting a Python list of child elements that
        match the passed in CSS selector. Returns an empty list if no elements
        are found.
        """
        if self.content:
            return list(self.content.querySelectorAll(selector))
        return []


class App:
    """
    Represents a HyperCard-ish application.

    This encapsulates the state (as a `DataStore`), stack of `Card` instances,
    and registering transitions.

    Other app-wide functions (such as playing or pausing sounds) are methods
    of this class.

    Furthermore, it will be possible to dump and load a declarative `JSON`
    representation of the application.

    If no default arguments given, the app will assume sensible defaults.
    """

    def __init__(
        self,
        name=None,
        datastore=None,
        cards=None,
        sounds=None,
    ):
        """
        Initialise a PyperCard app.

        If no `name` is given, the page's `title` value is used, otherwise the
        given `name` becomes the page `title`.

        The `datastore` is an optional pre-populated `DataStore` instance.

        The `cards` is an optional list of `Card` instances with which to
        initialise.

        The `sounds` dict contains default `name` / `url` pairs that define
        the initial sounds the app may need to play.
        """
        self.started = False
        if name:
            self.name = name
            # Update the page title to the name of the app.
            document.querySelector("title").innerText = self.name
        else:
            # No name given, so use the page title.
            self.name = document.querySelector("title").innerText
        self.datastore = datastore if datastore else DataStore()
        self.stack = collections.OrderedDict()
        self.machine = Machine(self)
        self.sounds = {}

        card_list = cards or self._harvest_cards_from_dom()
        if not card_list:
            raise RuntimeError("Cannot find cards for application.")

        for card in card_list:
            self.add_card(card)

        if sounds:
            for name, url in sounds.items():
                self.add_sound(name, url)

        # Create the element into which the app will appear.
        self.placeholder = document.createElement("pyper-app")
        document.body.appendChild(self.placeholder)
        # Ensure the <html> and <body> tags have the expected style (needed for
        # background images).
        style = document.createElement("style")
        style.innerText = "html, body {width:100%;height:100%;}"
        document.head.appendChild(style)

    def _harvest_cards_from_dom(self):
        """
        Harvest any cards defined in the DOM.

        This queries the DOM for all 'template' tags and uses their attributes
        to configure card.

        Returns a (possibly empty) list of the Card instances.
        """
        cards = []
        transitions = []
        for card_template in document.querySelectorAll("template"):
            name = card_template.id
            template = card_template.innerHTML
            auto_advance = card_template.getAttribute("auto-advance")
            if auto_advance:
                auto_advance = float(auto_advance)
            transition = card_template.getAttribute("transition")
            background = card_template.getAttribute("background")
            background_repeat = card_template.getAttribute("background-repeat")
            sound = card_template.getAttribute("sound")
            if sound:
                self.add_sound(sound, sound)
            sound_loop = card_template.hasAttribute("sound-loop")
            new_card = Card(
                name,
                template=template,
                auto_advance=auto_advance,
                transition=transition,
                background=background,
                background_repeat=background_repeat,
                sound=sound,
                sound_loop=sound_loop,
            )

            buttons = card_template.content.querySelectorAll(
                "button[transition]"
            )
            for button in buttons:
                next_card_name = button.getAttribute("transition")
                if next_card_name:
                    transitions.append(
                        self._create_dom_event_transition(
                            name, next_card_name, "click", button.id
                        )
                    )
                    new_card.register_transition("click", button.id)

            cards.append(new_card)

        self.machine.transitions.extend(transitions)

        return cards

    def _resolve_card(self, card_reference):
        """
        Given a card reference, that could be either a string containing the
        card's name, or a card object, returns the correct card instance if
        the card is in the app's stack.

        Otherwise, raises a `ValueError`.
        """
        if isinstance(card_reference, str):
            # The card reference is a string containing the name of the card,
            if card_reference in self.stack:
                return self.stack[card_reference]
            raise ValueError(
                f"The card '{card_reference}' does not exist in the stack."
            )
        elif isinstance(card_reference, Card):
            if card_reference.name in self.stack:
                return card_reference
            raise ValueError(
                "The card '{card_reference.name}' is not in the stack."
            )
        else:
            raise ValueError("Invalid card reference.", card_reference)

    def show_card(self, card):
        """
        Show the referenced card into the DOM via `self.placeholder`.
        """
        card.show()
        # Ensure the background is [re]set.
        background = ""
        if card.background:
            if CSS.supports("color", card.background):
                # It's a background colour.
                background = f"background-color: {card.background};"
            else:
                # Assume it's a URL to a background image.
                if card.background_repeat:
                    # Tiled
                    background = (
                        f"background-image: url('{card.background}');"
                        "background-repeat: repeat;"
                    )
                else:
                    # Filled
                    background = (
                        f"background-image: url('{card.background}');"
                        "background-size: cover;"
                        "background-repeat: no-repeat;"
                        "background-position: center;"
                    )
        self.set_background(background)
        if not self.placeholder.querySelector(f"#{card.name}"):
            self.placeholder.appendChild(card.content)

        autofocus = card.content.querySelector("[autofocus]")
        if autofocus:
            autofocus.focus()

        if card.sound:
            self.play_sound(card.sound, card.sound_loop)

    def hide_card(self, card):
        """
        Hide the specified card.
        """
        card.hide()

    def add_card(self, card):
        """
        Add a card to the stack.
        """
        if card.name in self.stack:
            raise ValueError(
                f"A card with the name '{card.name}' already exists."
            )
        card.register_app(self)
        self.stack[card.name] = card

        # Create and add a state machine state for the card along with any
        # appropriate transitions (e.g. auto-advance etc.).
        state, transitions = self._create_card_state(card)
        self.machine.add_state(state, transitions)

    def get_next_card(self, card):
        """
        Get the next card sequentially in the card list.

        Returns `None` if 'card' is the last card.
        """

        cards = list(self.stack.values())

        index = cards.index(card)
        if index == len(cards) - 1:
            return None

        next_card = cards[index + 1]

        return next_card

    def remove_card(self, card_reference):
        """
        Remove a card from the stack.

        The reference to the card can be an instance of the card itself, or
        a string containing the card's `name`.
        """
        card = self._resolve_card(card_reference)
        del self.stack[card.name]

        # TODO: remove the card state and transitions from the app's state
        # machine.

    def add_sound(self, name, url):
        """
        Add a named Audio object to the application, to play the sound file
        found at the given URL.

        **NOTE** The URL is NOT a reference to a file on the PyScript
        filesystem, but a file accessible to the browser via an HTTP request.
        """
        if name in self.sounds:
            raise ValueError(f"A sound with the name '{name}' already exists.")
        self.sounds[name] = Audio.new(url)

    def get_sound(self, name):
        """
        Get the sound referenced by the given name.

        If the name doesn't reference a sound, a ValueError is raised.
        """
        if name in self.sounds:
            return self.sounds[name]
        else:
            raise ValueError(f"A sound with the name '{name}' does not exist.")

    def remove_sound(self, name):
        """
        Remove the Audio object referenced by the given name.
        """
        if name in self.sounds:
            del self.sounds[name]

    def play_sound(self, name, loop=False):
        """
        Play the sound, added to self with the given name. If
        the sound was paused with the `keep_place` flag set to `True`, the
        sound will resume playing from the place at which it was paused.
        Otherwise, the sound will play from the start.

        If `loop` is `True` the sound will keep repeating until paused or
        removed from the application.
        """
        sound = self.get_sound(name)
        sound.loop = loop
        if sound.currentTime > 0:
            self.pause_sound(name)
        sound.play()

    def pause_sound(self, name, keep_place=False):
        """
        If the sound, added to self with the given name, is
        playing, pause it. If `keep_place` is `True` the sound will pause at
        its current location. Otherwise, should the sound be played again, it
        will play from the start.

        """
        sound = self.get_sound(name)
        sound.pause()
        if not keep_place:
            sound.currentTime = 0

    def set_background(self, background=""):
        """
        Set the body tag's background style attribute to the given value. If
        no value is given, resets it to blank.
        """
        document.body.style = background

    def transition(self, from_card_name, dom_event_name, id=None, query=None):
        """
        A decorator to create transitions for DOM events within the specified
        card.

        This just adds a transition to the app's state machine.
        """

        def wrapper(fn):
            self.machine.transitions.append(
                self._create_dom_event_transition(
                    from_card_name, fn, dom_event_name, id
                )
            )

            # App level transition.
            if from_card_name == "*":

                def handler(evt):
                    self.machine.next(
                        {"event": dom_event_name, "dom_event": evt}
                    )

                handler_proxy = ffi.create_proxy(handler)
                document.addEventListener(dom_event_name, handler_proxy)

            # Card-level transition.
            else:
                from_card = self._resolve_card(from_card_name)
                from_card.register_transition(dom_event_name, id)

        return wrapper

    def start(self, card_reference=None):
        """
        Start the app with the referenced card.

        The reference to the card can be an instance of the card itself, or
        a string containing the card's `name`.
        """

        if self.started:
            raise RuntimeError("The application has already started.")

        if card_reference:
            card_name = self._resolve_card(card_reference).name

        else:
            card_name = (
                None  # Machine will default to the first card in the list.
            )

        self.machine.start(card_name)
        self.started = True

    def dump(self):
        """
        TODO: Dump a tree (JSON) representation of the app.
        """
        pass

    def load(self, tree):
        """
        TODO: Load a tree (JSON) representation of the app.
        """
        pass

    def _create_auto_advance_transition(self, from_card):
        """
        Create a transition that accepts a timeout and advances to another
        card.
        """

        def acceptor(machine, input_):
            """
            Accepts a timeout event on the card.
            """

            if (
                input_.get("event") == "timeout"
                and input_.get("card").name == from_card.name
            ):
                # Timers are removed when a state is exited, but just in case
                # there is a timing issue, we make sure the machine is still
                # on the card that timed out.
                if machine.state_name == from_card.name:
                    return True

            return False

        def target(machine, input_):
            """
            Returns the name of the card to transition to.

            This uses the card's "transition" attribute which can be either:

            - a function with two arguments (card , datastore) that returns a
              string which is the name of card to transition to.

            - a string which is the name of the card to transition to.
            """

            return self._get_to_card_name(
                from_card, from_card.transition, input_
            )

        return Transition(
            source=from_card.name, acceptor=acceptor, target=target
        )

    def _create_dom_event_transition(
        self, from_card_name, fn_or_to_card_name, dom_event_name, element_id
    ):
        """
        Create a transition triggered by a DOM event.
        """

        def acceptor(machine, input_):
            """
            Accepts a DOM event with the specified name.

            If an element id is specified then only accept if the element was
            the DOM event target.
            """

            if input_.get("event") != dom_event_name:
                return False

            if element_id is not None:
                if input_.get("dom_event").target.id != element_id:
                    return False

            return True

        def target(machine, input_):
            """
            Return the name of the card to transition to.
            """

            if from_card_name == "*":
                from_card = self._resolve_card(self.machine.current_state.name)

            else:
                from_card = self._resolve_card(from_card_name)

            return self._get_to_card_name(
                from_card, fn_or_to_card_name, input_
            )

        return Transition(
            source=from_card_name, acceptor=acceptor, target=target
        )

    def _create_card_state(self, card):
        """
        Create a state machine state for the specified card.

        Returns a `tuple` in the form (State, [Transition])
        """

        state = State(
            name=card.name,
            on_enter=[lambda machine: self.show_card(card)],
            on_exit=[lambda machine: self.hide_card(card)],
        )

        transitions = []
        if card.auto_advance is not None:
            transitions.append(self._create_auto_advance_transition(card))

        return state, transitions

    def _get_to_card_name(self, from_card, fn_or_to_card_name, input_):
        """
        Get the name of the card to transition *to*.
        """

        # If we have a callable transition then, err, call it!
        if callable(fn_or_to_card_name):
            # The arguments to pass to the callable transition.
            args = [self, from_card]

            # If the transition was triggered by a DOM event then the event can
            # (optionally) be passed into the transition depending on the
            # signature of the user's function.
            dom_event = input_.get("dom_event")
            if dom_event:
                signature = inspect.signature(fn_or_to_card_name)
                if len(signature.parameters) > 2:
                    args.append(dom_event)

            to_card_or_name = fn_or_to_card_name(*args)

        # Otherwise the transition is just the name of the card to transition
        # to.
        else:
            to_card_or_name = fn_or_to_card_name

        # No transition.
        if not to_card_or_name:
            return ""

        if isinstance(to_card_or_name, str):
            to_card_name = to_card_or_name

        else:
            to_card_name = to_card_or_name.name

        if to_card_or_name == "-":
            card_list = list(self.stack.values())
            if card_list.index(from_card) > 0:
                to_card_name = self.machine.history_pop_previous()

            else:
                to_card_name = ""

        elif to_card_name == "+":
            card_list = list(self.stack.values())
            if card_list.index(from_card) < len(card_list) - 1:
                to_card_name = self.get_next_card(from_card).name

            else:
                to_card_name = ""

        return to_card_name
