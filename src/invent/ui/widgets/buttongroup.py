"""
A button group widget for the Invent framework.

Button groups are a way of grouping buttons together, often with a shared
purpose and as a more pleasing alternative to radio buttons. They consist
of a set of buttons, only one of which can be active at a time. The active
button is visually distinct from the others, and indicates the current
selection.

The possible values of the button group are defined by the choices property.
When a button is pressed, the value of the button group is updated to match
the value of the button that was pressed.

The button group also emits a change event when the value changes, which can
be used to trigger other actions in the application.

Button groups can be styled in the same way as regular buttons, with size and
purpose properties. The buttons within the group will inherit these styles,
but the active button will also have an additional "active" style to indicate
that it is the currently selected option.

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

from collections import OrderedDict

from invent.i18n import _
from pyscript.ffi import create_proxy
from pyscript.web import div, input_, label
from invent.ui.core import (
    Widget,
    TextProperty,
    ListProperty,
    ChoiceProperty,
    Event,
)
from invent.ui.core.measures import PURPOSES


class ButtonGroup(Widget):
    """
    A button group widget for the Invent framework.

    Button groups are a way of grouping buttons together, often with a shared
    purpose and as a more pleasing alternative to radio buttons. They consist
    of a set of buttons, only one of which can be active at a time. The active
    button is visually distinct from the others, and indicates the current
    selection.

    The possible values of the button group are defined by the choices
    property. When a button is pressed, the value of the button group is
    updated to match the value of the button that was pressed.

    The button group also emits a change event when the value changes, which
    can be used to trigger other actions in the application.

    Button groups can be styled in the same way as regular buttons, with size
    and purpose properties. The buttons within the group will inherit these
    styles, but the active button will also have an additional "active" style
    to indicate that it is the currently selected option.
    """

    choices = ListProperty(_("The options from which to select."))

    value = TextProperty(
        _("The currently selected option."),
        default_value=None,
    )

    group = TextProperty(
        _("The group to which the button-group belongs."),
        default_value="",
    )

    size = ChoiceProperty(
        _("The size of the buttons."),
        default_value="MEDIUM",
        choices=["LARGE", "MEDIUM", "SMALL"],
        group="style",
    )

    purpose = ChoiceProperty(
        _("The buttons' purpose."),
        default_value="DEFAULT",
        choices=PURPOSES,
        group="style",
    )

    changed = Event(
        _("Sent when the selected option changes."),
        value=_("The new value of the button group."),
    )

    # Holds the radio/label pair against the relevant choice value for easy
    # access when updating things.
    _items = OrderedDict()

    def _build_pair(self, index, choice):
        """
        Build and return a (radio, button_label) pair for a single choice.

        The radio input is visually hidden; the button_label acts as the
        visible, clickable button. The CSS :checked + label selector
        drives the active-state appearance.
        """
        button_id = f"{self.group}-{index}"
        radio = input_(
            type="radio",
            name=self.group,
            id=button_id,
            value=choice,
            classes=["invent-btn-check"],
        )
        if choice == self.value:
            radio.checked = True
        radio.addEventListener("change", create_proxy(self._on_radio_change))
        button_label = label(choice, for_=button_id, classes=["invent-btn"])
        return radio, button_label

    def on_choices_changed(self):
        """
        Rebuild all radio/label pairs when the choices list changes.
        """
        self.element.replaceChildren()
        self._items = OrderedDict()
        for i, choice in enumerate(self.choices):
            radio, button_label = self._build_pair(i, choice)
            self.element.append(radio)
            self.element.append(button_label)
            self._items[choice] = (radio, button_label)

    def on_group_changed(self):
        """
        Update name and id on all radio inputs when the group changes.
        """
        for i, (radio_element, label_element) in enumerate(
            self._items.values()
        ):
            button_id = f"{self.group}-{i}"
            radio_element.name = self.group
            radio_element.id = button_id
            label_element.for_ = button_id

    def on_value_changed(self):
        """
        Sync radio checked state when value is set programmatically.
        """
        for choice, (radio, _) in self._items.items():
            radio.checked = choice == self.value

    def on_size_changed(self):
        """Update the size class on the group when size changes."""
        self.element.classList.remove("large")
        self.element.classList.remove("small")
        if self.size == "LARGE":
            self.element.classList.add("large")
        elif self.size == "SMALL":
            self.element.classList.add("small")

    def on_purpose_changed(self):
        """Update the purpose class on the group when purpose changes."""
        self.element.classList.remove("primary")
        self.element.classList.remove("secondary")
        self.element.classList.remove("success")
        self.element.classList.remove("warning")
        self.element.classList.remove("danger")
        if self.purpose == "PRIMARY":
            self.element.classList.add("primary")
        elif self.purpose == "SECONDARY":
            self.element.classList.add("secondary")
        elif self.purpose == "SUCCESS":
            self.element.classList.add("success")
        elif self.purpose == "WARNING":
            self.element.classList.add("warning")
        elif self.purpose == "DANGER":
            self.element.classList.add("danger")

    def _on_radio_change(self, event):
        """Handle a radio change, updating value and emitting change."""
        new_value = event.target.value
        self.value = new_value
        self.publish(self.changed, value=new_value)

    def render(self):
        """
        Render the button group as a div containing hidden radio inputs
        and visible labels styled as buttons for each choice.

        Active state is driven by the CSS :checked + label selector.
        """
        element = div(classes=["invent-btn-group"], role="group")
        return element
