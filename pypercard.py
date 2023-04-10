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
import json
from pyodide import ffi
from js import document, localStorage, CSS, clearTimeout, setTimeout, Audio, fetch


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


class Card:
    """
    Represents a card in the application. A card defines what is presented to
    the user.

    The app ensures that only one card is ever displayed at once. Each card
    has a `name` and an html `template` that defines how it looks on the page.

    Cards may also have optional `auto_advance` and `transition`
    attributes for transitioning to a target card after a given period of time.

    Cards are rendered from the `template` by the `render` method, that returns
    an HTML element for the app to insert into the DOM.

    Bespoke behaviour for rendering can be defined by the user. This should
    be passed in as the optional `on_render` argument when initialising the
    card. It will be called, at the end of the card's `render` function, but
    before the element to insert into the DOM is returned to the app. The
    `on_render` function is called with the same arguments as a transition
    function: current card, and datastore.

    The `hide` method cleans up the rendered HTML element, which the parent app
    will eventually remove from the DOM.

    It's also possible to use the `register_transition` method to register a
    user defined function to handle events dispatched by elements found in the
    card's HTML. These transition the app to new cards.

    The convenience functions called `get_by_id`, `get_element` and
    `get_elements` return individual or groups of matching HTML elements
    rendered by this card, given a valid id or CSS selector (comments attached
    to the functions explain the specific behaviours).

    Audio capabilities can be accessed via every card's `play_sound` and
    `pause_sound` methods. The sounds to be played must be referenced by the
    app (see the App class documentation for how this works).

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
        on_render=None,
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

        The `on_render` function is called just after the card is rendered, but
        before it is added to the DOM. It should take `card` and `datastore`
        arguments (just like transitions) and be used for customising the
        rendered card.

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
                self.transition = lambda card, datastore: transition
            elif callable(transition):
                self.transition = transition
            else:
                raise TypeError(
                    "The transition must be either a string or function."
                )
        # Pre-fetch/cache background image.
        if self.background and not CSS.supports("color", self.background):
            fetch(self.background)
        self.on_render = on_render
        self._transitions = []  # To hold transitions acting on the card.
        self.content = None  # Will reference the rendered element in the DOM.
        self.app = None  # Will reference the parent application.

    def register_app(self, app):
        """
        Add a reference to the hosting app, of which this card is a part.
        """
        self.app = app

    def render(self, datastore):
        """
        Renders this card into a container `pyper-card` element that is
        returned to the parent app to insert into the DOM.

        Ensures the template is `.format`-ed with the datastore dictionary (so
        named custom values can be inserted into the template).

        Rebinds any user defined transitions to the newly rendered elements
        created by the card.
        """

        # Create the rendered element if it doesn't already exist.
        if not self.content:
            self.content = document.createElement("pyper-card")
        html = self.template.format(**datastore)
        self.content.innerHTML = html

        # Add DOM event listeners for any transitions added via "app.transition".
        for transition in self._transitions:
            target_elements = self.get_elements(transition["selector"])
            # TODO: Closure in for loop!
            for element in target_elements:
                def handler(evt):
                    self.app.machine.next(
                        {"event": transition["event_name"], "dom_event": evt}
                    )

                handler_proxy = ffi.create_proxy(handler)
                transition["handler"] = handler_proxy

                element.addEventListener(
                    transition["event_name"], transition["handler"]
                )

        # And finally... show the card content!
        self.content.style.display = "block"

        # Ensure user-supplied on_render is called.
        if self.on_render:
            self.on_render(self, datastore)
        return self.content

    def hide(self):
        """Hide the card (i.e. make it invisible to the user!).

        This leaves the card in the DOM but just sets 'display' to None, and removes
        any DOM event listeners.

        """

        self.content.style.display = "none"

        # Remove any DOM event listeners that were hooked up when the card was
        # shown.
        for transition in self._transitions:
            target_elements = self.get_elements(transition["selector"])
            for element in target_elements:
                element.removeEventListener(
                    transition["event_name"], transition["handler"]
                )

    def register_transition(self, element_id, event_name):
        """
        `element_id` - the unique ID identifying the target element.
        `event_name` - e.g. "click"
        """

        self._transitions.append(
            {
                "selector": "#" + element_id,
                "event_name": event_name,
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

    def play_sound(self, name, loop=False):
        """
        Play the sound, added to the self.app object with the given name. If
        the sound was paused with the `keep_place` flag set to `True`, the
        sound will resume playing from the place at which it was paused.
        Otherwise, the sound will play from the start.

        If `loop` is `True` the sound will keep repeating until paused or
        removed from the application.
        """
        sound = self.app.get_sound(name)
        sound.loop = loop
        if sound.currentTime > 0:
            self.pause_sound(name)
        sound.play()

    def pause_sound(self, name, keep_place=False):
        """
        If the sound, added to the self.app object with the given name, is
        playing, pause it. If `keep_place` is `True` the sound will pause at
        its current location. Otherwise, should the sound be played again, it
        will play from the start.

        """
        sound = self.app.get_sound(name)
        sound.pause()
        if not keep_place:
            sound.currentTime = 0


class App:
    """
    Represents a HyperCard-ish application.

    This encapsulates the state (as a `DataStore`), stack of `Card` instances,
    and registering transitions. Furthermore, it's possible to dump and load a
    declarative `JSON` representation of the application.

    If no default arguments given, the app will assume sensible defaults.
    """

    def __init__(
        self,
        name=None,
        datastore=None,
        card_list=None,
        sounds=None,
    ):
        """
        Initialise a PyperCard app.

        If no `name` is given, the page's `title` value is used, otherwise the
        given `name` becomes the page `title`.

        The `datastore` is an optional pre-populated `DataStore` instance.

        The `card_list` is an optional list of `Card` instances with which to
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
        self.sounds = {}

        transitions = []
        if not card_list:
            card_list, transitions = self._harvest_cards_from_dom()

        if not card_list:
            raise RuntimeError("Cannot find cards for application.")

        for card in card_list:
            self.add_card(card)

        # Create the app's finite state machine.
        self.machine = self._create_app_state_machine(transitions)

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

        # Any active card timers.
        self._card_timers = {}

    def _harvest_cards_from_dom(self):
        """
        Harvest any cards defined in the DOM.

        This queries the DOM for all 'template' tags and uses their attributes to
        configure card.

        Returns:
            A (possibly empty) list of the Card instances.

        """

        cards = []
        transitions =[]
        for card_template in document.querySelectorAll("template"):
            name = card_template.id
            template = card_template.innerHTML
            auto_advance = card_template.getAttribute("auto-advance")
            if auto_advance:
                auto_advance = float(auto_advance)
            transition = card_template.getAttribute("transition")
            background = card_template.getAttribute("background")
            background_repeat = card_template.getAttribute(
                "background-repeat"
            )
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
                        self._create_app_transition(
                            next_card_name, name, button.id, "click"
                        )
                    )
                    new_card.register_transition(button.id, "click")

            cards.append(new_card)

        return cards, transitions

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

    def render_card(self, card):
        """
        Renders the referenced card into the DOM via `self.placeholder`.
        """

        card.render(self.datastore)

        if card.auto_advance is not None:
            def on_timeout():
                """Called when the card timer has timed-out!"""

                self.machine.next({"event": "timeout", "card": card})

            # Python sleeps in seconds, JavaScript in milliseconds :)
            self._card_timers[card.name] = setTimeout(
                ffi.create_proxy(on_timeout), int(card.auto_advance * 1000)
            )

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
            card.play_sound(card.sound, card.sound_loop)

    def hide_card(self, card):
        """Hide the specified card."""

        timer = self._card_timers.get(card.name)
        if timer:
            clearTimeout(timer)

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

    def remove_card(self, card_reference):
        """
        Remove a card from the stack.

        The reference to the card can be an instance of the card itself, or
        a string containing the card's `name`.
        """
        card = self._resolve_card(card_reference)
        del self.stack[card.name]

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

    def set_background(self, background=""):
        """
        Set the body tag's background style attribute to the given value. If
        no value is given, resets it to blank.
        """
        document.body.style = background

    def transition(self, from_card_name, element_id, event_name):
        """A decorator to create transitions for an event within the specified card.

        This just adds a transition to the app's state machine.

        """

        from_card = self._resolve_card(from_card_name)

        def wrapper(fn):
            self.machine.transitions.append(
                self._create_app_transition(fn, from_card_name, element_id, event_name)
            )

            from_card.register_transition(element_id, event_name)

        return wrapper

    def start(self, card_reference):
        """
        Start the app with the referenced card.

        The reference to the card can be an instance of the card itself, or
        a string containing the card's `name`.
        """
        if self.started:
            raise RuntimeError("The application has already started.")

        self.machine.start()
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

    # Internal #########################################################################

    def _create_app_state_machine(self, transitions=None, state_name=None, history=None, context=None):
        """Create a simple finite state machine ("machine" for short!) for the app."""

        states = []
        transitions = transitions or []
        for card in self.stack.values():
            card_state, card_transitions = self._create_card_state(card)
            states.append(card_state)
            transitions.extend(card_transitions)

        machine = Machine(
            model=self,
            states=states,
            transitions=transitions,
            state_name=state_name or states[0].name,
            history=history,
            context=context
        )

        return machine

    def _create_app_transition(self, fn_or_card_name, from_card_name, element_id, event_name):
        """Create a transition specified via the "app.transition" decorator."""

        def acceptor(machine, input_):
            if input_.get("event") != event_name:
                return False

            if element_id is not None and input_.get("dom_event").target.id != element_id:
                return False

            return True

        def target(machine, _input):
            """This function is called to get the state to transition to.

            If the transition function returns...

            - either an empty string or None, the machine stays in the current state.
            - a non-empty string, the machine moves to the state with that name.
            - a Card instance, the machine moves to the state with the card's name.

            """

            # The card that we are (potentially) transitioning from.
            from_card = self._resolve_card(from_card_name)

            # Call the transition function and see where we are headed to.
            if callable(fn_or_card_name):
                to_state_or_card = fn_or_card_name(from_card, self.datastore)

            else:
                to_state_or_card = fn_or_card_name

            if isinstance(to_state_or_card, str):
                to_state = to_state_or_card

            else:
                to_state = to_state_or_card.name

            if to_state == "<previous>":
                to_state = machine.history_pop_previous()

            return to_state

        return Transition(source=from_card_name, acceptor=acceptor, target=target)

    def _create_card_state(self, card):
        """Create a state machine state for the specified card.

        Returns:
            a tuple in the form (State, [Transition])

        """

        state = State(
            name=card.name,
            on_enter=[lambda machine: self.render_card(card)],
            on_exit=[lambda machine: self.hide_card(card)]
        )

        transitions = []
        if card.auto_advance is not None:
            transitions.append(self._create_auto_advance_transition(card))

        return state, transitions

    def _create_auto_advance_transition(self, card):
        """Create a transition that accepts a timeout and advances to the next card."""

        def acceptor(machine, input_):
            if input_.get("event") == "timeout" and input_.get("card").name == card.name:
                # Timers are removed when a state is exited, but just in case there is a
                # timing issue, we make sure the machine is still on the card that timed
                # out.
                if machine.state_name == card.name:
                    return True

            return False

        def target(machine, input_):
            return card.transition(card, card.app.datastore)

        return Transition(source=card.name, target=target, acceptor=acceptor)


