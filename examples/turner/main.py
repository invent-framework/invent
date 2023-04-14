"""
Using the background attributes of a card to display pictures by Turner to the
music of Bach.
"""
from pypercard import App, Card


# The templates for these cards can be found in index.html.
cards = [
    Card(
        "intro",
        background="#eee",
    ),
    Card(
        "burning_of_house_of_commons",
        transition="norham_castle_sunrise",
        auto_advance=10,
        background="burning_of_house_of_commons.jpg",
    ),
    Card(
        "norham_castle_sunrise",
        transition="rain_steam_speed",
        auto_advance=10,
        background="norham_castle_sunrise.jpg",
    ),
    Card(
        "rain_steam_speed",
        transition="sunrise_with_sea_monsters",
        auto_advance=10,
        background="rain_steam_speed.jpg",
    ),
    Card(
        "sunrise_with_sea_monsters",
        transition="the_shipwreck",
        auto_advance=10,
        background="sunrise_with_sea_monsters.jpg",
    ),
    Card(
        "the_shipwreck",
        transition="burning_of_house_of_commons",
        auto_advance=10,
        background="the_shipwreck.jpg",
    ),
]


turner_app = App(
    name="Turner's Paintings",
    cards=cards,
    sounds={
        "bach": "bach_cello.mp3",
    },
)


@turner_app.transition("*", "keydown")
def keydown(app, card, event):
    if event.keyCode == 39:
        return "+"

    if event.keyCode == 37:
        return "-"


@turner_app.transition("intro", "click", "start")
def start(app, card):
    app.play_sound("bach", loop=True)
    return "burning_of_house_of_commons"


turner_app.start("intro")
