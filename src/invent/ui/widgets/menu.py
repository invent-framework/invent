"""
A menu widget for the Invent framework. Clicking on the activation button
opens up a menu of options. The menu can be dismissed by clicking outside of
it, or by selecting an option. The choices are provided as a list of strings,
and when the user selects one, the selected event is fired with the selected
option.

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
from pyscript.ffi import create_proxy
from pyscript.web import div, li, ul
from invent.ui.core import (
    Widget,
    TextProperty,
    ListProperty,
    ChoiceProperty,
    Event,
)
from invent.ui.widgets.button import Button
from invent.ui.core.measures import PURPOSES


class Menu(Widget):
    """
    A menu widget activated by a button, containing choices.
    """

    choices = ListProperty(_("The options from which to select."))

    hover = ChoiceProperty(
        _("Defines where the menu appears in relation to the button."),
        default_value="BELOW",
        choices=["ABOVE", "BELOW", "BEFORE", "AFTER"],
        group="style",
    )

    text = TextProperty(_("The text on the button."), default_value="≡")

    size = ChoiceProperty(
        _("The size of the button."),
        default_value="MEDIUM",
        choices=["LARGE", "MEDIUM", "SMALL"],
        group="style",
    )

    purpose = ChoiceProperty(
        _("The button's purpose."),
        default_value="DEFAULT",
        choices=PURPOSES,
        group="style",
    )

    opened = Event(
        _("Sent when the button is pressed."),
        button=_("The button that was clicked."),
    )

    selected = Event(
        _("The menu option has been selected."),
        selected=_("The new selected option."),
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256"><path d="M224,128a8,8,0,0,1-8,8H40a8,8,0,0,1,0-16H216A8,8,0,0,1,224,128ZM40,72H216a8,8,0,0,0,0-16H40a8,8,0,0,0,0,16ZM216,184H40a8,8,0,0,0,0,16H216a8,8,0,0,0,0-16Z"></path></svg>'  # noqa

    def on_choices_changed(self):
        # The menu list is rebuilt on every open, so no DOM update
        # is needed here.
        ...

    def on_text_changed(self):
        # Delegate text changes to the trigger button.
        self.trigger_button.text = self.text

    def on_size_changed(self):
        # Delegate size changes to the trigger button.
        self.trigger_button.size = self.size

    def on_purpose_changed(self):
        # Delegate purpose changes to the trigger button.
        self.trigger_button.purpose = self.purpose

    def on_hover_changed(self):
        # Swap the position modifier class on the wrapper.
        for pos in ("above", "below", "before", "after"):
            self._wrapper.classList.remove(f"invent-menu-wrapper--{pos}")
        self._wrapper.classList.add(
            f"invent-menu-wrapper--{self.hover.lower()}"
        )

    def _close_menu(self):
        """
        Remove the open menu list from the DOM and clear the open state
        class from the wrapper.
        """
        if self._menu_list is not None:
            self._menu_list.remove()
            self._menu_list = None
        self._wrapper.classList.remove("invent-menu-wrapper--open")

    def open_menu(self, event):
        """
        Toggle the menu open or closed when the button is clicked.

        When opening: build a list of items from self.choices, append it
        to the wrapper div (so it scrolls with the page), and publish
        the "opened" event.

        When closing: remove the menu list from the DOM.

        Clicking an item closes the menu and fires the "selected" event.
        """
        # Toggle: close if already open.
        if self._menu_list is not None:
            self._close_menu()
            return

        self.publish(
            self.opened,
            button=self.trigger_button.element,
        )

        def make_item_handler(option):
            # Return a proxied handler closed over the specific option,
            # avoiding the classic for-loop closure capture bug.
            def handler(e):
                e.stopPropagation()
                self._close_menu()
                self.publish(self.selected, selected=option)

            return create_proxy(handler)

        # Build the menu list from the current choices.
        menu_list = ul()
        menu_list.classList.add("invent-menu")
        for choice in self.choices or []:
            item = li(choice)
            item.classList.add("invent-menu-item")
            item.addEventListener("click", make_item_handler(choice))
            menu_list.append(item)

        self._menu_list = menu_list
        # The menu list is a child of the wrapper so it scrolls with
        # the page. CSS handles its absolute position relative to the
        # wrapper based on the hover modifier class.
        self._wrapper.classList.add("invent-menu-wrapper--open")
        self._wrapper.append(menu_list)

    def render(self):
        self.trigger_button = Button()
        self.trigger_button.render()
        btn_element = self.trigger_button.element
        btn_element.addEventListener("click", create_proxy(self.open_menu))

        # Initialise open-state tracker.
        self._menu_list = None

        # Wrapper: position: relative so the menu list can be absolutely
        # positioned relative to the button, and scrolls with the page.
        self._wrapper = div()
        self._wrapper.classList.add("invent-menu-wrapper")
        self._wrapper.classList.add(
            f"invent-menu-wrapper--{self.hover.lower()}"
        )
        self._wrapper.append(btn_element)
        return self._wrapper
