"""Summarizer demo."""


import asyncio

import invent
from invent.ui import *

from overlords import ask_the_overlords
from utils import get_file_by_name, read_file


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


async def read_files(filenames):
    return [
        await read_file(get_file_by_name(filename))

        for filename in filenames or []
    ]


async def summarize():
    content = await read_files(invent.datastore["filenames"])
    summary = ask_the_overlords(context="\n\n".join(content))

    invent.datastore["summary"] = summary

    print("summarize: done", summary)
    return summary


def on_summarize(message):
    """Summarize the text files."""

    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(summarize(), loop)


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

