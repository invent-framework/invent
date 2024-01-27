import invent
from invent.ui import Button, Image


# User interface
farmyard_app = invent.App(
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
                    name="button honk",
                    label="HONK!",
                    channel="honk"
                ),
                invent.ui.Button(
                    name="to_pig",
                    label="Visit Percy",
                    channel="navigate"
                ),
            ],
        ),
        invent.Page(
            name="Oink",
            content = [
                invent.ui.Image(
                    "/static/pig.png",
                    channel="oink"
                ),
                invent.ui.Button(
                    name="button oink",
                    label="OINK!",
                    channel="oink"
                ),
                invent.ui.Button(
                    name="to_goose",
                    label="Visit Lucy",
                    channel="navigate"
                ),
            ],
        )
    ],
)


# Handlers (stacks of blocks)
def make_honk(message):
    invent.play_sound("/static/honk.mp3")  # invent.media.sounds.honk.mp3)


def make_oink(message):
    invent.play_sound("/static/oink.mp3")  # invent.media.sounds.honk.mp3)


def move_page(message):
    if message.button == "to_goose":
        invent.goto("Honk")
    elif message.button == "to_pig":
        invent.goto("Oink")


# Pubsub (???)
invent.pubsub.subscribe(make_honk, to_channel="honk", when=["press", "touch"])
invent.pubsub.subscribe(make_oink, to_channel="oink", when=["press", "touch"])
invent.pubsub.subscribe(move_page, to_channel="navigate", when=["press",])


# GO!
farmyard_app.go()
