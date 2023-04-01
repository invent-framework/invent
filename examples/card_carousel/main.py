"""
This simple app demonstrates how cards can automatically advance to another
card after a certain amount of time. The auto_advance can either be a string
containing the name of the next card, or a function to call that returns the
name of the next card.
"""
from pypercard import App, Card


def auto_func(card, datastore):
    """
    Called while transitioning from card 2, to card 3.
    """
    count = datastore.setdefault("counter", 0)
    count += 1
    datastore["counter"] = count
    return "card3"


# The templates for these cards can be found in index.html.
cards = [
    Card("card1", auto_advance="card2", auto_advance_after=10),
    Card("card2", auto_advance=auto_func, auto_advance_after=20),
    Card("card3", auto_advance="card1", auto_advance_after=5),
]


# Create the app while ensuring the counter is reset.
carousel_app = App(
    name="PyperCard carousel", datastore={"counter": 0}, card_list=cards
)


@carousel_app.transition("card2", "reset", "click")
def reset(card, datastore):
    return "card1"


carousel_app.start("card1")
