

import invent
from invent.ui import *

from overlords import ask_the_overlords


# Datastore ##################################################################


invent.datastore["filenames"] = []
invent.datastore["summary"] = ""


# Code #######################################################################


def list_of_filenames(filenames):
    if filenames:
        result = "Files: " + ', '.join(filenames)

    else:
        result = "Files: Upload all of the files you want to summarize..."

    return result


def on_summarize(message):
    ...
    print("summarize!!!!!")
    invent.datastore["summary"] = ask_the_overlords("where is Paris?")


def on_data_changed(message):
    print("on_data_changed:", message)


invent.subscribe(on_data_changed, to_channel="store-data", when_subject="filenames")
invent.subscribe(on_summarize, to_channel="summarize", when_subject="press")


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
                    purpose="SUCCESS",
                    channel="summarize"
                ),
                TextBox(
                    text=from_datastore("summary"),
                )
            ],
        ),
    ],
)


# GO! ########################################################################

invent.go()

