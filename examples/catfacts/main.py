"""
Example application that uses a Task to get cat facts.
"""
import invent
from invent.ui import *

URL = "https://catfact.ninja/"


# Datastore ############################################################################

invent.datastore["catfact"] = ""

# Code #################################################################################



# Channels #############################################################################


invent.subscribe(navigate, to_channel="navigate", when_subject=["press"])
invent.subscribe(make_honk, to_channel="honk", when_subject=["press", "touch"])
invent.subscribe(make_oink, to_channel="oink", when_subject=["press", "touch"])


# User Interface #######################################################################


app = App(
    name="CatFacts!",
    content=[
        Page(
            name="Facts",
            content=[
                Column(
                    content=[
                        Image(
                            image=invent.media.images.goose.png,
                            channel="honk",
                            position="MIDDLE-CENTER",
                        ),
                        Row(
                            position="CENTER",
                            content=[
                                Button(
                                    name="button honk",
                                    label="HONK!",
                                    channel="honk",
                                    position="FILL",
                                ),
                                Button(
                                    name="to_percy",
                                    label="Visit Percy",
                                    channel="navigate",
                                    position="FILL",
                                ),
                            ],
                        ),
                        Button(
                            name="to_code",
                            label="Get Facts",
                            channel="get_cat_facts",
                            position="FILL",
                        ),
                        TextBox(
                            name="a_cat_fact",
                            text=from_datastore("cat_fact"),
                            position="MIDDLE-CENTER",
                        ),
                    ]
                ),
            ],
        ),
        Page(
            name="Percy",
            content=[
                Column(
                    content=[
                        Image(
                            image=invent.media.images.pig.png,
                            channel="oink",
                            position="MIDDLE-CENTER",
                        ),
                        Row(
                            position="CENTER",
                            content=[
                                Button(
                                    name="button oink",
                                    label="OINK!!",
                                    channel="oink",
                                ),
                                Button(
                                    name="to_lucy",
                                    label="Visit Lucy",
                                    channel="navigate",
                                    position="FILL",
                                ),
                                TextBox(
                                    name="number_of_oinks",
                                    text=from_datastore("number_of_oinks"),
                                    position="MIDDLE-CENTER",
                                ),
                            ],
                        ),
                        Row(
                            id="pigs",
                            position="CENTER",
                            content=from_datastore(
                                "number_of_oinks", with_function=make_pigs
                            ),
                        ),
                        Button(
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
    Page(
        name="Code",
        content=[
            Row(
                content=[
                    Button(
                        name="to_lucy",
                        label="Visit Lucy",
                        channel="navigate",
                        position="FILL",
                    ),
                    Button(
                        name="to_percy",
                        label="Visit Percy",
                        channel="navigate",
                        position="FILL",
                    ),
                ]
            ),
            Code(code=export.as_pyscript_app(app)[1]),
        ],
    )
)


# GO! ##################################################################################


invent.go()
