from pyscript import document

from .base import Widget


class Box(Widget):
    def render(self):
        return document.createElement("div")

    def refresh(self):
        super().refresh()
        self.element.style.display = "flex"
        # flex-direction (row/column) is handled in pack.py.
