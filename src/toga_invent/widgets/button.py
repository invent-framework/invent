from pyscript import document
from pyscript.ffi import create_proxy

from .base import Widget


class Button(Widget):
    def render(self):
        element = document.createElement("button")
        element.addEventListener("click", create_proxy(self.click))
        return element

    def click(self, event):
        self.interface.on_press()

    def get_text(self):
        return self.element.innerText

    def set_text(self, text):
        self.element.innerText = text

    def get_icon(self):
        return None

    def set_icon(self, icon):
        pass

    def get_purpose(self):
        return self._purpose

    def set_purpose(self, purpose):
        self._purpose = purpose
        self.element.className = f"btn-{purpose.lower()}"
