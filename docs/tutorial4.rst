Using Forms and Python
----------------------

While it's nice to click buttons in an adventure game to work your way through
the story, most applications need more powerful and flexible means of capturing
user input. These usually involve forms which can contain various different
types of input.

PyperCard has a very simple form mechanism that allows you to specify just one
input type per card.

In addition, you don't need to use JSON to specify your cards (although this is
often convenient for applications that don't use forms). It's possible to
specify cards using Python and define how to handle the user input and other
changes in the application's state by creating simple functions.

Defining a card in Python is very simple::

    from pypercard import CardApp, Card

    hello_card = Card(
        title="hello",
        text="Hello",
        text_color="green",
        buttons=[{"label": "Finish", target: "goodbye"}]
        )

    goodbye_card = Card(
        title="goodbye",
        text="Goodbye",
        text_color="red",
        buttons=[{"label": "Start again", target: "hello"}]
        )

Note how the buttons are defined as Python dictionaries.

Adding cards to an app is as simple as putting them into a Python list and
passing them into the application::

    stack = [hello_card, goodbye_card, ] 
    app = CardApp(stack=stack)
    app.run()

There are some further attributes which PyperCard cards can have which have not
been mentioned so far. They are:

* ``text_size`` - the size of the text. Expressed as a number. If not given,
  defaults to ``48``.
* ``form`` - the type of input to display on the card (see below). If not
  given, no form input is displayed.
* ``options`` - options which define the form input's behaviour (see below).
  Ignored if no ``form`` attribute is given.
* ``auto_advance`` - a number (e.g. ``3.5``) to indicate the number of seconds
  to wait before automatically transitioning to a target card. If not given,
  the card won't automatically transition. You must supply a valid
  ``auto_target`` attribute, or the card will appear paused.
* ``auto_target`` - a string identifying the target card to automatically
  transition to after ``auto_advance`` seconds.

In addition to the required ``label`` and ``target`` attributes, buttons may
also have the following optional attributes:

* ``text_size`` - the size of the text in the button's label. Expressed as a
  number. If not given defaults to ``24``.
* ``text_color`` - the colour of the text in the button's label (e.g.
  ``"red"``). If not given, defaults to ``"white"``.
* ``background_color`` - the colour of the button's background (e.g.
  ``"blue"``). If not given, defaults to ``"grey"``.

Form Inputs
+++++++++++

Function follows Form
+++++++++++++++++++++

Always Check User Input!
++++++++++++++++++++++++

Back to :doc:`tutorial3`. Continue to :doc:`tutorial5`.
