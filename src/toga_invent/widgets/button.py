from pyscript import document
from pyscript.ffi import create_proxy

from .base import Widget


class Button(Widget):

    def render(self):
        element = document.createElement("button")
        element.addEventListener("click", create_proxy(self.click))
        element.className = f"btn-{self.interface.purpose.lower()}"
        return element

    def click(self, event):
        self.interface.on_press()

    def get_text(self):
        return self.element.innerText

    def set_text(self, text):
        self.element.innerText = text

    def set_icon(self, icon):
        pass
