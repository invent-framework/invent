import invent
from invent.ui import Button, Image

invent.set_media_root("static")

# User interface
farmyard_app = invent.App(
    name="Loosey Goosey",
    content = [
        invent.Page(
            name="Honk",
            content = [
                invent.ui.Image(
                    invent.media.images.goose.png,
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
                    invent.media.images.pig.png,
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
    invent.play_sound(invent.media.sounds.honk.mp3)


def make_oink(message):
    invent.play_sound(invent.media.sounds.oink.mp3)


def move_page(message):
    if message.button == "to_goose":
        invent.show_page("Honk")
    elif message.button == "to_pig":
        invent.show_page("Oink")


# Pubsub (???)
invent.pubsub.subscribe(make_honk, to_channel="honk", when=["press", "touch"])
invent.pubsub.subscribe(make_oink, to_channel="oink", when=["press", "touch"])
invent.pubsub.subscribe(move_page, to_channel="navigate", when=["press",])


# GO!
farmyard_app.go()
