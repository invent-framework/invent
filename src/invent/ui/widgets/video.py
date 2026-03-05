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

import re

from invent.i18n import _
from invent.ui.core import (
    Widget,
    TextProperty,
    Event,
)
from pyscript.web import div, video
from pyscript.ffi import create_proxy

# Patterns to extract video IDs from hosted platform URLs.
_YOUTUBE_ID_RE = re.compile(r"v=([a-zA-Z0-9_-]+)")
_VIMEO_ID_RE = re.compile(r"vimeo\.com/(\d+)")
_DAILYMOTION_ID_RE = re.compile(r"video/([a-zA-Z0-9]+)")


# Permissions granted to hosted video iframes.
_IFRAME_ALLOW = (
    "accelerometer; autoplay; clipboard-write; "
    "encrypted-media; gyroscope; picture-in-picture"
)


def _hosted_embed_url(source):
    """
    Return an iframe embed URL for a known hosted platform, or None.
    """
    if "youtube" in source or "youtu.be" in source:
        m = _YOUTUBE_ID_RE.search(source)
        return (
            "https://www.youtube.com/embed/{}".format(m.group(1))
            if m
            else None
        )
    if "vimeo" in source:
        m = _VIMEO_ID_RE.search(source)
        return (
            "https://player.vimeo.com/video/{}".format(m.group(1))
            if m
            else None
        )
    if "dailymotion" in source or "dai.ly" in source:
        m = _DAILYMOTION_ID_RE.search(source)
        return (
            "https://www.dailymotion.com/embed/video/{}".format(m.group(1))
            if m
            else None
        )
    return None


class Video(Widget):
    """
    A video player with a play button, progress indicator and volume
    control. Supports local/remote video files and hosted platforms
    (YouTube, Vimeo, Dailymotion). Hosted sources render as responsive
    iframes; programmatic control (play, pause, etc.) is not available
    for those sources.
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
        Play the video from the current position.
        """
        self.element.querySelector("video").play()

    def pause(self):
        """
        Pause the video at the current position.
        """
        self.element.querySelector("video").pause()

    def reset(self):
        """
        Reset the current position to the start of the video.
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
        Seek to the given position (in seconds).
        """
        native = self.element.querySelector("video")
        native.currentTime = position
        self.publish(
            "position_changed",
            source=self.source,
            position=position,
        )

    def on_play(self, event):
        """Handle the native video play event."""
        self.publish("playing", source=self.source)

    def on_pause(self, event):
        """Handle the native video pause event."""
        self.publish(
            "paused",
            source=self.source,
            position=event.target.currentTime,
        )

    def _build_native(self):
        """
        Build an HTML5 video element with playback controls and
        event listeners.
        """
        el = video()
        el.setAttribute("controls", "controls")
        if self.source:
            el.setAttribute("src", self.source)
        el.addEventListener("play", create_proxy(self.on_play))
        el.addEventListener("pause", create_proxy(self.on_pause))
        return el

    def _build_hosted(self, embed_url):
        """
        Build a responsive 16:9 iframe wrapper for a hosted platform
        embed URL.
        """
        wrapper = div()
        wrapper.setAttribute(
            "style",
            "position:relative;padding-bottom:56.25%;"
            "height:0;overflow:hidden;",
        )
        wrapper.innerHTML = (
            f'<iframe src="{embed_url}" '
            f'style="position:absolute;top:0;left:0;'
            f'width:100%;height:100%;border:0;" '
            f"allowfullscreen "
            f'allow="{_IFRAME_ALLOW}">'
            f"</iframe>"
        )
        return wrapper

    def _inject(self):
        """
        Clear the container and inject either a native video element
        or a hosted iframe, depending on the current source.
        """
        self.element.innerHTML = ""
        embed_url = _hosted_embed_url(self.source) if self.source else None
        child = (
            self._build_hosted(embed_url)
            if embed_url
            else self._build_native()
        )
        self.element.append(child)

    def on_source_changed(self):
        """
        Re-inject the appropriate player into the container whenever
        the source property changes.
        """
        self._inject()

    def render(self):
        """
        Render a stable container div and inject the appropriate
        player as a child. The container never changes, allowing
        the source to be switched freely after render.
        """
        container = div(id=self.id)
        return container
