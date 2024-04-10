from pyscript import document
from pyscript.ffi import create_proxy

from .base import Widget


class TextInput(Widget):

    def render(self):
        return document.createElement("input")

    def get_value(self):
        return self.element.value

    def set_value(self, value):
        self.element.value = value

    def set_readonly(self, value):
        self.element.readOnly = value

    def set_placeholder(self, value):
        self.element.placeholder = value
