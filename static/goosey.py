import invent
from invent.ui import Button, Image


# User interface
honk_app = invent.App(
    name="Loosey Goosey",
    content = [
        invent.Page(
            name="Honk",
            content = [
                invent.ui.Image(
                    "/static/goose.png",
                    channel="honk"
                ),
                invent.ui.Button(
                    name="button go",
                    label="HONK!",
                    channel="honk"
                )
            ],
        ),
    ],
)


# Handlers (stacks of blocks)
def make_honk(message):
    invent.play_sound("/static/honk.mp3")  # invent.media.sounds.honk.mp3)


# Pubsub (???)
invent.pubsub.subscribe(make_honk, to_channel="honk", when=["press", "touch"])


# GO!
honk_app.go()
