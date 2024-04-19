from pyscript import window
from pyscript.ffi import create_proxy


_VOICES_BY_NAME = None


def on_voices_changed(event):
    """Voices are loaded asynchronously."""

    global _VOICES_BY_NAME

    voices_by_name = {voice.name: voice for voice in synth.getVoices()}

    _VOICES_BY_NAME = voices_by_name


try:
    synth = window.speechSynthesis
    synth.onvoiceschanged = create_proxy(on_voices_changed)

except AttributeError:
    print("Sorry, your browser doesn't support text to speech!")
    raise


try:
    SpeechRecognition = window.SpeechRecognition

except AttributeError:
    try:
        SpeechRecognition = window.webkitSpeechRecognition

    except AttributeError:
        print("Sorry, your browser doesn't support speech recognition!")
        raise


def get_voice_by_name(voice_name):
    """
    Return the voice with the specified name.

    Defaults to the first voice.
    """

    voice_name = voice_name.strip()

    if _VOICES_BY_NAME is not None:
        voice = _VOICES_BY_NAME.get(voice_name)

    else:
        voice = None

    return voice


preferred_voice_name = None


def set_voice(voice_name):
    global preferred_voice_name

    # We DON'T try to look up the actual voice, just in case the voices haven't
    # loaded yet. We will look it up when we actually say something.
    preferred_voice_name = voice_name


def say(text):
    """
    Say the specified text using speech synthesis.
    """
    utterance = window.SpeechSynthesisUtterance.new()

    # We may not get the requested voice if:
    #
    # a) the voices haven't loaded yet.
    # b) no voice exists with the specified name :)
    if preferred_voice_name:
        voice = get_voice_by_name(preferred_voice_name)
        if voice:
            utterance.voice = voice

    utterance.text = text
    synth.speak(utterance)


async def listen():
    """
    Speech recognition via the microphone.
    """

    import asyncio

    recognition = SpeechRecognition.new()

    # The speech recognition API is non-blocking but uses callbacks, so here
    # we wrap it with a Future, so we can create this awaitable function.
    future = asyncio.Future()

    def on_result(event):
        transcript = event.results.item(0).item(0).transcript
        future.set_result(transcript)

    def on_stop(event):
        recognition.stop()

    def on_error(event):
        raise Exception(str(event))

    recognition.onresult = create_proxy(on_result)
    recognition.onstop = create_proxy(on_stop)
    recognition.onerror = create_proxy(on_error)

    # Auto-stops when it detects a pause in the user's speech.
    recognition.continuous = False

    # If the speech synthesizer is still speaking, wait for it to shut up,
    # otherwise the microphone will pick up what it is saying :)
    while synth.speaking:
        await asyncio.sleep(0.1)

    recognition.start()

    return await future
