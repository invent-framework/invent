"""
Example application that uses a Task to get cat facts.
"""

import random
import invent
from invent.ui import *
from invent.tools import net, sound
from invent import App
from invent.ui import Page, Column, Button, Label, Image

URL = "https://catfact.ninja/fact"

MEOWS = [
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
    invent.datastore["working"] = True
    net.request(url=URL, json=True, result_key="cat_fact")


def handle_cat_fact(value):
    if value:
        sound.play(random.choice(MEOWS))
        invent.datastore["working"] = False
        return value["fact"]
    return value


def ready(value):
    return not value


# Channels ####################################################################


invent.subscribe(
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
