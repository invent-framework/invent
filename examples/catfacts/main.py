"""
Example application that uses a Task to get cat facts.
"""

import invent
from invent.ui import *
from invent import net
from invent import utils
from invent import App, Page

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
    net.send_web_request(url=URL, key="cat_fact"),
    to_channel="get_cat_facts",
    when_subject=["press"],
)


# User Interface ##############################################################


app = App(
    name="CatFacts!",
    pages=[
        Page(
            name="Facts",
            children=[
                Column(
                    children=[
                        Image(
                            image=invent.media.images.puff.svg,
                            visible=from_datastore("working"),
                            layout=dict(align_self="center"),
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
                        Label(
                            name="a_cat_fact",
                            text=from_datastore(
                                "cat_fact", with_function=handle_cat_fact
                            ),
                            layout=dict(align_self="center"),
                        ),
                    ]
                ),
            ],
        ),
    ],
)


# GO! #########################################################################


invent.go()
