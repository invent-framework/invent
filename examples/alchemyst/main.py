"""
A mysterious Myst like game to demonstrate some of the more creative uses of
PyperCard.
"""
from pypercard import App, Card
import random


app = App()


@app.transition("hello", "submit", "click")
def hello(card, datastore):
    datastore["name"] = card.get_by_id("name").value
    return "intro1"


app.start("hello")
