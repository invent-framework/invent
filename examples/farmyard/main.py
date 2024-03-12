import invent
from invent.ui import export


# Datastore ############################################################################


#invent.datastore.setdefault("number_of_honks", 0)
#invent.datastore.setdefault("number_of_oinks", 0)

invent.datastore["number_of_honks"] = 0
invent.datastore["number_of_oinks"] = 0


# Code #################################################################################


def navigate(message):
    if message.button == "to_lucy":
        invent.show_page("Lucy")
    elif message.button == "to_percy":
        invent.show_page("Percy")
    elif message.button == "to_code":
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
    return [invent.ui.TextBox(text="🪿") for _ in range(number_of_honks)]


def make_pigs(number_of_oinks):
    return [invent.ui.TextBox(text="🐖") for _ in range(number_of_oinks)]


# Channels #############################################################################


invent.subscribe(navigate, to_channel="navigate", when_subject=["press"])
invent.subscribe(make_honk, to_channel="honk", when_subject=["press", "touch"])
invent.subscribe(make_oink, to_channel="oink", when_subject=["press", "touch"])


# User Interface #######################################################################


app = invent.ui.App(
    name="Farmyard",
    content=[
        invent.ui.Page(
            name="Lucy",
            content=[
                invent.ui.Slider(
                    value=invent.ui.from_datastore("number_of_honks"),
                    name='Honk Slider',
                    position='FILL',
                    step=1,
                ),
                invent.ui.Column(
                    content=[
                        invent.ui.Image(
                            image=invent.media.images.goose.png,
                            channel="honk",
                            position="MIDDLE-CENTER",
                        ),
                        invent.ui.Row(
                            position="CENTER",
                            content=[
                                invent.ui.Button(
                                    name="button honk",
                                    label="HONK!",
                                    channel="honk",
                                    position="FILL",
                                ),
                                invent.ui.Button(
                                    name="to_percy",
                                    label="Visit Percy",
                                    channel="navigate",
                                    position="FILL",
                                ),
                                invent.ui.TextBox(
                                    name="number_of_honks",
                                    text=invent.ui.from_datastore(
                                        "number_of_honks"
                                    ),
                                    position="MIDDLE-CENTER",
                                ),
                            ],
                        ),
                        invent.ui.Row(
                            id="geese",
                            position="CENTER",
                            content=invent.ui.from_datastore(
                                "number_of_honks", with_function=make_geese
                            ),
                        ),
                        invent.ui.Button(
                            name="to_code",
                            label="Show Code",
                            channel="navigate",
                            position="FILL",
                        ),
                    ]
                )
            ],
        ),
        invent.ui.Page(
            name="Percy",
            content=[
                invent.ui.Column(
                    content=[
                        invent.ui.Image(
                            image=invent.media.images.pig.png,
                            channel="oink",
                            position="MIDDLE-CENTER",
                        ),
                        invent.ui.Row(
                            position="CENTER",
                            content=[
                                invent.ui.Button(
                                    name="button oink",
                                    label="OINK!!",
                                    channel="oink",
                                ),
                                invent.ui.Button(
                                    name="to_lucy",
                                    label="Visit Lucy",
                                    channel="navigate",
                                    position="FILL",
                                ),
                                invent.ui.TextBox(
                                    name="number_of_oinks",
                                    text=invent.ui.from_datastore(
                                        "number_of_oinks"
                                    ),
                                    position="MIDDLE-CENTER",
                                ),
                            ],
                        ),
                        invent.ui.Row(
                            id="pigs",
                            position="CENTER",
                            content=invent.ui.from_datastore(
                                "number_of_oinks", with_function=make_pigs
                            ),
                        ),
                        invent.ui.Button(
                            name="to_code",
                            label="Show Code",
                            channel="navigate",
                            position="FILL",
                        ),
                    ],
                ),
            ],
        ),
    ],
)


# Add a page that shows the code! ######################################################


app.content.append(
    invent.ui.Page(
        name="Code",
        content=[
            invent.ui.Row(
                content=[
                    invent.ui.Button(
                        name="to_lucy",
                        label="Visit Lucy",
                        channel="navigate",
                        position="FILL",
                    ),
                    invent.ui.Button(
                        name="to_percy",
                        label="Visit Percy",
                        channel="navigate",
                        position="FILL",
                    ),
                ]
            ),
            invent.ui.Code(code=export.as_pyscript_app(app)[0]),
        ],
    )
)


# GO! ##################################################################################


invent.go()
