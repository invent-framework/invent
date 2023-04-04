"""
Honking as a service.
"""
from pypercard import App, Card

honk_app = App(
    name="Loosey Goosey.",
    card_list=[
        Card("goose_card"),
    ],
    sounds={
        "honk": "honk.mp3",
    },
)


@honk_app.transition("goose_card", "honk", "click")
def honk_button(card, datastore):
    card.play_sound("honk")


@honk_app.transition("goose_card", "goose", "click")
def honk_picture(card, datastore):
    card.play_sound("honk")


honk_app.start("goose_card")
