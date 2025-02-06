from pyscript import document

from .base import Widget


class Grid(Widget):
    def render(self):
        return document.createElement("div")

    def refresh(self):
        super().refresh()
        self.element.style.display = "grid"
