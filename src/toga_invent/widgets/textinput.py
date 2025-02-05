from pyscript import document
from pyscript.ffi import create_proxy

from .base import Widget


class TextInput(Widget):

    def render(self):
        element = document.createElement("input")
        element.addEventListener("input", create_proxy(self.input))
        return element

    def input(self, event):
        self.interface.on_change()

    def get_value(self):
        return self.element.value

    def set_value(self, value):
        self.element.value = value
        self.input(None)

    def get_readonly(self):
        return self.element.readOnly

    def set_readonly(self, value):
        self.element.readOnly = value

    def get_placeholder(self):
        return self.element.placeholder

    def set_placeholder(self, value):
        self.element.placeholder = value
