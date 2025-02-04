from pyscript import document

from . import stub_methods
from .app import App


class Window:

    def __init__(self, interface, title, position, size):
        self.interface = interface
        self.element = document.querySelector(interface.id)
        if not self.element:
            raise ValueError(f"no element matching {interface.id!r}")
        self.content = None

    def set_content(self, widget):
        if self.content:
            self.element.removeChild(content)
        if widget:
            self.element.appendChild(widget.element)
        self.content = widget


stub_methods(Window, "create_toolbar", "set_app")
