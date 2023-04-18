# Cheatsheet

PyperCard is an easy and simple GUI framework with a focus on beginner Python
programmers. This page contains all the technical information you need in one
place. You should use it for reference purposes. If you’d like to learn more
about PyperCard please consult the [tutorials](tutorials.md).

```{contents}
:depth: 2
```

## Installation

The quickest way to get going is via a free (but limited) account at
[PyScript.com](https://pyscript.com/):

* Create a new project.
* Update the project's `pyscript.toml` file so `pypercard` is listed as a
  dependency:

```python
packages = ["pypercard", ]
```

* Create your app and define transitions, via Python, in the `main.py` file.
* The `index.html` file can be used to define how your cards look via several
  hidden `template` elements.

You can also just do the equivalent of:

```
pip install pypercard
```

In your usual Python development environment.

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

This object encapsulates the state (as a `DataStore` instance), stack of `Card`
instances, and registering transitions.

The app's `datastore` is a shim around the browser's `localStorage` expressed
as a Python `dict`. Sometimes, because of the browser's security policy, it's
not possible to get access to `localStorage` and so a standard Python `dict` is
used instead (although, as a result, state is not preserved between page
reloads).

For an app to work, it needs a stack of cards and some transitions. Each card
has a name, unique within the application context.

Other app-wide functions (such as playing or pausing sounds) are methods of
this class. To add your own app-wide functions, create a sub-class of this one.

If no default arguments are given, the app will assume sensible defaults and 
try to discover its stack of cards from the DOM (more on this below).

Once created, start the app with a given card, or else the app starts with the
very first card added to its stack.


## A Card


## Transitions


## DataStore


## Other Stuff
