"""
A function to play a given audio file.

Based on original pre-COVID work by [Nicholas H.Tollervey.](https://ntoll.org/)

Copyright (c) 2019-present Invent contributors.

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
from pyscript.web import audio
from pyscript.ffi import create_proxy

PLAYING = "_AUDIO_PLAYING"
ENDED = "_AUDIO_ENDED"


def play(url, result_key=None):
    """
    Play an audio file at the given URL. If a result key is provided, the
    datastore will be updated with the status of the audio. The status will be
    either PLAYING or ENDED.
    """

    def _on_ended(event):
        """
        Handle the audio ending.
        """
        if result_key:
            invent.datastore[result_key] = ENDED

    sound = audio(src=str(url))
    sound.addEventListener("ended", create_proxy(_on_ended))
    if result_key:
        invent.datastore[result_key] = PLAYING
    sound.play()
