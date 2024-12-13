"""
An audio player widget for the Invent framework.

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

from invent.i18n import _
from invent.ui.core import (
    Widget,
    TextProperty,
    Event,
)
from pyscript.web import audio
from pyscript.ffi import create_proxy


class Audio(Widget):
    """
    An audio player with a play button, progress indicator and volume control.
    """

    source = TextProperty(_("The audio source file to play."))

    playing = Event(
        _("Sent when the audio starts to play."),
        audio="The audio source playing.",
    )

    paused = Event(
        _("Sent when the audio is paused."),
        audio=_("The audio source paused."),
        position=_("The pause position in seconds."),
    )

    position_changed = Event(
        _("Sent when the position in the audio is changed."),
        audio=_("The audio source that has been affected."),
        position=_("The new position in seconds."),
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M155.51 24.81a8 8 0 0 0-8.42.88L77.25 80H32a16 16 0 0 0-16 16v64a16 16 0 0 0 16 16h45.25l69.84 54.31A8 8 0 0 0 160 224V32a8 8 0 0 0-4.49-7.19M32 96h40v64H32Zm112 111.64l-56-43.55V91.91l56-43.55Zm54-106.08a40 40 0 0 1 0 52.88a8 8 0 0 1-12-10.58a24 24 0 0 0 0-31.72a8 8 0 0 1 12-10.58M248 128a79.9 79.9 0 0 1-20.37 53.34a8 8 0 0 1-11.92-10.67a64 64 0 0 0 0-85.33a8 8 0 1 1 11.92-10.67A79.83 79.83 0 0 1 248 128"/></svg>'  # noqa

    def play(self):
        """
        Play the audio source file, from the current position.
        """
        self.element.play()

    def pause(self):
        """
        Pause the playing of the source file.
        """
        self.element.pause()

    def reset(self):
        """
        Reset the current position to the start of the audio source file.
        """
        self.set_position(0)

    def stop(self):
        """
        Pause and reset the audio.
        """
        self.pause()
        self.reset()

    def set_position(self, position):
        """
        Set the current place in the audio source file to the specified
        position, as a value in seconds.
        """
        self.element.currentTime = position
        self.publish("position_changed", audio=self.source, position=position)

    def on_play(self, event):
        self.publish("playing", audio=self.source)

    def on_pause(self, event):
        self.publish(
            "paused", audio=self.source, position=event.target.currentTime
        )

    def on_source_changed(self):
        self.element.setAttribute("src", self.source)

    def render(self):
        element = audio(id=self.id)
        element.setAttribute("controls", "controls")
        element.addEventListener("play", create_proxy(self.on_play))
        element.addEventListener("pause", create_proxy(self.on_pause))
        return element
