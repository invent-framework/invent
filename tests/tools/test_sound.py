import asyncio
import invent
from invent.tools import sound


async def test_play_sound():
    """
    Use of the simple `play` function with a sound file.
    """
    sound_file = "./tests/test_data/honk.mp3"
    result_key = "sound_played"
    got_play_from_sound = asyncio.Event()  # Used to wait for the play event.
    got_end_from_sound = asyncio.Event()  # Used to wait for the end event.

    def handler(message):
        if message.value == sound.PLAYING:
            got_play_from_sound.set()
        elif message.value == sound.ENDED:
            got_end_from_sound.set()

    invent.subscribe(
        handler,
        to_channel=invent.datastore.DATASTORE_SET_CHANNEL,
        when_subject=result_key,
    )

    sound.play(sound_file, result_key=result_key)
    print("HONK!", end="")

    await got_play_from_sound.wait()
    assert (
        invent.datastore[result_key] == sound.PLAYING
    ), "Sound play event not stored in datastore."
    await got_end_from_sound.wait()
    assert (
        invent.datastore[result_key] == sound.ENDED
    ), "Sound end event not stored in datastore."
