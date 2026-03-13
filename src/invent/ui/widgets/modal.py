"""
A modal container. This is a box that appears above the main content, often
with a backdrop, and is used for things like popups and more complicated alerts.

The modal is always activated by a trigger button. The trigger button is a child
of the modal, and is used to open the modal when clicked. Only the trigger button
will be visible in the location in which the modal is placed in the page layout.

Once triggered, the modal will appear as a layer above the main content, with a
backdrop behind it. The modal can be dismissed by clicking outside of it, or by
clicking a dismiss button within the modal.

A modal, like all containers, can contain any other components. This ensures a
wide variety of use cases can be met, from simple alerts to complex modals with
forms and other interactive content.

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
from invent.ui.core import Widget, TextProperty, ChoiceProperty, Event
from invent.ui.widgets.button import Button
from invent.ui.containers import Column
from invent.ui.core.measures import PURPOSES
from pyscript.web import button, div, page
from pyscript.ffi import create_proxy


class Modal(Widget):
    """
    A modal container. This is a box that appears above the main content,
    often with a backdrop, and is used for things like popups and more
    complicated alerts.

    The modal is always activated by a trigger button. The trigger button
    is a child of the modal, and is used to open the modal when clicked.
    Only the trigger button will be visible in the location in which the
    modal is placed in the page layout.

    Once triggered, the modal will appear as a layer above the main
    content, with a backdrop behind it. The modal can be dismissed by
    clicking outside of it, or by clicking a dismiss button within the
    modal.

    A modal, like all containers, can contain any other components. This
    ensures a wide variety of use cases can be met, from simple alerts to
    complex modals with forms and other interactive content.
    """

    trigger_button = Button()

    modal = Column()

    text = TextProperty(_("The text on the button."), default_value="Click Me")
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

    open = Event(
        _("Sent when the button is pressed."),
        button=_("The button that was clicked."),
        modal=_("The modal that was opened."),
    )

    close = Event(
        _("Sent when the modal is dismissed."),
        modal=_("The modal that was closed."),
    )

    on_text_changed = trigger_button.on_text_changed
    on_size_changed = trigger_button.on_size_changed
    on_purpose_changed = trigger_button.on_purpose_changed

    def __init__(self, **kwargs):
        kids = kwargs.pop("children", [])
        super().__init__(**kwargs)
        self.modal.children = kids
        self.trigger_button.parent = self
        self.modal.parent = self

    def close_modal(self, event=None):
        """
        If it exists, remove the backdrop from the DOM and signal closure.
        """
        if hasattr(self, "backdrop"):
            self.backdrop.remove()
            self.publish("close", modal=self)

    def open_modal(self, event):
        """
        Render the modal's content into a div, then display it as a layer
        above the main content, with a backdrop behind it. The modal can
        be dismissed by clicking outside of it, or by clicking a dismiss
        button ("X") within the modal.

        Publish the "open" event, passing the trigger button and the modal
        itself as arguments.

        Ensure closing the modal publishes the "close" event, passing the
        modal as an argument.
        """
        self.publish("open", button=self.trigger_button, modal=self)

        # Dismiss ("×") button anchored to the modal's top-right corner.
        dismiss = button("×")
        dismiss.classList.add("dismiss")
        dismiss.setAttribute("aria-label", _("Close"))
        dismiss.addEventListener(
            "click", create_proxy(lambda e: self.close_modal())
        )

        # The modal box: a dialog floating above the backdrop.
        modal_box = div()
        modal_box.classList.add("invent-modal")
        modal_box.setAttribute("role", "dialog")
        modal_box.setAttribute("aria-modal", "true")
        modal_box.append(dismiss)
        modal_box.append(self.modal.element)
        # Prevent clicks inside the box bubbling up to the backdrop.
        modal_box.addEventListener(
            "click",
            create_proxy(lambda e: e.stopPropagation()),
        )

        # The backdrop: a full-viewport overlay; clicking it closes the
        # modal.
        self.backdrop = div()
        self.backdrop.classList.add("invent-modal-backdrop")
        self.backdrop.append(modal_box)
        self.backdrop.addEventListener(
            "click", create_proxy(lambda e: self.close_modal())
        )

        page.body.append(self.backdrop)

    def render(self):
        # Render the modal content into a div, but don't add it to the DOM yet.
        self.modal.render()
        # Only the trigger button is placed in the normal page flow.
        element = self.trigger_button.render()
        element.addEventListener("click", create_proxy(self.open_modal))
        return element
