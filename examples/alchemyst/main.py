"""
A mysterious Myst like game to demonstrate some of the more creative uses of
PyperCard.
"""
from pypercard import App, Card
import random


app = App()


@app.transition("hello", "click", "submit")
def hello(card, datastore):
    name = card.get_by_id("name").value.strip()
    if name:
        datastore["name"] = name
        return "intro1"
    return "nameerror"


app.start("hello")
