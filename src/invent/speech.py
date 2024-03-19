import json
from pyscript import fetch, window

try:
    synth = window.speechSynthesis
except:
    # If tts is not supported we disable the action buttons
    print("Sorry, your browser doesn't support text to speech!")
    synth = None
    raise


def say(text):
    """Ask the overlords!"""
    msg = window.SpeechSynthesisUtterance.new()
    msg.text = text
    synth.speak(msg)


def listen():
    try:
        SpeechRecognition =  window.SpeechRecognition
    except AttributeError:
        try:
            SpeechRecognition = window.webkitSpeechRecognition
        except AttributeError:
            print("Unable to find the SpeechRecognition or webkitSpeechRecognition APIs")

    recognition = SpeechRecognition.new()

    def on_start(e=None):
        print("starting to listen... SPEAK!")

    def on_stop(e=None):
        print("stopped listening")
        recognition.stop()

    def on_result(result):
        window.console.log(result.results)
        print(result.results[0][0].transcript)

    recognition.onspeechend = on_stop
    recognition.onresult = on_result
    recognition.onstart = on_start

    # We start the recognition here
    recognition.start();