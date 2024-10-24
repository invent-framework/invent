import invent
from invent.ui import export
from invent.ui import *


# Datastore ############################################################################


# invent.datastore.setdefault("number_of_honks", 0)
# invent.datastore.setdefault("number_of_oinks", 0)

invent.datastore["number_of_honks"] = 0
invent.datastore["number_of_oinks"] = 0


# Code #################################################################################


def navigate(message):
    if message.button.name == "to_lucy":
        invent.show_page("Lucy")
    elif message.button.name == "to_percy":
        invent.show_page("Percy")
    elif message.button.name == "to_code":
        invent.show_page("Code")


def make_honk(message):
    invent.datastore["number_of_honks"] = (
        invent.datastore["number_of_honks"] + 1
    )
    invent.play_sound(invent.media.sounds.honk.mp3)


def make_oink(message):
    invent.datastore["number_of_oinks"] = (
        invent.datastore["number_of_oinks"] + 1
    )
    invent.play_sound(invent.media.sounds.oink.mp3)


def make_geese(number_of_honks):
    return [TextBox(text="🪿") for _ in range(number_of_honks)]


def make_pigs(number_of_oinks):
    return [TextBox(text="🐖") for _ in range(number_of_oinks)]


# Channels #############################################################################


invent.subscribe(navigate, to_channel="navigate", when_subject=["press"])
invent.subscribe(make_honk, to_channel="honk", when_subject=["press", "touch"])
invent.subscribe(make_oink, to_channel="oink", when_subject=["press", "touch"])


# User Interface #######################################################################


app = App(
    name="Farmyard!",
    pages=[
        Page(
            name="Lucy",
            children=[
                Column(
                    children=[
                        Image(
                            image=invent.media.images.goose.png,
                            channel="honk",
                            layout=dict(align_self="center"),
                        ),
                        Row(
                            layout=dict(align_self="center"),
                            children=[
                                Button(
                                    name="button honk",
                                    label="HONK!",
                                    channel="honk",
                                ),
                                Button(
                                    name="to_percy",
                                    label="Visit Percy",
                                    channel="navigate",
                                ),
                            ],
                        ),
                        Row(
                            children=[
                                TextBox(
                                    name="number_of_honks",
                                    text=from_datastore("number_of_honks"),
                                    layout=dict(align_self="center"),
                                ),
                                Slider(
                                    value=from_datastore("number_of_honks"),
                                    name="Honk Slider",
                                    step=1,
                                    layout=dict(flex=1),
                                ),
                            ]
                        ),
                        Row(
                            id="geese",
                            justify_content="center",
                            children=from_datastore(
                                "number_of_honks", with_function=make_geese
                            ),
                        ),
                        Button(
                            name="to_code",
                            label="Show Code",
                            channel="navigate",
                        ),
                    ]
                ),
            ],
        ),
        Page(
            name="Percy",
            children=[
                Column(
                    children=[
                        Image(
                            image=invent.media.images.pig.png,
                            channel="oink",
                            layout=dict(align_self="center"),
                        ),
                        Row(
                            layout=dict(align_self="center"),
                            children=[
                                Button(
                                    name="button oink",
                                    label="OINK!!",
                                    channel="oink",
                                ),
                                Button(
                                    name="to_lucy",
                                    label="Visit Lucy",
                                    channel="navigate",
                                ),
                                TextBox(
                                    name="number_of_oinks",
                                    text=from_datastore("number_of_oinks"),
                                    layout=dict(align_self="center"),
                                ),
                            ],
                        ),
                        Row(
                            id="pigs",
                            justify_content="center",
                            children=from_datastore(
                                "number_of_oinks", with_function=make_pigs
                            ),
                        ),
                        Button(
                            name="to_code",
                            label="Show Code",
                            channel="navigate",
                        ),
                    ],
                ),
            ],
        ),
    ],
)


# Add a page that shows the code! ######################################################


app.pages.append(
    Page(
        name="Code",
        children=[
            Row(
                children=[
                    Button(
                        name="to_lucy",
                        label="Visit Lucy",
                        channel="navigate",
                        layout=dict(flex=1),
                    ),
                    Button(
                        name="to_percy",
                        label="Visit Percy",
                        channel="navigate",
                        layout=dict(flex=1),
                    ),
                ]
            ),
            Code(code=export.as_pyscript_app(app)[1]),
        ],
    )
)


# GO! ##################################################################################


invent.go()
