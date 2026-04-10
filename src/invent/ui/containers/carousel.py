"""
A carousel container for the Invent framework.

Items (Invent components) in the carousel are displayed one at a time, with
controls to move between them. The carousel always loops, so advancing from
the last item will return to the first item, and vice versa.

The height of the carousel is determined by the tallest item, and the width is
determined by the widest item. This means that the carousel will not change
size as the user navigates through the items, providing a stable and
consistent layout.

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
from ..core.component import Component
from invent.ui.core import ListProperty, ChoiceProperty, IntegerProperty
from pyscript import ffi
from pyscript.web import div, button

# SVG icons for the carousel controls. These are defined as constants to avoid
# cluttering the main class definition. They are simple left and right carets
# that will be used for the previous and next buttons in the carousel controls.
_CARET_RIGHT = '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256"><path d="M181.66,133.66l-80,80a8,8,0,0,1-11.32-11.32L164.69,128,90.34,53.66a8,8,0,0,1,11.32-11.32l80,80A8,8,0,0,1,181.66,133.66Z"></path></svg>'  # noqa
_CARET_LEFT = '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256"><path d="M165.66,202.34a8,8,0,0,1-11.32,11.32l-80-80a8,8,0,0,1,0-11.32l80-80a8,8,0,0,1,11.32,11.32L91.31,128Z"></path></svg>'  # noqa


class Carousel(Component):
    """
    A carousel container for the Invent framework.
    """

    children = ListProperty(
        _("The child items to display in the carousel."),
        default_value=None,
    )

    current_index = IntegerProperty(
        _("The index of the currently displayed item in the carousel."),
        default_value=0,
        min_value=0,
    )

    transition = ChoiceProperty(
        _("The transition effect to use when moving between items."),
        choices=["fade", "slide"],
        default_value="fade",
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256"><path d="M192,48H64A16,16,0,0,0,48,64V192a16,16,0,0,0,16,16H192a16,16,0,0,0,16-16V64A16,16,0,0,0,192,48Zm0,144H64V64H192V192ZM240,56V200a8,8,0,0,1-16,0V56a8,8,0,0,1,16,0ZM32,56V200a8,8,0,0,1-16,0V56a8,8,0,0,1,16,0Z"></path></svg>'  # noqa

    def _on_prev(self, event):
        """
        Move to the previous item, wrapping from first to last.
        """
        n = len(self.children) if self.children else 0
        if n:
            self.current_index = (self.current_index - 1) % n

    def _on_next(self, event):
        """
        Move to the next item, wrapping from last to first.
        """
        n = len(self.children) if self.children else 0
        if n:
            self.current_index = (self.current_index + 1) % n

    def _on_touch_start(self, event):
        """
        Record the X position where a swipe gesture begins.
        """
        self._touch_start_x = event.touches[0].clientX

    def _on_touch_end(self, event):
        """
        Complete a swipe gesture.

        A swipe of more than 50px to the left advances to the next
        item; to the right it returns to the previous item. Smaller
        movements are ignored to avoid triggering on accidental nudges.
        """
        delta = event.changedTouches[0].clientX - self._touch_start_x
        if abs(delta) > 50:
            if delta < 0:
                self._on_next(event)
            else:
                self._on_prev(event)

    def _activate(self, index):
        """
        Show the slot at index directly, without any transition.
        """
        for i, slot in enumerate(self._item_slots):
            slot.classes.remove("active")
            slot.classes.remove("leaving")
            if i == index:
                slot.classes.add("active")

    def on_children_changed(self):
        """
        Rebuild the carousel track when the child list changes.

        Each child is wrapped in a slot div that the carousel uses to
        manage visibility and transitions. The first item is shown
        immediately, without transition animation.
        """
        self._track.replaceChildren()
        self._item_slots = []
        if not self.children:
            return
        for child in self.children:
            child.parent = self
            slot = div(classes="invent-carousel-item")
            slot.append(child.element)
            self._item_slots.append(slot)
            self._track.append(slot)
        self._prev_index = 0
        self._activate(0)

    def on_current_index_changed(self):
        """
        Animate to the newly selected item.

        Computes travel direction from the previous and new indices,
        sets the data-direction attribute for CSS to act on, then
        moves the outgoing slot to 'leaving' and the incoming slot
        to 'active'. Any stale 'leaving' slot from a prior transition
        is cleared first.
        """
        if not self._item_slots:
            return
        n = len(self._item_slots)
        new_index = self.current_index
        # Guard against a stale prev_index after children are replaced.
        prev_index = self._prev_index if self._prev_index < n else 0
        # Forward means a higher index, or wrapping from the last item
        # back to the first.
        going_forward = (
            (new_index > prev_index)
            and not (prev_index == 0 and new_index == n - 1)
        ) or (prev_index == n - 1 and new_index == 0)
        self.element.setAttribute(
            "data-direction",
            "forward" if going_forward else "backward",
        )
        # Clear any slot still marked as leaving from the previous
        # transition before starting the next one.
        for slot in self._item_slots:
            slot.classes.remove("leaving")
        old_slot = self._item_slots[prev_index]
        new_slot = self._item_slots[new_index]
        if old_slot is not new_slot:
            old_slot.classes.remove("active")
            old_slot.classes.add("leaving")
        new_slot.classes.add("active")
        self._prev_index = new_index

    def on_transition_changed(self):
        """
        Apply the chosen transition mode to the carousel element.

        The CSS uses the data-transition attribute to select between
        the fade and slide transition styles.
        """
        self.element.setAttribute("data-transition", self.transition)

    def render(self):
        """
        Create the static HTML scaffold for the carousel.

        Builds the track div (which will hold child slots) and the two
        control buttons, then returns the outer wrapper as self.element.
        The transition and direction data attributes are given their
        starting values here; the on_*_changed methods update them later.
        """
        self._track = div(classes="invent-carousel-track")
        self._item_slots = []
        self._prev_index = 0

        prev_btn = button(
            classes="invent-carousel-ctrl invent-carousel-ctrl--prev"
        )
        prev_btn.innerHTML = _CARET_LEFT
        prev_btn.setAttribute("aria-label", _("Previous"))
        prev_btn.addEventListener("click", ffi.create_proxy(self._on_prev))

        next_btn = button(
            classes="invent-carousel-ctrl invent-carousel-ctrl--next"
        )
        next_btn.innerHTML = _CARET_RIGHT
        next_btn.setAttribute("aria-label", _("Next"))
        next_btn.addEventListener("click", ffi.create_proxy(self._on_next))

        wrapper = div(classes="invent-carousel")
        # Set the initial transition mode; on_transition_changed will
        # update this if the user sets a different value.
        wrapper.setAttribute("data-transition", "fade")
        # Swipe gestures on touch devices are handled on the track so
        # the full content area is touch-sensitive.
        self._track.addEventListener(
            "touchstart", ffi.create_proxy(self._on_touch_start)
        )
        self._track.addEventListener(
            "touchend", ffi.create_proxy(self._on_touch_end)
        )
        wrapper.append(self._track)
        wrapper.append(prev_btn)
        wrapper.append(next_btn)
        return wrapper