# A simple Finite State Machine (FSM) implementation ###################################


class Machine:
    """ A simple Finite State Machine (FSM) implementation. """

    def __init__(
            self, model, states=None, transitions=None, state_name='', history=None,
            context=None
    ):
        """ Constructor. """

        # For convenience, we allow each state to be passed as either:-
        #
        # a) A State instance.
        # b) A tuple of constructor arguments for the State class.
        self.states = [
            state if isinstance(state, State) else State(*state)

            for state in states or []
        ]

        # For convenience, we allow each transition to be passed as either:-
        #
        # a) A Transition instance.
        # b) A tuple of constructor arguments for the Transition class.
        self.transitions = [
            transition if isinstance(transition, Transition) else Transition(*transition)

            for transition in transitions or []
        ]

        self.model = model
        self.state_name = state_name or self.states[0].name
        self.history = history or []
        self.context = context or {}

        # Make it quicker to lookup states by name :)
        self._states_by_name = {state.name: state for state in self.states}

    @property
    def current_state(self):
        """Return the current state."""

        return self._states_by_name[self.state_name]

    @property
    def is_done(self):
        """ Return True iff there are no transitions out of the current state.

        The machine inherently has no notion of success or failure - it only
        knows whether there is any possible way out of the current state. The state
        machine writer can add meaning to the 'done' states with naming conventions
        and/or state subclasses etc.

        """

        return not any([
            (transition.source == self.state_name or transition.source == '*')

            for transition in self.transitions
        ])

    def goto(self, state_name, run_hooks=True):
        """ Goto a specific state.

        This calls any on exit hooks on the current state and any on enter hooks on
        the target state.

        """

        state = self._states_by_name.get(state_name)
        if state is None:
            raise ValueError(f'No such state: {state}')

        # Exit the current state...
        if run_hooks:
            self._exit_state(state)

        # ... and enter the new one.
        self.state_name = state_name
        if run_hooks:
            self._enter_state(self.current_state)

        return state_name

    def next(self, input_):
        """ Attempt to transition from the current state with the given input.

        Return either:-

        1) the name of the state we transitioned to.
        2) an empty string if a transition accepted the input but didn't move state.
        3) null if no transition accepted the input.

        """

        if self.is_done:
            self.pprint()
            raise ValueError(f'Machine is already done but got input: {input_}')

        for transition in self.transitions:
            if transition.source == '*' or transition.source == self.state_name:
                # We use the first transition that accepts the input.
                if transition.acceptor.accepts(self, input_):
                    return self._do_transition(transition, input_)

        # No transition handled the input.
        # print('No transition handled input:', input_)
        return ''

    def history_pop_previous(self):
        """ Return the name of the previous state in the history.

        This pops the current and previous states from the history ready for the
        transition to the previous state (where the previous state will get added to the
        history).

        TODO: This only works if this method is called from a transition...

        """

        if len(self.history) < 2:
            raise ValueError(f"No previous state: {self.history}")

        # Remove the current state from the history...
        self.history.pop()

        # Remove the previous state we are going back to from the history too as it
        # gets added again when we go there.
        return self.history.pop()

    def run(self, *inputs):
        """ Call 'next' for all the specified inputs.

        Primarily useful for testing/playing with your state machine!

        """

        for input_ in inputs:
            self.next(input_)

    def start(self):
        """ Start the machine. """

        self._enter_state(self.current_state)

    # For manual debugging ####################################################

    def pprint(self, indent=''):
        """ Pretty-print the object. """

        print(
            f'{indent}{type(self).__name__}({self.model}, {self.state_name}, {self.context})')

        indent += '  '
        for state in self.states:
            state.pprint(indent)

        for transition in self.transitions:
            transition.pprint(indent)

    # Internal #########################################################################

    def _do_transition(self, transition, input_):
        """Do the specified transition!"""

        # Transitions can add to the context... we do it here in case any of the
        # transition hooks want to use the value.
        if transition.context_object_name:
            self.context[
                transition.context_object_name] = transition.get_context_object(self,
                                                                                input_)

        # Pre-transition hooks.
        transition.call_before_hooks(self, input_)

        # Where are we heading next? :)
        next_state_name = transition.get_target(self, input_)

        # A transition can accept the input but NOT move to another state by returning
        # an empty string (this is our cheap and cheerful solution to handle incorrect
        # answers in quizzes etc.).
        #
        # We allow either an empty string or None to mean "no transition".
        if next_state_name:
            # Exit the current state...
            self._exit_state(self.current_state)

            # ... and enter the new one.
            self.state_name = next_state_name
            self._enter_state(self.current_state)

        # Post-transition hooks.
        transition.call_after_hooks(self, input_)

        return next_state_name

    def _enter_state(self, state):
        """ Enter the specified state. """

        state.call_on_enter_hooks(self)
        self.history.append(state.name)

    def _exit_state(self, state):
        """ Exit the specified state. """

        state.call_on_exit_hooks(self)


