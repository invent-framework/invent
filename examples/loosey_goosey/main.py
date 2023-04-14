"""
Honking as a service.
"""
from pypercard import App, Card

honk_app = App(
    name="Loosey Goosey.",
    cards=[
        Card("goose_card"),
    ],
    sounds={
        "honk": "honk.mp3",
    },
)


@honk_app.transition("goose_card", "click")
def honk(app, card):
    app.play_sound("honk")


honk_app.start("goose_card")
