Design Decisions
================

Design decisions are logged on this page for future developers and other
interested parties to learn how some of the features ended up being implemented
(as well as to give context to the decisions). Each design decision should have
a descriptive main header under which should be three further sections starting
with sub-headings: "Decision", "Background" and "Discussion and
Implementation". The design decisions are listed in date order (oldest first).

The decision section should precisely and fully describe the technical outcome
relating to the feature. The background section should include any context
setting and reference technical details and/or constraints pertinent to the
decision. The discussion and implementation section should describe the
decision making process and, if helpful contain two further subsections:
"Implemented via" (to contain links to GitHub pull requests and/or commits) and
"Discussion in" (to reference significant / important discussion happening in
related issues, bug reports or code reviews).

If in doubt, just follow the conventions found within the already documented
design decisions.

.. contents::
    :depth: 2

JSON Stacks
-----------

Decision
++++++++

Use declarative JSON files for simple applications which require no business
logic expressed in transition functions.

The JSON file must contain an array of JSON objects. Each object represents a
card in the application's stack.

Attributes of the JSON objects must match the names of the arguments used when
instantiating the Python ``Card`` class (see :doc:`api` for full details of
these arguments).

Use the ``CardApp`` class's ``load`` convenience function with the path to the
JSON file to load the stack::

    from pypercard import CardApp

    app = CardApp()
    app.load("my_stack.json")
    app.run()

Background
++++++++++

PyperCard is designed to be easy to use and understand, with special attention
paid to the needs of beginner developers.

Writing Python code can be intimidating for beginner developers. In order to
declare the UI stack of cards in Python a developers needs to instantiate
several classes, create a Python list and even write their own functions when
all they want to do is describe a very simple stack of cards.

The JSON data format is a lightweight and easy to read solution which has the
advantage of being a ubiquitous form of data exchange. Following simple naming
conventions for defining JSON objects means little effort is needed to define
a working stack for a simple app.

This also has the advantage that, at some later date, a graphical beginner
friendly tool, could be created to emit valid JSON files to make this process
even less intimidating. Nevertheless, writing JSON in a text editor is not an
onerous task and goes some way to demonstrating how simple it is to use a text
based medium for programming.

Discussion and Implementation
+++++++++++++++++++++++++++++

The inspiration for this version of PyperCard was created by Adafruit and
described in a blog post where an early version of the JSON based specification
for defining stacks of cards was outlined.

After discussion with Adafruit we agreed that I should make changes to the
original specification to simplify names and/or reorganise things to allow for
more flexibility.

The end result is what you find in the current implementation. I'm particularly
pleased that using the Python naming conventions in the JSON objects means the
implementation of the ``CardApp`` class's ``load`` method is
`extremely simple <https://github.com/ntoll/pypercard/blob/c38336dc1fada24dca1484a2f3b18e82230fa197/pypercard/core.py#L579>`_.

Implemented via:
~~~~~~~~~~~~~~~~

* https://github.com/ntoll/pypercard/commit/9cff63316374a5f81460aeb0f81ade92e26ed7fd

Discussion in:
~~~~~~~~~~~~~~

* https://learn.adafruit.com/circuit-python-your-own-adventure (original
  Adafruit blog post).
* :doc:`cheatsheet` (description of the revised [Python based] attribute names
  to use in the JSON objects).
