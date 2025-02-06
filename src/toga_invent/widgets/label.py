from pyscript import document

from .base import Widget


class Label(Widget):
    def render(self):
        return document.createElement("div")

    def get_text(self):
        return self.element.innerText

    def set_text(self, value):
        self.element.innerText = value
