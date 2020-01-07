Using Forms and Python
----------------------

While it's nice to click buttons in an adventure game to work your way through
the story, most applications need more powerful and flexible means of capturing
user input. These usually involve forms containing various different
types of input. Happily, PyperCard has a very simple form mechanism that
allows you to specify just one input type per card.

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
        buttons=[{"label": "Finish", "target": "goodbye"}]
    )

    goodbye_card = Card(
        title="goodbye",
        text="Goodbye",
        text_color="red",
        buttons=[{"label": "Start again", "target": "hello"}]
    )

Note how the buttons are defined as Python dictionaries.

Adding cards to an app is as simple as putting them into a Python list and
passing them into the application::

    stack = [hello_card, goodbye_card, ] 
    app = CardApp(stack=stack)
    app.run()

Alternatively, you can add cards individually via the application's
``add_card`` method::

    app = CardApp()
    app.add_card(hello_card)
    app.add_card(goodbye_card)
    app.run()

When a card or stack of cards are added to the application, the card titles
will be checked to ensure they are unique. If not, PyperCard will raise an
exception.

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

For an application to be useful it often needs to gather and process user
input. In PyperCard this is achieved through form input fields. Each card may
only have one form input field.

There are five possible types of input.

A single-line text box:

.. image:: textbox.png

A multi-line text entry field:

.. image:: textarea.png

A multiple choice field so users can select none, one or more of a range of
values:

.. image:: multichoice.png

A selector field so users can select a single value or no value at all from a
range of values:

.. image:: select.png

A slider for providing numeric input between a minimum and maximum value with
an option to define the step between values as the slider moves.

.. image:: slider.png

Function follows Form
+++++++++++++++++++++

You're probably asking yourself how PyperCard works with user input.

The answer is the programmer creates transition functions.

A transition is simply how a user moves between cards, usually via a button
click. A function is a named block of code that does something useful.

As you've already seen, transitions can already be defined as a string
containing the unique title attribute of the target card. A transition function
is simply a "regular" Python function that takes two expected arguments and
must return a string containing the unique title of the target card for the
transition. In this way, the transition function may be used to decide which,
of a number of options or cards, should be returned as the target. In this way
the application becomes a dynamic system.

Transition functions are used in two places:

1. As the value of the ``"target"`` attribute of a button, or;
2. As the value of a card's ``"auto_target"`` attribute.

Transition functions **must be defined before you reference them in your
code**.

In addition to working out the target card for the transition and handling user
input (dealt with below), transition functions also allow you to store and
retrieve data which may be useful for the functioning of your application. This
is often called storing "state".

Transition functions are very easy to understand:

* They take the same two arguments each time,
* They must return a string containing the ``title`` of the target card.
* The application will wait until the transition function has finished before
  actually doing anything. If your transition function takes a long time, your
  application will appear unresponsive.

The two arguments all transition functions should handle are:

* ``data_store`` - the application's "data store". This is simply a Python
  dictionary (and the same dictionary is passed into each function, so if you
  make changes to the dictionary, these will be available to subsequent
  transition functions).
* ``form_value`` - the current value of the form input field on the card from
  which the user is transitioning. This will be ``None`` if the card didn't
  contain a form input field, or an "empty" (false) value if the user didn't
  enter anything.

Transition functions should look something like this::

    def my_transition(data_store, form_value):
        # Arbitrary Python code goes here.
        return "a_card_title"

Let's imagine we want to build an application that asks the user for their name
and then says "Hello, whatever-their-name-is". If they don't enter a name the
application should report an error.

Simple..!

The first card should contain a text box entry field and instructions along
with a button that uses a transition function. The resulting transition
function should check the user's input and, if there is any, store it away
before transitioning to the card which displays the friendly greeting. If the
user doesn't enter a name, the transition function should cause the application
to transition to a temporary error card which returns them back to the card
with the name input form.

Here's how I'd write the function::

    def get_name(data_store, form_value):
        if form_value:
            data_store["username"] = form_value
            return "hello"
        else:
            return "error"

Notice how if use ``if ... else`` statements to work out which sort of card
to display. Basically, if there's user input transition to the "hello" card,
otherwise, transition to the "error" card.

Importantly, *before* transitioning store the user's input in the
``"username"`` field in the ``data_store`` dictionary, so the ``"hello"`` card
can use it within the message.

How does the ``"hello"`` card make use of the user's input? Well, if the
text to display were ``"Hello {username}"`` then PyperCard knows to replace the
bit including the curly brackets with the value stored in the record whose name
appears between the curly brackets. In this example, whatever is found in
``data_store["username"]`` replaces the bit in the text identified as
``{username}``.

So if the user enters ``"Fred"`` as the value in the input text field in the
very first card, then the value of ``data_store["username"]`` will be set to
``"Fred"``. Then, in the second card (where the friendly message is shown)
PyperCard notices we have a curly-bracket enclosed name, looks in the
``data_store`` for a value with that name and replaces it. In our case, the
``{username}`` part of the text message is replaced with ``"Fred"``, which
the transition function from the first card stored away into the
``data_store``.

The following simple example shows this all in action::

    from pypercard import Inputs, Card, CardApp


    def get_name(data_store, form_value):
        """
        Gets the name of the user from the form field and stores it in the
        data store. If no name is given, causes an error card to be displayed
        instead.
        """
        if form_value:  # Check if there's user input.
            data_store["username"] = form_value  # Store the user's input.
            return "hello"  # Transition to the "hello" card.
        else:  # No user input... :-(
            return "error"  # ...so transition to the "error" card.


    stack = [
        Card(
            "get_value",  # First card get's the user's name.
            form=Inputs.TEXTBOX,  # Contains a single text box...
            text="What is your name..?",  # ...with appropriate instructions.
            buttons=[
                # A button whose target is the "get_name" transition function.
                {"label": "OK", "target": get_name}  # Click "OK".
            ]
        ),
        Card(
            "hello",  # A card to say "Hello" to the user.
            text="Hello {username}!",  # Note the replacement of {username}.
            buttons=[
                # A simple transition back to the input form.
                {"label": "OK", "target": "get_value"}
            ]
        ),
        Card(
            "error",  # A card to display an error.
            text="ERROR\n\nPlease enter a name!",  # The error message...
            text_color="white",  # ... is white text...
            background="red",  # ... on a red background ...
            auto_advance=3,  # ... displayed for three seconds, the go to...
            auto_target="get_value"  # the input form to try again.
        ),
    ]

    app = CardApp(stack=stack)
    app.run()

The end result should look like this:

.. image:: name_app.gif

Always Check User Input!
++++++++++++++++++++++++

A final word of warning. **ALWAYS** check input provided by users.

Users have a habit of doing the wrong thing, either on purpose or because they
want to try to break your application. You should treat all user input as
suspect until you've thoroughly checked it.

For instance, in the example above, I made sure that something had been entered
by the user so the user wouldn't end up seeing the nonsensical message:
"Hello !" (note the gap where the missing name should be).

Your checks of user input can be as simple or complicated as your application
requires. But most importantly, your application must **ALWAYS** check user
input.

Don't say we didn't warn you... ;-)

Back to :doc:`tutorial3`. Continue to :doc:`tutorial5`.
