"""
PyperCard

A simple HyperCard inspired framework for PyScript, implemented as a finite
state machine for building graphical apps in Python.

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
from js import document, localStorage, setTimeout


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
        behaviour.
        """
        raise NotImplementedError

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

    Cards may also have optional `auto_advance` and `auto_advance_after`
    attributes for transitioning to another card after a given period of time.

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

    Finally, the convenience functions called `get_by_id`, `get_element` and
    `get_elements` return individual or groups of matching HTML elements
    rendered by this card, given a valid id or CSS selector (comments attached
    to the functions explain the specific behaviours).
    """

    def __init__(
        self,
        name,
        template=None,
        on_render=None,
        auto_advance=None,
        auto_advance_after=None,
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

        The `auto_advance` can be either a string containing the name of the
        card to which to automatically transition, or a transition function to
        call that returns a string containing the name of the next card.

        The `auto_advance_after` is the number of seconds, as a `float` or
        `int`, to wait until the `auto_advance` is evaluated to discern the
        next card to which to automatically transition.

        Either both `auto_advance` and `auto_advance_after` need to be given,
        or both need to be `None`. Otherwise, the card will raise a
        `ValueError`. If the `auto_advance` is not a string or function or the
        `auto_advance_after` is not an integer or float, a `TypeError` will be
        raised.
        """
        self.name = name
        self.auto_advance = None
        self.auto_advance_after = None
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
        # Check auto_* values are a pair: either both truth-y or both false-y.
        if bool(auto_advance) != bool(auto_advance_after):
            raise ValueError(
                "Both auto_advance AND auto_advance_after are required."
            )
        # Auto advance setup / validation.
        if auto_advance:
            if isinstance(auto_advance, str):
                self.auto_advance = lambda c, d: auto_advance
            elif callable(auto_advance):
                self.auto_advance = auto_advance
            else:
                raise TypeError(
                    "The auto_advance must be either a string or function."
                )
        if auto_advance_after:
            if isinstance(auto_advance_after, float) or isinstance(
                auto_advance_after, int
            ):
                # Python counts time in seconds (that may be floats to indicate
                # fractions-of-a-second, or integers).
                self.auto_advance_after = float(auto_advance_after)
            else:
                raise TypeError(
                    "Please use a number of seconds for auto_advance_after."
                )
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


class App:
    """
    Represents a HyperCard-ish application.

    This encapsulates the state (as a `DataStore`), stack of `Card` instances,
    and registering transitions. Furthermore, it's possible to dump and load a
    declaritive `JSON` representation of the application.

    If no default arguments given, the app will assume sensible defaults.
    """

    def __init__(
        self, name="My PyperCard App", datastore=None, card_list=None
    ):
        """
        Initialise a PyperCard app with a given `name` (used as the page's
        `title`).

        The `datastore` is an optional pre-populated `DataStore` instance.

        The `card_list` is an optional list of `Card` instances with which to
        initialise.
        """
        self.started = False
        self.name = name
        self.datastore = datastore if datastore else DataStore()
        self.stack = {}
        if card_list:
            for card in card_list:
                self.add_card(card)
        # Update the page title to the name of the app.
        document.querySelector("title").innerText = self.name
        # Create the element into which the app will appear.
        self.placeholder = document.createElement("pyper-app")
        document.body.appendChild(self.placeholder)

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
                    next_card = card.auto_advance(card, self.datastore)
                    if next_card:
                        new_card = self._resolve_card(next_card)
                        card.hide()
                        self.render_card(new_card)

            timeout_handler = ffi.create_proxy(wrapper)
            # Python sleeps in seconds, JavaScript in milliseconds.
            setTimeout(timeout_handler, int(card.auto_advance_after * 1000))
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
