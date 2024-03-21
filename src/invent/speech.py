from pyscript import fetch, window
from .compatability import proxy


try:
    synth = window.speechSynthesis

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

    for voice in synth.getVoices():
        if voice.name == voice_name:
            break

    else:
        voice = synth.getVoices()[0]

    return voice


def say(text):
    """
    Say the specified text using speech synthesis.
    """
    utterance = window.SpeechSynthesisUtterance.new()
    utterance.voice = get_voice_by_name("Catherine")
    utterance.text = text
    synth.speak(utterance)


async def listenJS():
    """
    Speech recognition via the microphone using pure JS.
    """
    return await window.recognizeSpeech()


async def listen():
    """
    Speech recognition via the microphone.
    """

    import asyncio

    recognition = SpeechRecognition.new()

    # The speech recognition API is non-blocking but uses callbacks, so here
    # we wrap it with a Future.
    future = asyncio.Future()

    def on_result(event):
        transcript = event.results.item(0).item(0).transcript
        future.set_result(transcript)

    def on_stop(event):
        recognition.stop()

    def on_error(event):
        raise Exception(str(event))

    recognition.onresult = proxy(on_result)
    recognition.onstop = proxy(on_stop)
    recognition.onerror = proxy(on_error)

    # Auto-stops when it detects a pause in the user's speech.
    recognition.continuous = False

    # If the speech synthesizer is still speaking, wait for it to shut up,
    # otherwise the microphone will pick up what it is saying :)
    while synth.speaking:
        await asyncio.sleep(0.1)

    recognition.start()

    return await future
