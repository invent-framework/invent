"""
A star rating widget for the Invent framework.

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
    FloatProperty,
    ChoiceProperty,
    BooleanProperty,
    Event,
)
from pyscript.web import div, span
from pyscript.ffi import create_proxy


class Rating(Widget):
    """
    A star rating widget with half-star precision (0.5 steps).

    Each star is split into a left half (scores i-0.5) and a right half
    (scores i), giving values like 0.5, 1, 1.5 ... up to maximum.

    Displays the numeric value alongside the stars. When the user changes
    the rating a brief popup message appears and then fades away.
    """

    value = FloatProperty(
        _("The current rating value (multiples of 0.5)."),
        default_value=0.0,
    )

    # TODO: Allow a choice of 1. This could be used to indicate a favourite item, without implying a 5-star rating system.
    maximum = ChoiceProperty(
        _("The number of stars to display."),
        default_value="5",
        choices=["3", "5", "10"],
        group="style",
    )

    # TODO: Add a "step" property to allow either whole or half-star steps.

    read_only = BooleanProperty(
        _("Prevent the user from changing the rating."),
        default_value=False,
    )

    change = Event(
        _("Sent when the rating value is changed by the user."),
        rating=_("The Rating widget whose value changed."),
        value=_("The new rating value."),
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256"><path d="M239.18,97.26A16.38,16.38,0,0,0,224.92,86l-59-4.76L143.14,26.15a16.36,16.36,0,0,0-30.27,0L90.11,81.23,31.08,86a16.46,16.46,0,0,0-9.37,28.86l45,38.83L53,211.75a16.38,16.38,0,0,0,24.5,17.82L128,198.49l50.53,31.08A16.4,16.4,0,0,0,203,211.75l-13.76-58.07,45-38.83A16.43,16.43,0,0,0,239.18,97.26Zm-15.34,5.47-48.7,42a8,8,0,0,0-2.56,7.91l14.88,62.8a.37.37,0,0,1-.17.48c-.18.14-.23.11-.38,0l-54.72-33.65a8,8,0,0,0-8.38,0L69.09,215.94c-.15.09-.19.12-.38,0a.37.37,0,0,1-.17-.48l14.88-62.8a8,8,0,0,0-2.56-7.91l-48.7-42c-.12-.1-.23-.19-.13-.5s.18-.27.33-.29l63.92-5.16A8,8,0,0,0,103,91.86l24.62-59.61c.08-.17.11-.25.35-.25s.27.08.35.25L153,91.86a8,8,0,0,0,6.75,4.92l63.92,5.16c.15,0,.24,0,.33.29S224,102.63,223.84,102.73Z"></path></svg>'  # noqa

    # Helpers

    def _half_click(self, half_value):
        """Return a click handler that sets the rating to `half_value`."""

        def handler(event):
            event.stopPropagation()
            if not self.read_only:
                self.value = half_value
                self._show_message(
                    _(f"Rating changed to {self.value} out of {self.maximum}.")
                )
                self.publish("change", rating=self, value=self.value)

        return create_proxy(handler)

    # TODO: Do we need this? ;-)
    def _show_message(self, text):
        """Restart the fade-out animation on the message element."""
        el = self._message_element
        el.classes.remove("rating-message-visible")
        el.textContent = text
        _ = el._dom_element.offsetWidth
        el.classes.add("rating-message-visible")

    def _rebuild_stars(self):
        """Redraw all star spans to reflect the current value and maximum."""
        self._stars_element._dom_element.replaceChildren()

        max_stars = int(self.maximum)
        for i in range(1, max_stars + 1):
            star = span()
            star.classes.add("rating-star")

            # Fill state — drives the CSS color/gradient.
            if self.value >= i:
                star.classes.add("rating-star-full")
            elif self.value >= i - 0.5:
                star.classes.add("rating-star-half")
            else:
                star.classes.add("rating-star-empty")

            # Visible glyph — always ★, appearance controlled by CSS.
            glyph = span("★")
            glyph.classes.add("rating-star-glyph")
            star.append(glyph)

            # Invisible left/right halves that capture clicks.
            # Only added when the widget is interactive.
            if not self.read_only:
                left = span()
                left.classes.add("rating-half")
                left.classes.add("rating-half-left")
                left._dom_element.addEventListener(
                    "click", self._half_click(i - 0.5)
                )

                right = span()
                right.classes.add("rating-half")
                right.classes.add("rating-half-right")
                right._dom_element.addEventListener(
                    "click", self._half_click(float(i))
                )

                star.append(left)
                star.append(right)

            self._stars_element.append(star)

        self._value_element.textContent = f"{self.value}/{self.maximum}"

    # Property change hooks

    def on_value_changed(self):
        if hasattr(self, "_stars_element"):
            self._rebuild_stars()

    def on_maximum_changed(self):
        if self.value > int(self.maximum):
            self.value = float(int(self.maximum))
        if hasattr(self, "_stars_element"):
            self._rebuild_stars()

    def on_read_only_changed(self):
        if hasattr(self, "_stars_element"):
            if self.read_only:
                self.element.classes.remove("rating-interactive")
                self.element.classes.add("rating-readonly")
            else:
                self.element.classes.remove("rating-readonly")
                self.element.classes.add("rating-interactive")
            self._rebuild_stars()

    # Render

    def render(self):
        self._stars_element = span()
        self._stars_element.classes.add("rating-stars")

        self._value_element = span(f"{self.value}/{self.maximum}")
        self._value_element.classes.add("rating-value")

        self._message_element = span("")
        self._message_element.classes.add("rating-message")

        element = div(
            self._stars_element,
            self._value_element,
            self._message_element,
            id=self.id,
        )
        element.classes.add("rating")
        if self.read_only:
            element.classes.add("rating-readonly")
        else:
            element.classes.add("rating-interactive")

        self._rebuild_stars()
        return element
