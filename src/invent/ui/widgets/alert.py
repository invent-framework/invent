"""
An alert informs users of important information that requires their attention.
Alerts are typically used to display error messages, warnings, or other
important notifications. They can be used to provide feedback on user actions,
such as form submissions or system errors.

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
    ChoiceProperty,
    BooleanProperty,
    Event,
)
from invent.ui.core.measures import PURPOSES
from invent.utils import from_markdown
from pyscript.web import button, div, p


class Alert(Widget):
    """
    An alert informs users of important information that requires their attention.
    Alerts are typically used to display error messages, warnings, or other
    important notifications. They can be used to provide feedback on user actions,
    such as form submissions or system errors.

    If the dismissable property is set to True, the alert can be dismissed by the
    user by clicking on a close cross icon (thus removing the alert). When the alert
    is dismissed, the dismissed event is fired, which can be used to perform any
    necessary cleanup or actions in response to the dismissal.
    """

    title = TextProperty(_("The title of the alert."))
    text = TextProperty(_("The text to display in the alert."))
    purpose = ChoiceProperty(
        _("The purpose of the alert."),
        default_value="DEFAULT",
        choices=PURPOSES,
        group="style",
    )
    dismissable = BooleanProperty(
        _("Whether the alert can be dismissed by the user."),
        default_value=False,
    )
    dismissed = Event(_("An event that is fired when the alert is dismissed."))

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256"><path d="M236.8,188.09,149.35,36.22h0a24.76,24.76,0,0,0-42.7,0L19.2,188.09a23.51,23.51,0,0,0,0,23.72A24.35,24.35,0,0,0,40.55,224h174.9a24.35,24.35,0,0,0,21.33-12.19A23.51,23.51,0,0,0,236.8,188.09ZM222.93,203.8a8.5,8.5,0,0,1-7.48,4.2H40.55a8.5,8.5,0,0,1-7.48-4.2,7.59,7.59,0,0,1,0-7.72L120.52,44.21a8.75,8.75,0,0,1,15,0l87.45,151.87A7.59,7.59,0,0,1,222.93,203.8ZM120,144V104a8,8,0,0,1,16,0v40a8,8,0,0,1-16,0Zm20,36a12,12,0,1,1-12-12A12,12,0,0,1,140,180Z"></path></svg>'  # noqa

    def on_dismissed(self):
        """
        Handle the alert being dismissed by the user.
        """
        self.element.remove()
        self.publish(self.dismissed)

    def on_purpose_changed(self):
        """
        Update the alert's colour-scheme CSS variables.
        """
        if self.purpose == "DEFAULT":
            self.element.style.pop("--alert-bg", None)
            self.element.style["--alert-border-color"] = "var(--primary)"
        else:
            p = self.purpose.lower()
            self.element.style["--alert-bg"] = f"var(--{p}-light)"
            self.element.style["--alert-border-color"] = f"var(--{p})"

    def on_text_changed(self):
        """
        Update the alert's text content and visibility in the DOM.
        """
        self._text_el.innerHTML = from_markdown(self.text) or ""
        self.element.style["display"] = "block" if self.text else "none"

    def on_title_changed(self):
        """
        Update the alert's title text in the DOM.
        """
        self._title_el.textContent = self.title or ""

    def on_dismissable_changed(self):
        """
        Add or remove the dismiss button based on the dismissable property.
        """
        if self.dismissable:
            btn = button("✕")
            btn.setAttribute("aria-label", _("Dismiss"))
            btn.addEventListener("click", lambda e: self.on_dismissed())
            self.element.append(btn)
        else:
            for btn in self.element.querySelectorAll("button"):
                btn.remove()

    def render(self):
        """
        Build and return the root element for the alert widget.

        Stores refs to the title and text child elements so that
        the on_*_changed handlers can update them directly. If the
        alert is dismissable, appends a button wired via
        addEventListener that calls on_dismissed on click.
        """
        self._title_el = p(classes=["alert-title"])
        self._text_el = p()
        element = div(self._title_el, self._text_el, classes=["invent-alert"])
        element.setAttribute("role", "alert")
        return element
