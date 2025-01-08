import asyncio
import invent
import umock
import upytest
from invent.tools import speech
from pyscript import window


async def test_voices():
    """
    An array of voices should be returned.
    """
    result = speech.voices()
    assert isinstance(result, list), "Voices not returned as a list."
    assert len(result) > 0, "No voices returned."


async def test_get_voice():
    """
    A voice should be returned, by name.
    """
    voices = speech.voices()
    voice = voices[0]
    result = speech.get_voice(voice.name)
    assert (
        result.name == voice.name
    ), f"Voice not returned. Got: {result} Expected: {voice}"


async def test_set_voice():
    """
    The preferred voice should be set.
    """
    voices = speech.voices()
    voice = voices[0]
    speech.set_voice(voice.name)
    assert (
        speech.PREFERRED_VOICE.name == voice.name
    ), "Preferred voice not set. Got: {result} Expected: {voice}"


async def test_say():
    """
    Use of the simple `say` function.
    """
    speech.PREFERRED_VOICE = None
    text = "Hello, world!"
    result_key = "speech_said"
    got_speaking_from_speech = (
        asyncio.Event()
    )  # Used to wait for the speak event.
    got_ended_from_speech = asyncio.Event()  # Used to wait for the end event.

    def handler(message):
        if message.value == speech.SPEAKING:
            got_speaking_from_speech.set()
        elif message.value == speech.ENDED:
            got_ended_from_speech.set()

    invent.subscribe(handler, to_channel="store-data", when_subject=result_key)

    speech.say(text, result_key=result_key)

    await got_speaking_from_speech.wait()
    assert (
        invent.datastore[result_key] == speech.SPEAKING
    ), "Speech speak event not stored in datastore."
    await got_ended_from_speech.wait()
    assert (
        invent.datastore[result_key] == speech.ENDED
    ), "Speech end event not stored in datastore."


async def test_say_with_options():
    """
    Use of the `say` function with options.
    """
    speech.PREFERRED_VOICE = None
    text = "Hello, world with speech options!"
    result_key = "speech_said"
    got_speaking_from_speech = (
        asyncio.Event()
    )  # Used to wait for the speak event.
    got_ended_from_speech = asyncio.Event()  # Used to wait for the end event.

    def handler(message):
        if message.value == speech.SPEAKING:
            got_speaking_from_speech.set()
        elif message.value == speech.ENDED:
            got_ended_from_speech.set()

    invent.subscribe(handler, to_channel="store-data", when_subject=result_key)

    speech.say(
        text,
        result_key=result_key,
        lang="en-US",
        pitch=2,
        rate=2,
        volume=0.5,
    )

    await got_speaking_from_speech.wait()
    assert (
        invent.datastore[result_key] == speech.SPEAKING
    ), "Speech speak event not stored in datastore."
    await got_ended_from_speech.wait()
    assert (
        invent.datastore[result_key] == speech.ENDED
    ), "Speech end event not stored in datastore."


@upytest.skip(
    "This feature only works on Chromium based browsers.",
    skip_when=not speech.SPEECH_RECOGNITION_AVAILABLE,
)
async def test_listen():
    """
    Use of the simple `listen` function.

    Since we can't automatically create spoken words for the browser to listen
    to, this test uses uMock to simulate the browser's speech synthesis API
    (specifically the calls to `start` and `abort`).
    """
    result_key = "speech_heard"
    got_listening_from_speech = (
        asyncio.Event()
    )  # Used to wait for the listen event.
    got_aborted_from_speech = (
        asyncio.Event()
    )  # Used to wait for the heard event.

    def handler(message):
        if message.value == speech.LISTENING:
            got_listening_from_speech.set()
        elif message.value == speech.ABORTED:
            got_aborted_from_speech.set()

    invent.subscribe(handler, to_channel="store-data", when_subject=result_key)

    with umock.patch("invent.tools.speech:window"):
        abort = speech.listen(result_key=result_key)
        await got_listening_from_speech.wait()
        assert (
            invent.datastore[result_key] == speech.LISTENING
        ), "Speech listen event not stored in datastore."
        abort()
        await got_aborted_from_speech.wait()
        assert (
            invent.datastore[result_key] == speech.ABORTED
        ), "Speech abort event not stored in datastore."
