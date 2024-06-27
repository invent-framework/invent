"""
Example application that uses a Task to get cat facts.
"""

import pyscript
import invent
import asyncio
from invent.ui import *
from invent import tasks
from invent import utils

URL = "https://catfact.ninja/fact"


# Datastore ###################################################################

invent.datastore["cat_fact"] = ""
invent.datastore["working"] = False


# Code ########################################################################


def handle_cat_fact(value):
    if value:
        utils.play_sound(invent.media.sounds.meow.mp3)
        return value["fact"]
    return value


def ready(value):
    return not value


# Channels ####################################################################


invent.subscribe(
    invent.Task(
        tasks.fetch,
        key="cat_fact",
        indicator="working",
        url=URL,
    ),
    to_channel="get_cat_facts",
    when_subject=["press"],
)


# User Interface ##############################################################


app = App(
    name="CatFacts!",
    content=[
        Page(
            name="Facts",
            content=[
                Column(
                    content=[
                        Image(
                            image=invent.media.images.puff.svg,
                            visible=from_datastore("working"),
                            align_self="center",
                        ),
                        Button(
                            name="cat_fact_button",
                            label="Get Facts",
                            channel="get_cat_facts",
                            purpose="SUCCESS",
                            enabled=from_datastore(
                                "working", with_function=ready
                            ),
                        ),
                        TextBox(
                            name="a_cat_fact",
                            text=from_datastore(
                                "cat_fact", with_function=handle_cat_fact
                            ),
                            align_self="center",
                        ),
                    ]
                ),
            ],
        ),
    ],
)


# GO! #########################################################################


invent.go()
