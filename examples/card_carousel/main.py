"""
This simple app demonstrates how cards can automatically advance to another
card after a certain amount of time. The auto_advance can either be a string
containing the name of the next card, or a function to call that returns the
name of the next card.
"""
from pypercard import App, Card


def auto_func(app, card):
    """
    Called while transitioning from card 2, to card 3.
    """
    count = app.datastore.setdefault("counter", 0)
    count += 1
    app.datastore["counter"] = count
    return "card3"


# The templates for these cards can be found in index.html.
cards = [
    Card("card1", auto_advance=10, transition="card2"),
    Card("card2", auto_advance=20, transition=auto_func),
    Card("card3", auto_advance=5, transition="card1"),
]


# Create the app while ensuring the counter is reset.
carousel_app = App(
    name="PyperCard carousel", datastore={"counter": 0}, cards=cards
)


@carousel_app.transition("card2", "click", "reset")
def reset(app, card):
    return "card1"


carousel_app.start("card1")
