"""
A video player widget for the Invent framework.

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

from invent.i18n import _
from invent.ui.core import (
    Widget,
    TextProperty,
    Event,
)
from pyscript.web import video
from pyscript.ffi import create_proxy


class Video(Widget):
    """
    A video player with a play button, progress indicator and volume control.
    """

    source = TextProperty(_("The video source file to play."))

    playing = Event(
        _("Sent when the video starts to play."),
        source=_("The video source playing."),
    )

    paused = Event(
        _("Sent when the video is paused."),
        source=_("The video source paused."),
        position=_("The pause position in seconds."),
    )

    position_changed = Event(
        _("Sent when the position in the video is changed."),
        source=_("The video source that has been affected."),
        position=_("The new position in seconds."),
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="m164.44 105.34l-48-32A8 8 0 0 0 104 80v64a8 8 0 0 0 12.44 6.66l48-32a8 8 0 0 0 0-13.32M120 129.05V95l25.58 17ZM216 40H40a16 16 0 0 0-16 16v112a16 16 0 0 0 16 16h176a16 16 0 0 0 16-16V56a16 16 0 0 0-16-16m0 128H40V56h176zm16 40a8 8 0 0 1-8 8H32a8 8 0 0 1 0-16h192a8 8 0 0 1 8 8"/></svg>'  # noqa

    def play(self):
        """
        Play the video source file, from the current position.
        """
        self.element.play()

    def pause(self):
        """
        Pause the playing of the source file.
        """
        self.element.pause()

    def reset(self):
        """
        Reset the current position to the start of the video source file.
        """
        self.set_position(0)

    def stop(self):
        """
        Pause and reset the video.
        """
        self.pause()
        self.reset()

    def set_position(self, position):
        """
        Set the current place in the video source file to the specified
        position, as a value in seconds.
        """
        self.element.currentTime = position
        self.publish("position_changed", source=self.source, position=position)

    def on_play(self, event):
        self.publish("playing", source=self.source)

    def on_pause(self, event):
        self.publish(
            "paused", source=self.source, position=event.target.currentTime
        )

    def on_source_changed(self):
        self.element.setAttribute("src", self.source)

    def render(self):
        element = video(id=self.id)
        element.setAttribute("controls", "controls")
        element.addEventListener("play", create_proxy(self.on_play))
        element.addEventListener("pause", create_proxy(self.on_pause))
        return element
