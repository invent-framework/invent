A Simple Adventure Game
-----------------------

The idea for PyperCard is the brainchild of the wonderfully creative and
playful folks at `Adafruit <https://adafruit.com/>`_. In order to make a 
game for one of their new line of `CircuitPython <https://circuitpython.org/>`_
boards (which comes with a
`touch screen <https://www.adafruit.com/product/4116>`_), they had to work out
what sort of game could work on the device and then figure out how to implement
it. They describe the process in a
`wonderful blog post <https://learn.adafruit.com/circuit-python-your-own-adventure/overview>`_
that channels all things 1980s.

Warlocks
++++++++

.. image:: warlock.jpg 

Back then (I was a child in the 1980s), there was a craze for "choose your own
adventure" books, the most famous being the "fighting fantasy" series of books
with the "Warlock of Firetop Mountain" being the first of many installments.

Instead of starting at page one and reading each page in order until
the end of the book, "choose your own" books generally contained numbered
entries that often ended with a choice for the reader. Depending
on the choice taken, the reader would be directed to read some other entry
identified by its number. The following picture illustrates the a typical page
from such a book:

.. image:: warlock_page.jpg

Another creation from the 1980s is a piece of software called
`HyperCard <https://en.wikipedia.org/wiki/HyperCard>`_. This is where the
original ideas of a stack, card and transition comes from. It was a sort of
pre-cursor to the world wide web but was a LOT easier to develop. The
HyperCard paradigm, updated for use with the Python programming language is why
this project is called "PyperCard".

.. image:: hypercard.jpg

I mentioned in a previous tutorial that once you understood the HyperCard
concepts of stacks, cards and transitions, you'll start to see such things all
over the place. Well, this is a classic example: "choose your own" stories are
stacks containing cards (one for each numbered entry in the story) and the
choices given to readers act as the transitions.

Let's build a "choose your own" adventure game with PyperCard!

Strange Maps
++++++++++++

The folks at Adafruit planned their game with a map of the story. Just like
the story-board mentioned in an earlier tutorial, different cards are linked
together with arrows to show how the transitions take place between the
different parts of the story. Each card is scant on detail and doesn't say what
the text for each part of the story will be, but the names of the cards
give enough information to show how the game fits together and fits into the
stack, card, transition paradigm.

.. image:: gaming_cave_adventure.jpg 

Each card needs attributes that PyperCard can use to display something useful
to the player and react to the various choices the player might make. As a
result PyperCard lets programmers define individual cards with specific named
attributes which are used for clearly defined purposes. The attributes we'll
use with each card in the adventure game are listed below:

* ``title`` - the unique title for a card. This is something all cards must
  have and it must be a string, such as ``"home"`` or ``"cave entrance"``.
* ``text`` - a string containing text to display to the user. We'll use this to
  hold the text of the story. If this attribute isn't given, PyperCard won't
  display any textual output.
* ``text_color`` - the colour of the text. This can be one of three sorts of
  string: 1) A colour name (like ``"red"``), 2) A hex number representing RGB
  (e.g. ``"0xff0000"``), 3) An HTML hex colour (e.g. ``"#FF0000"``). If this
  attribute isn't given, PyperCard will assume ``"white"``.
* ``background`` - an image or colour to display in the background of the card,
  behind the text. This is a string containing either a colour name (e.g.
  ``"red"``) or the image's filename. If this attribute isn't given, PyperCard
  will assume ``"black"``.
* ``sound`` - a sound to play when the user transitions to the card. This is a
  string containing the filename for the sound. If this attribute isn't given,
  PyperCard won't play a sound.
* ``sound_repeat`` - a boolean value (``True`` or ``False``) to indicate if the
  sound for the card should keep looping. This attribute will only work if a
  ``sound`` attribute is also provided.
* ``buttons`` - a list of buttons used to indicate the available choices. Each
  button must have a ``label`` (the text to display on the button) and a
  ``target`` (the ``title`` of the card to which the button should transition).

With a stack of cards with just these few attributes we can build our adventure
game. In order to do so, we need to tell PyperCard about each of the cards in
the stack.
  
Meet JSON
+++++++++

JSON (you say it, "Jason", like the name of the Greek hero), is a
data-interchange format that's easy for humans to read and write while also
being easy for programs to consume and emit.

Put another way, it's a way to write data (and our data contains cards with
the attributes listed above). JSON is also very common and used in all sorts of
different situations, so learning it is going to be very useful.

