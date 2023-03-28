"""
A simple PyperCard example of using a form to get a user's name, and then
display a friendly "Hello world!" type message.
"""
from pypercard import App, Card


cards = [
    Card(
        "get_name",
        """
<label for="name">Enter your name: </label>
<input id="name" type="text" autofocus/>
<button id="submit">Hello</button>
""",
    ),
    Card(
        "say_hello",
        """
<h1>Hello {name}!</h1>
<button id="again" autofocus>Again</button>
""",
    ),
]

hello_app = App(name="Hello world, PyperCard style", card_list=cards)


@hello_app.transition("get_name", "submit", "click")
def hello(card, datastore):
    datastore["name"] = card.get_by_id("name").value
    return "say_hello"


@hello_app.transition("say_hello", "again", "click")
def again(card, datastore):
    return "get_name"


hello_app.start("get_name")
