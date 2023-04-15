"""
A mysterious Myst like game to demonstrate some of the more creative uses of
PyperCard.
"""
from pypercard import App, DataStore
import random


app = App()

if "open" not in app.datastore:
    app.datastore.update(
        {
            # Default game state flags.
            "open": False,
            "inscription": False,
            "encounter": False,
            "locked": True,
            "red_book": False,
            "instructions": False,
        }.items()
    )


@app.transition("hello", "click", "submit")
def hello(app, card):
    name = card.get_by_id("name").value.strip()
    if name:
        app.datastore["name"] = name
        return "intro1"
    return "nameerror"


app.start("hello")
