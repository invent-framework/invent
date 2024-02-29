import invent
from pyscript import window


# Datastore ############################################################################


invent.datastore.setdefault("number_of_honks", 0)
invent.datastore.setdefault("number_of_oinks", 0)


# Code #################################################################################


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

    # Add a piggy...
    from invent.ui.core import Component
    piggies = Component.get_component_by_id("piggies")
    piggies.append(invent.ui.TextBox(text="🐖"))


def move_page(message):
    if message.button == "to_goose":
        invent.show_page("Honk")
    elif message.button == "to_pig":
        invent.show_page("Oink")


# Channels #############################################################################


invent.subscribe(make_honk, to_channel="honk", when_subject=["press", "touch"])
invent.subscribe(make_oink, to_channel="oink", when_subject=["press", "touch"])
invent.subscribe(
    move_page,
    to_channel="navigate",
    when_subject=[
        "press",
    ],
)


# User Interface #######################################################################


invent.ui.App(
    name="Farmyard",
    content=[
        invent.ui.Page(
            name="Honk",
            content=[
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
                                    name="to_pig",
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
                    ]
                )
            ],
        ),
        invent.ui.Page(
            name="Oink",
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
                                    name="to_goose",
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
                            id="piggies",
                            position="CENTER",
                            content=[
                            ],
                        ),
                    ]
                )
            ],
        ),
    ],
)


# GO! ##################################################################################


invent.go()
