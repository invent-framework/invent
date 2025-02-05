from pyscript import document

from .base import Widget


class Grid(Widget):

    def render(self):
        element = document.createElement("div")
        element.style.display = "grid"
        return element

    def get_columns(self):
        return self.element.style.columns

    def set_columns(self, value):
        self.element.style.columns = value
