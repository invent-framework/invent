"""
A minimal button.
"""

from invent.ui.core import Widget, TextProperty, MessageBlueprint
from pyscript import document


class Button(Widget):
    label = TextProperty("The text on the button.", default_value="Click Me")
    size = ChoiceField("The size of the button.", default_value="MEDIUM", choices=["LARGE", "MEDIUM", "SMALL"])
    purpose = ChoiceField("The button's purpose.", default_value="DEFAULT", choices=["DEFAULT", "PRIMARY", "SECONDARY", "SUCCESS", "WARNING", "DANGER"])

    press = MessageBlueprint(
        "Sent when the button is pressed.",
        button="The button that was clicked.",
    )

    @classmethod
    def preview(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M216 40H40a16 16 0 0 0-16 16v144a16 16 0 0 0 16 16h176a16 16 0 0 0 16-16V56a16 16 0 0 0-16-16m0 160H40V56h176z"/></svg>'  # noqa

    def click(self, event):
        self.publish("press", button=self.name)

    def on_label_changed(self):
        self.element.innerText = self.label

    def on_size_changed(self):
        # Reset
        self.element.classList.remove("btn-large")
        self.element.classList.remove("btn-small")
        if self.size == "LARGE":
            self.element.classList.add("btn-large")
        elif self.size == "SMALL":
            self.element.classList.add("btn-small")

    def on_purpose_changed(self):
        # Reset
        self.element.classList.remove("btn-primary")
        self.element.classList.remove("btn-secondary")
        self.element.classList.remove("btn-success")
        self.element.classList.remove("btn-warning")
        self.element.classList.remove("btn-danger")
        if self.purpose == "PRIMARY":
            self.element.classList.add("btn-primary")
        elif self.purpose == "SECONDARY":
            self.element.classList.add("btn-secondary")
        elif self.purpose == "SUCCESS":
            self.element.classList.add("btn-success")
        elif self.purpose == "WARNING":
            self.element.classList.add("btn-warning")
        elif self.purpose == "DANGER":
            self.element.classList.add("btn-danger")

    def render(self):
        element = document.createElement("button")
        element.id = self.id
        element.innerText = self.label
        element.addEventListener("click", self.click)
        return element
