"""
A mysterious Myst like game to demonstrate some of the more creative uses of
PyperCard.
"""
from pypercard import App, Card
import random


# The templates for these cards can be found in index.html.
cards = [
    Card("get_name"),
    Card("say_hello"),
]


app = App()


@app.transition("get_name", "submit", "click")
def hello(card, datastore):
    datastore["name"] = card.get_by_id("name").value
    return "say_hello"


@app.transition("say_hello", "again", "click")
def again(card, datastore):
    return "get_name"


app.start("get_name")
