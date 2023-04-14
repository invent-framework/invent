"""
A simple PyperCard example of using a form to get a user's name, and then
display a friendly "Hello world!" type message.
"""
from pypercard import App, Card


# The templates for these cards can be found in index.html.
cards = [
    Card("get_name"),
    Card("say_hello"),
]


hello_app = App(name="Hello world, PyperCard style", cards=cards)


@hello_app.transition("get_name", "click", "submit")
def hello(app, card):
    app.datastore["name"] = card.get_by_id("name").value
    return "say_hello"


@hello_app.transition("say_hello", "click", "again")
def again(app, card):
    return "get_name"


hello_app.start("get_name")
