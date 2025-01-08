"""
Speech related functions: say (text-to-speech), list available voices for 
speech synthesis, set the preferred voice, and listen (speech-to-text).

Based on original pre-COVID work by [Nicholas H.Tollervey.](https://ntoll.org/)

Copyright (c) 2024 Invent contributors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import invent
from invent.i18n import _
from pyscript.ffi import create_proxy
from pyscript import window


# Check if the speech synthesis and recognition APIs are available.
try:
    synth = window.speechSynthesis
    SPEECH_SYNTHESIS_AVAILABLE = True
except AttributeError:
    SPEECH_SYNTHESIS_AVAILABLE = False
try:
    SpeechRecognition = window.SpeechRecognition
    SPEECH_RECOGNITION_AVAILABLE = True
except AttributeError:
    try:
        SpeechRecognition = window.webkitSpeechRecognition
        SPEECH_RECOGNITION_AVAILABLE = True
    except AttributeError:
        SPEECH_RECOGNITION_AVAILABLE = False

#: Flag for the datastore to indicate speech synthesis is taking place.
SPEAKING = "_SPEECH_SPEAKING"
#: Flag for the datastore to indicate speech synthesis has ended.
ENDED = "_SPEECH_ENDED"
#: Flag for the datastore to indicate speech detection is taking place.
LISTENING = "_SPEECH_LISTENING"
#: Flag for the datastore to indicate speech detection was prematurely aborted.
ABORTED = "_SPEECH_ABORTED"
#: Flag for the datastore to indicate an error during speech detection.
ERROR = "_SPEECH_ERROR"
#: Flag for the datastore to indicate speech detection was unable to match words.
NO_MATCH = "_SPEECH_NO_MATCH"

#: A reference to the preferred voice for speech synthesis.
PREFERRED_VOICE = None


def voices():
    """
    Return a list of available voices for speech synthesis.
    """
    if SPEECH_SYNTHESIS_AVAILABLE:
        return list(synth.getVoices())
    return []


def get_voice(name):
    """
    Return the voice with the given name.
    """
    for voice in voices():
        if voice.name == name:
            return voice
    return None


def set_voice(name):
    """
    Set the preferred voice for speech synthesis.
    """
    global PREFERRED_VOICE
    PREFERRED_VOICE = get_voice(name)


def say(text, result_key=None, lang=None, pitch=None, rate=None, volume=None):
    """
    Speak the given text string, which may contain SSML (but doesn't need to):

    https://en.wikipedia.org/wiki/Speech_Synthesis_Markup_Language

    If a result key is provided, the datastore will be updated with the status
    of the speech synthesiser. The status will be either SPEAKING or ENDED.
    If possible the preferred voice will be used (indicated via the set_voice
    function).

    The remaining parameters are optional, are based upon the properties of the
    built-in SpeechSynthesisUtterance class's properties, and can be used to
    specify the following:

      - lang: a string representing a BCP 47 language tag. For example,
        "en-US".
      - pitch: float representing the pitch value. It can range between 0
        (lowest) and 2 (highest), with 1 being the default pitch for the
        current platform or voice. Some speech synthesis engines or voices may
        constrain the minimum and maximum rates further. If SSML is used, this
        value will be overridden by prosody tags in the markup.
      - rate: a float representing the rate of speech value. It can range
        between 0.1 (lowest) and 2 (highest), with 1 being the default rate
        for the current platform or voice, which should correspond to a normal
        speaking rate. Other values act as a percentage relative to this, so
        for example 2 is twice as fast, 0.5 is half as fast, etc. Some speech
        synthesis engines or voices may constrain the minimum and maximum rates
        further. If SSML is used, this value will be overridden by prosody tags
        in the markup.
      - volume: a float that represents the volume value, between 0 (lowest)
        and 1 (highest). If SSML is used, this value will be overridden by
        prosody tags in the markup.
    """
    if not SPEECH_SYNTHESIS_AVAILABLE:
        raise RuntimeError(
            _("Sorry, your browser doesn't support speech synthesis!")
        )

    def _on_ended(event):
        """
        Handle the speech ending.
        """
        if result_key:
            invent.datastore[result_key] = ENDED

    def _on_error(error):
        """
        Handle the speech error.

        See: https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance/error_event
        """
        if result_key:
            invent.datastore[result_key] = ERROR + f": {error.error}."

    utterance = window.SpeechSynthesisUtterance.new()
    utterance.text = text
    if PREFERRED_VOICE:
        utterance.voice = PREFERRED_VOICE
    if lang:
        utterance.lang = lang
    if pitch:
        utterance.pitch = pitch
    if rate:
        utterance.rate = rate
    if volume:
        utterance.volume = volume
    utterance.addEventListener("end", create_proxy(_on_ended))
    utterance.addEventListener("error", create_proxy(_on_error))

    if result_key:
        invent.datastore[result_key] = SPEAKING
    synth.speak(utterance)


def listen(result_key):
    """
    Listen for speech and store the result in the datastore with the given
    result key. Returns a function that can be called to abort listening.

    The result key will be updated with the value LISTENING while
    listening is taking place. If the listening is aborted prematurely, the
    result key will be updated with the value ABORTED. If an error occurs, the
    result key will be updated with the value ERROR, along with an indication
    of the error that was encountered. If no match is found, the result key
    will be updated with the value NO_MATCH.

    Otherwise the result key will be updated with a string containing a
    transcript of the detected speech.
    """
    if not SPEECH_RECOGNITION_AVAILABLE:
        raise RuntimeError(
            _("Sorry, your browser doesn't support speech recognition!")
        )

    recognition = SpeechRecognition.new()

    def _on_result(event):
        """
        Handle the speech recognition result.
        """
        invent.datastore[result_key] = event.results[
            event.results.length - 1
        ].transcript

    def _on_no_match(event):
        """
        Handle the speech recognition not matching.
        """
        invent.datastore[result_key] = NO_MATCH

    def _on_error(error):
        """
        Handle a speech recognition error.

        See:https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognitionErrorEvent
        """
        invent.datastore[result_key] = (
            ERROR + f": {error.error} ({error.message})."
        )

    recognition.addEventListener("result", create_proxy(_on_result))
    recognition.addEventListener("nomatch", create_proxy(_on_no_match))
    recognition.addEventListener("error", create_proxy(_on_error))
    invent.datastore[result_key] = LISTENING
    recognition.start()

    def _abort():
        """
        Abort the speech recognition.
        """
        recognition.abort()
        invent.datastore[result_key] = ABORTED

    return _abort
