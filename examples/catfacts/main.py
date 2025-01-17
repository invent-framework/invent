"""
Example application that gets random cat facts via the net.
"""

import random
import invent
from invent.ui import *
from invent.tools import net, sound
from invent import App
from invent.ui import Page, Column, Button, Label, Image


# The URL to get cat facts from.
URL = "https://catfact.ninja/fact"


MEOWS = [  # Meow sounds.
    invent.media.sounds.meow1.mp3,
    invent.media.sounds.meow2.mp3,
    invent.media.sounds.meow3.mp3,
    invent.media.sounds.meow4.mp3,
    invent.media.sounds.meow5.mp3,
]


# Datastore ###################################################################


await invent.setup(
    cat_fact="", working=False
)  # Load default values for the datastore.


# Code ########################################################################


def get_cat_fact(message):
    """
    Get a cat fact from the URL. Put the result in the datastore under the
    key "cat_fact".
    """
    invent.datastore["working"] = True
    net.request(url=URL, json=True, result_key="cat_fact")


def handle_cat_fact(value):
    """
    Play a meow sound and return the cat fact.
    """
    if value:
        sound.play(random.choice(MEOWS))
        invent.datastore["working"] = False
        return value["fact"]
    return value


def ready(value):
    """
    Flip the ready status of the button.
    """
    return not value


# Channels ####################################################################


invent.subscribe(  # Press the button to get a cat fact.
    get_cat_fact,
    to_channel="get_cat_facts",
    when_subject=["press"],
)


# User Interface ##############################################################


app = App(
    name="🐱 Cat Facts!",
    pages=[
        Page(
            name="Facts",
            children=[
                Column(
                    children=[
                        Image(
                            image=invent.media.images.puff.svg,
                            visible=from_datastore("working"),
                            horizontal_align="center",
                        ),
                        Button(
                            name="cat_fact_button",
                            text="Get 🐱 Facts",
                            channel="get_cat_facts",
                            purpose="SUCCESS",
                            enabled=from_datastore(
                                "working", with_function=ready
                            ),
                        ),
                        Label(
                            name="a_cat_fact",
                            text=from_datastore(
                                "cat_fact", with_function=handle_cat_fact
                            ),
                            horizontal_align="center",
                        ),
                    ]
                ),
            ],
        ),
    ],
)


# GO! #########################################################################


invent.go()
