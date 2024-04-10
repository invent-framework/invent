from pyscript import document

from .base import Widget


class Box(Widget):

    def render(self):
        return document.createElement("div")

    def refresh(self):
        super().refresh()

        # Hidden elements are given `display: none` by the superclass.
        if not self.element.style.display:
            self.element.style.display = "flex"
