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
import functools
import json
from pyodide import ffi
from js import document, localStorage, CSS, setTimeout, Audio, fetch


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
                self.transition = lambda c, d: transition
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
        # Create the rendered element.
        self.content = document.createElement("pyper-card")
        html = self.template.format(**datastore)
        self.content.innerHTML = html
        # Attach transitions.
        for transition in self._transitions:
            target_elements = self.get_elements(transition["selector"])
            for element in target_elements:
                element.addEventListener(
                    transition["event_name"], transition["handler"]
                )
        # Ensure user-supplied on_render is called.
        if self.on_render:
            self.on_render(self, datastore)
        return self.content

    def hide(self):
        """
        Cleans up the HTML related to this card, since it will be removed from
        the DOM.
        """
        self.content = None

    def register_transition(self, element_id, event_name, handler):
        """
        `element_id` - the unique ID identifying the target element.
        `event_name` - e.g. "click"
        `handler` - the Python transition function to call when the event
        fires.

        The transition function should return the unique name of the next
        card to display. If no name is returned the app will stay on the
        current card.
        """
        handler_proxy = ffi.create_proxy(handler)
        self._transitions.append(
            {
                "selector": "#" + element_id,
                "event_name": event_name,
                "handler": handler_proxy,
            }
        )

    def get_by_id(self, element_id):
        """
        Convenence function for getting a child element by id. Returns `None`
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
    declaritive `JSON` representation of the application.

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

        If no `name` is given, the page's `title` value is used. Otherwise the
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
        self.stack = {}
        if card_list:
            for card in card_list:
                self.add_card(card)
        self.sounds = {}
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

    def _resolve_card(self, card_reference):
        """
        Given a card reference, that could be either a string containing the
        card's name, or a card object, returns the correct card instance if
        the card is in the app's stack.

        Otherwise raises a `ValueError`.
        """
        if isinstance(card_reference, str):
            # The card reference is a string containing the name of the card,
            if card_reference in self.stack:
                return self.stack[card_reference]
            raise ValueError(
                "The card '{card_reference}' does not exist in the stack."
            )
        elif isinstance(card_reference, Card):
            if card_reference.name in self.stack:
                return card_reference
            raise ValueError(
                "The card '{card_reference.name}' is not in the stack."
            )
        else:
            raise ValueError("Invalid card reference.")

    def render_card(self, card):
        """
        Renders the referenced card into the DOM via `self.placeholder`.
        """
        new_element = card.render(self.datastore)
        if card.auto_advance:
            # Start auto advance timer.

            def wrapper():
                """
                Wraps the card's `auto_advance` function. Called when the
                timeout is activated. Only calls the `auto_advance` if the card
                is still displayed (i.e. it has rendered `content`).
                """
                if card.content:
                    next_card = card.transition(card, self.datastore)
                    if next_card:
                        new_card = self._resolve_card(next_card)
                        card.hide()
                        self.render_card(new_card)

            timeout_handler = ffi.create_proxy(wrapper)
            # Python sleeps in seconds, JavaScript in milliseconds.
            setTimeout(timeout_handler, int(card.auto_advance * 1000))
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
        self.placeholder.replaceChildren(new_element)
        autofocus = new_element.querySelector("[autofocus]")
        if autofocus:
            autofocus.focus()

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

    def transition(self, from_card, element, event):
        """
        Return a function, that handles an event dispatched from within the
        referenced `from_card`.

        It ensures the event ends up calling the user's wrapped function which
        returns the `name` of the next card.

        The outer function hides the current card, and shows the next card.

        The reference to the card can be an instance of the card itself, or
        a string containing the card's `name`.
        """
        card = self._resolve_card(from_card)

        def wrapper(func):
            @functools.wraps(func)
            def inner_wrapper(event):
                next_card = func(card, self.datastore)
                if next_card:
                    new_card = self._resolve_card(next_card)
                    card.hide()
                    self.render_card(new_card)

            card.register_transition(element, event, inner_wrapper)
            return inner_wrapper

        return wrapper

    def start(self, card_reference):
        """
        Start the app with the referenced card.

        The reference to the card can be an instance of the card itself, or
        a string containing the card's `name`.
        """
        if self.started:
            raise RuntimeError("The application has already started.")
        card = self._resolve_card(card_reference)
        self.render_card(card)
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
