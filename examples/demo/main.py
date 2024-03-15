

import invent
from invent.ui import *


# Datastore ##################################################################


invent.datastore["filenames"] = []
invent.datastore["result"] = ""


# Code #######################################################################


def list_of_filenames(filenames):
    return "Files: " + ', '.join(filenames)


def on_data_changed(message):
    print("on_data_changed:", message)


invent.subscribe(on_data_changed, to_channel="store-data", when_subject=["filenames"])


# User Interface #############################################################


App(
    name='Summarizer',
    content=[
        Page(
            name='Page 1',
            content=[
                FileUpload(
                    files=from_datastore("filenames")
                ),
                TextBox(
                    text=from_datastore("filenames", with_function=list_of_filenames)
                ),
                Button(
                    label="Summarize",
                    purpose="SUCCESS"
                ),
                TextBox(
                    text=from_datastore("result"),
                )
            ],
        ),
    ],
)


# GO! ########################################################################

invent.go()

