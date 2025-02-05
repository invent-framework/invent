from pyscript import document

from .base import Widget


class Box(Widget):

    def render(self):
        element = document.createElement("div")
        element.style.display = "flex"
        # flex-direction (row/column) is handled in pack.py.
        return element