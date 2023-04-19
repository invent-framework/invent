# Cheatsheet

PyperCard is an easy and simple GUI framework with a focus on beginner Python
programmers. This page contains all the technical information you need in one
place. You should use it for reference purposes. If you’d like to learn more
about PyperCard please consult the [tutorials](tutorials.md).

```{contents}
:depth: 2
```

## Installation

PyperCard runs on top of [PyScript](https://pyscript.net/) - a browser based
Python platform.

The quickest way to get going is via a free (but limited) account at
[PyScript.com](https://pyscript.com/):

* Create a new project.
* Update the project's `pyscript.toml` file so `pypercard` is listed as a
  dependency:

```toml
packages = ["pypercard", ]
```

* Create your app and define transitions, via Python, in the `main.py` file.
* The `index.html` file can be used to define how your cards look via several
  hidden `template` elements.

Alternatively, just look at the
[example projects](https://github.com/pyscript/pypercard/tree/main/examples)
to see how to organise an app.

## Core concepts

PyperCard's core concepts are:

* An app contains a _stack of cards_.
* A card _represents a screen_ in your app.
* A transition allows users to _move between cards in a meaninful way_.

If the app is the global context, then each card fulfils a specific role or
function within the application. Cards define what the user sees at any given
time.

When a transition is activated (for example, because a user has clicked a
button), functions containing business logic are called, state is changed via 
the app's key/value datastore (more on this below) and the next card is
indicated.

## The App

The `App` class represents a card based application.

This object encapsulates state (as a key/value `DataStore` instance), a stack
of `Card` instances, and registering transitions.

The app's `datastore` is a shim around the browser's `localStorage` expressed
as a Python `dict`. Sometimes, because of the browser's security policy, it's
not possible to get access to `localStorage` and so a standard Python `dict` is
used instead (although, as a result, state is not preserved between page
reloads).

For an app to work, it needs a stack of cards and some transitions. Each card
has a name, unique within the application context. A list of `Card` instances
can be passed in when the app is instantiated, or cards can be added later, on
the fly. If no cards are passed in at instantiation, the app will query the DOM
for `template` elements, whose attributes and content it will use to create its
stack.

Transitions are simply decorated Python functions that will be called with the
instance of the app, and the `Card` instance representing the card that
generated the event that fired the decorated transition function.

Other app-wide functions (such as playing or pausing sounds) are methods of
this class. To add your own app-wide functions, create a sub-class of this one.

Once created, start the app with a given card, or else the app starts with the
very first card added to its stack.

The application is rendered into the DOM via a `pyper-app` element.

## A Card

A `Card` instance defines what is presented to the user. The app ensures only
one card is displayed at any time.

Every card has a `name` that is unique within the current application, and a
`template` that can either be a string passed in at instantiation time or else
the card will look for a `template` tag in the DOM with an `id` that matches
the card's name, and whose content and attributes will define how the card
looks and behaves.

Cards may also have optional `auto_advance` and `transition` attributes for
transitioning to a target card after a given period of time.

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

The convenience functions called `get_by_id`, `get_element` and
`get_elements` return individual or groups of matching HTML elements
rendered by this card, given a valid id or CSS selector (comments attached
to the functions explain the specific behaviours).

Cards can optionally define the nature of their background, via the
`background` and `background_repeat` attributes. The `background` should
either be a valid CSS `color` or a URL to an image. If the `background` is
an image, the `background_repeat` flag will indicate if the image will
fill the whole screen or repeat in a tiled fashion (the default is to
fill the whole screen).

The attributes of a `template` element in the DOM will map directly to the
attributes of the related `Card` instance. Thus, `background`, `auto-advance`
and other HTMLElement attributes set the equivalent methods on the instance.

A further convenience includes detecting a `transition` attribute on an HTML
`button` element within the card's template. If, when the card is visible to
the user, the button is clicked, it will automatically transition to the name
of the card given as the value of the `transition` attribute.

## Transitions

Transitions are simply Python functions that react to events, and tell the
app what to do next.

If a transition returns a string, and the string contains the name of a card in
the app's stack, the app will hide the current card and display the card
referenced in the result of the function. If the transition function returns a
`None` the app will keep the current card on the screen.

A transition function always takes the same arguments, a reference to the
current app (so you have access to getting/setting state or other capabilities
provided by the `App` class), and the `Card` instance that dispatched the
event. You can, optionally, retrieve the event object created by the browser
that represents activity that resulted in the function call.

To define a transition function you need to use a decorator provided by your
app.

```python
my_app = App()

@my_app.transition("my_card", "click", "button_id")
def my_transition(app, card, event):
    """
    A decorated transition function for the "my_card" card.

    When the HTML element with the `id` "button_id" is "click"-ed then the
    function will be called.
    """
    ... do business logic here...
    return "next_card"
```

This just adds a transition to the app's underlying state machine.

The first argument can be either a string of the name of the target card, or a
list of target card names.

The second argument is the name of the event, as dispatched by the
browser, e.g. "click".

The third argument is the unique `id` attribute of the target element within
the referenced card[s], that will dispatch the event.

Finally, you can replace the `id` argument with a named `query` argument, as a
way to provide a valid CSS query to match elements within the referenced
card[s], that will dispatch the event.

## DataStore

Every app has a `datastore`, an object that behaves like a Python `dict` for
storing app state.

Usually, this is a Pythonic shim around the browser's `localStorage` object.
However, sometimes due to the browser's security context, the `localStorage`
object is not available. In this case, a regular Python `dict` is used, but
with the disadvantage that state isn't retained between page reloads.

For more information about the characteristics of the `localStorage` object
please
[read this documentation](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API).


## Other Stuff

The PyperCard framework is very much "early stage" and alpha quality, despite
such a lot having already been written.

More coming soon.