JSON works by grouping related attributes together between curly brackets (i.e.
``{`` and ``}``). Such related attributes are called objects. Attributes have a
name and associated value separated by a colon (``:``). The name is always a
string of characters and the associated value can be a string, number, boolean,
array or an object. Attributes are separated by a comma (``,``). Groups of
objects can be stored in an array, which is a comma separated list enclosed in
square brackets (i.e. ``[`` and ``]``).

Here's an example of a JSON object containing some attributes::

    {
        "name": "PyperCard",
        "version": "0.0.1-alpha.1",
        "downloads": 1728394,
        "author": "Nicholas H.Tollervey",
    }

Can you work out what this JSON object represents?

The trick is to look at the names and values of the attributes and figure out
what they represent (in this case, it's details about the PyperCard project).

Here's how to represent a PyperCard card as a JSON object::

    {
        "title": "start",
        "text": "Welcome. Your adventure begins, as many do, in Ye Olde Inn.",
        "text_color": "0x000001",
        "background": "page01.bmp",
        "buttons": [
            {
                "label": "Continue",
                "target": "inn"
            }
        ]
    }

The card's unique title is ``"start"`` and, since this is a card in our
adventure game stack, the text is ``"Welcome. Your adventure begins, as many
do, in Ye Olde Inn."``. The text can be anything we want, it just so happens
that we're creating an adventure game, so the text for the card reflects the
sort of textual content found in "choose your own" adventures. Most of the
other attributes should make sense, but I want to draw your attention to the
value of the ``"buttons"`` attribute: it's an array (remember, starting and
ending with square brackets, ``[`` and ``]``) containing another JSON object
to represent a single button. The button object contains two attributes, one
for the button's label and the other providing the title of the card to
transition to when the button is pressed. As we'll see in a moment, there may
be more than one button associated with a card (see the next JSON example).

In order to create a stack of cards in JSON, we need to put the JSON objects
representing the PyperCard cards into an array that represents the stack. We
do it like this (note the opening and closing ``[`` and ``]``)::

    [
        {
            "title": "start",
            "background": "page01.bmp",
            "text": "Welcome. Your adventure begins, as many do, in Ye Olde Inn.",
            "text_color": "0x000001",
            "buttons": [
                {
                    "label": "Continue",
                    "target": "inn"
                }
            ]
        },
        {
            "title": "inn",
            "background": "page01.bmp",
            "sound": "pub.wav",
            "sound_repeat": true,
            "text": "This is a peaceful, happy inn with plentiful drink.",
            "text_color": "0x000001",
            "buttons": [ 
                {
                    "label": "Stay",
                    "target": "inn"
                },
                {
                    "label": "Go!",
                    "target": "cave entrance"
                }
            ]
        },

        ... a whole bunch of many more card objects go here ...

        {
            "title": "die",
            "background": "page01.bmp",
            "sound": "scream.wav",
            "text": "The bridge gives way and you fall to a painful death.",
            "text_color": "0x000001",
            "buttons": [
                {
                    "label": "Next",
                    "target": "inn"
                }
            ]
        }
    ]

.. note::
    
    The line ``"... a whole bunch of many more card objects go here ..."``
    isn't actually part of the JSON, but just a way for me to truncate the
    example.

.. warning::

    Observe how the ``target`` attributes of buttons contain the value
    associated with the ``title`` attributes of other objects. If there is a
    mismatch here, the application won't work! This is why it is so important
    that card ``title`` attributes are unique -- PyperCard needs to be able to
    unambiguously identify them.

If the JSON data is saved as a file (for example, ``cyoa.json`` -- for "choose
your own adventure"), then it's very easy to get PyperCard to load this file
and run the game (making sure all the sounds and images used in the game are
in the same directory as the following Python script)::

    from pypercard import CardApp

    app = CardApp("Adventure Game")
    app.load("cyoa.json")
    app.run()

That's it! The full JSON file is part of the `PyperCard examples <https://github.com/ntoll/pypercard/blob/master/examples/adafruit_adventure/cyoa.json>`_,
along with all the `necessary sound effects and images <https://github.com/ntoll/pypercard/tree/master/examples/adafruit_adventure>`_.

For the sake of convenience, we've
`zipped it up for easy download <_static/adventure.zip>`_.

Why not try to modify and change the JSON file to create your own "choose your
own" adveture. Change the text, sounds and background images used. Experiment
with several choices for a more complicated game.

Sadly, the only thing missing is gathering user input. For that we need to
learn how to use forms...

Back to :doc:`tutorial2`. Continue to :doc:`tutorial4`.
