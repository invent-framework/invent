"""
Contains the definition of an Invent page - i.e. the content of the screen
at any single point in time. Many pages make an app. Move between pages via
transitions triggered by the user.

```
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
```
"""

from pyscript.ffi import create_proxy
from pyscript.web import page as document

from .column import Column
from invent.i18n import _
from invent.ui.core import ChoiceProperty, TextProperty
from invent.utils import is_micropython

# Maps transition speed choices to their CSS variable equivalents.
_SPEED_VARS = {
    "SLOW": "--transition-speed-slow",
    "MEDIUM": "--transition-speed",
    "FAST": "--transition-speed-fast",
}


class Page(Column):
    """
    Only one page at a time is displayed on the screen. Pages contain
    related widgets to achieve some aim.
    """

    background = TextProperty(
        _("The page's background (colour, image or gradient)."),
        default_value=None,
        group="style",
    )

    transition = ChoiceProperty(
        _("The transition effect when showing or hiding the page."),
        default_value="NONE",
        choices=["NONE", "FADE", "SLIDE", "ZOOM", "CONVEX", "CONCAVE"],
        group="style",
    )

    transition_speed = ChoiceProperty(
        _("The speed of the page transition."),
        default_value="MEDIUM",
        choices=["SLOW", "MEDIUM", "FAST"],
        group="style",
    )

    def _apply_background(self):
        """
        Apply or reset self.background on the body element. A falsy
        value removes any inline background, restoring the stylesheet
        default.
        """
        if self.background:
            document.body.style["background"] = self.background
        else:
            document.body.style["background"] = (
                None  # Reset to stylesheet default.
            )

    def _apply_transition_speed(self):
        """
        Set the CSS transition duration variable on the element from
        the current transition_speed choice.
        """
        var = _SPEED_VARS[self.transition_speed]
        self.element.style["--page-transition-duration"] = f"var({var})"

    def _animate(self, cls, on_done):
        """
        Add an animation class and fire on_done when it completes.
        The listener removes itself after a single firing.
        """
        self.element.classes.add(cls)

        def handler(event):
            self.element.classes.remove(cls)
            self.element.removeEventListener(
                "animationend", self._animation_handler
            )
            if not is_micropython:
                self._animation_handler.destroy()
            self._animation_handler = None
            on_done()

        self._animation_handler = create_proxy(handler)
        self.element.addEventListener("animationend", self._animation_handler)

    def on_background_changed(self):
        """
        Update the body background immediately if this page is visible.
        """
        if self.element.style["display"] != "None":
            self._apply_background()

    def on_transition_speed_changed(self):
        """
        Update the CSS duration variable when the speed choice changes.
        """
        self._apply_transition_speed()

    def render(self):
        """
        Returns an HTML element to insert into the DOM.
        """
        element = super().render()
        element.classList.add("container")
        element.style["display"] = "None"
        var = _SPEED_VARS[self.transition_speed]
        element.style["--page-transition-duration"] = f"var({var})"
        return element

    def show(self):
        """
        Make the page visible, applying its background and transition.
        """
        self._apply_background()
        self.element.style["display"] = "flex"
        if self.transition != "NONE":
            cls = f"invent-page--entering-{self.transition.lower()}"
            self._animate(cls, lambda: None)

    def hide(self):
        """
        Hide the page, playing the exit transition before removing it
        from view.
        """
        if self.transition == "NONE":
            self.element.style["display"] = "None"  # Hidden by default.
            return
        cls = f"invent-page--leaving-{self.transition.lower()}"

        def on_done():
            # Hide the page once the exit animation completes.
            self.element.style["display"] = "None"

        self._animate(cls, on_done)
