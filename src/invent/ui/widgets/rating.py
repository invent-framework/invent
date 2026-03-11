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
    (scores i), giving values like 0.5, 1.0, 1.5 ... up to maximum.

    Displays the numeric value alongside the stars. When the user changes
    the rating a brief popup message appears and then fades away.
    """

    value = FloatProperty(
        _("The current rating value (multiples of 0.5)."),
        default_value=0.0,
    )

    maximum = ChoiceProperty(
        _("The number of stars to display."),
        default_value="5",
        choices=["3", "5", "10"],
        group="style",
    )

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
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="m234.5 114.38l-45.1 39.36l13.51 58.6a16 16 0 0 1-23.84 17.34l-51.11-31l-51 31a16 16 0 0 1-23.84-17.34l13.49-58.54l-45.11-39.42a16 16 0 0 1 9.12-28.06l59.46-5.15l23.21-55.36a15.95 15.95 0 0 1 29.44 0L191 81.17l59.44 5.15a16 16 0 0 1 9.11 28.06Z"/></svg>'  # noqa

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