class State:
    """ A state in a state machine :) """

    def __init__(self, name, on_enter=None, on_exit=None):
        """ Constructor."""

        self.name = name
        self.on_enter = on_enter or []
        self.on_exit = on_exit or []

    def pprint(self, indent=''):
        """ Pretty-print the object. """

        print(
            f'{indent}{type(self).__name__}("{self.name}", on_enter={self.on_enter}, on_exit={self.on_exit})')

    # TODO: async?
    def call_on_enter_hooks(self, machine):
        """ Call all on_enter hooks. """

        for hook in self.on_enter:
            hook(machine)

    # TODO: async?
    def call_on_exit_hooks(self, machine):
        """ Call all on_exit hooks. """

        for hook in self.on_exit:
            hook(machine)


class Transition:
    """ A possible transition from one state to another. """

    def __init__(self, source, acceptor, target=None, context_object_name='',
                 before=None, after=None):
        """ Constructor.

        If 'source' is the string '*' then it is a possible transition from
        *any* state.

        """

        self.source = source
        self.acceptor = acceptor if isinstance(acceptor, Acceptor) else Acceptor(
            acceptor)
        self.target = target
        self.context_object_name = context_object_name
        self.before = before or []
        self.after = after or []

    def pprint(self, indent=''):
        """ Pretty-print the object. """

        print(
            f'{indent}{type(self).__name__}("{self.source}", {self.acceptor}, "{self.target}", "{self.context_object_name}", before={self.before}, after={self.after})')

    def get_context_object(self, machine, input_):
        """ Return the object to add to the machine's context iff this transition succeeds.

        By default, we delegate this to the acceptor since state machine
        builders usually build acceptors, not transitions.

        """

        return self.acceptor.get_context_object(machine, input_)

    def get_target(self, machine, input_):
        """ Get the target state name. """

        if callable(self.target):
            return self.target(machine, input_)

        return self.target

    # TODO: async?
    def call_before_hooks(self, machine, input_):
        """ Call any before hooks. """

        for hook in self.before:
            hook(machine, input_)

    # TODO: async?
    def call_after_hooks(self, machine, input_):
        """ Call any before hooks. """

        for hook in self.after:
            hook(machine, input_)


class Acceptor:
    """ Acceptors determine whether the received input is allowed."""

    def __init__(self, fn=None):
        """ Constructor. """

        self.fn = fn

    def __str__(self):
        """ Pretty-print the object. """

        return f'{type(self).__name__}({self.fn.__name__ if self.fn is not None else ""})'

    def accepts(self, machine, input_):
        """ Return True iff the specified input is accepted.

        If no function 'fn' is specified this defaults to returning true (i.e.
        it accepts *everything* :) ).

        """

        # If the 'fn' attribute is set call that. This allows to us to
        # implement acceptors without the need for subclassing.
        if self.fn is not None:
            return self.fn(machine, input_)

        return True

    def get_context_object(self, machine, input_):
        """ Return the object to add to the machine's context iff this acceptor accepts! """

        return input_
