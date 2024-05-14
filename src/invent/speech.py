from pyscript import window
from pyscript.ffi import create_proxy

from invent.compatability import sleep_ms


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
    window.console.error("Sorry, your browser doesn't support text to speech!")


try:
    SpeechRecognition = window.SpeechRecognition
except AttributeError:
    try:
        SpeechRecognition = window.webkitSpeechRecognition
    except AttributeError:
        window.console.error(
            "Sorry, your browser doesn't support speech recognition!"
        )


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


class RecognitionStatus:
    """A class to encapsulate the status of speech recognition."""

    def __init__(self):
        self.done = False
        self.transcript = None
        self.error = None


async def listen():
    """
    Speech recognition via the microphone.
    """

    recognition = SpeechRecognition.new()

    status = RecognitionStatus()

    def on_result(event):
        status.transcript = event.results.item(0).item(0).transcript
        status.done = True

    def on_stop(event):
        recognition.stop()
        status.done = True

    def on_error(event):
        status.error = Exception(str(event))
        status.done = True

    recognition.onresult = create_proxy(on_result)
    recognition.onstop = create_proxy(on_stop)
    recognition.onerror = create_proxy(on_error)

    # Auto-stops when it detects a pause in the user's speech.
    recognition.continuous = False

    # If the speech synthesizer is still speaking, wait for it to shut up,
    # otherwise the microphone will pick up what it is saying :)
    while synth.speaking:
        await sleep_ms(100)

    recognition.start()

    while not status.done:
        await sleep_ms(10)

    if status.error:
        raise status.error

    return status.transcript
