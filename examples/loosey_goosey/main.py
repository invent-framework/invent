"""
The simplest possible app. It says, "Hello, World!".
"""
from pypercard import App, Card

honk_app = App(
    name="Loosey Goosey.",
    card_list=[Card("goose_card"),],
    sounds={"honk": "honk.mp3", },
)


@honk_app.transition("goose_card", "honk", "click")
def honk(card, datastore):
    card.play_sound("honk")


honk_app.start("goose_card")
