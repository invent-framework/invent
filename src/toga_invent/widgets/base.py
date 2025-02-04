from abc import ABC, abstractmethod

from .. import stub_methods


class Widget(ABC):

    def __init__(self, interface):
        self.interface = interface
        self.element = self.render()

        # This property is unused because we handle layout using CSS.
        self.container = None

    @abstractmethod
    def render(self):
        raise NotImplementedError()

    def get_enabled(self):
        return not self.element.disabled

    def set_enabled(self, value):
        self.element.disabled = not value

    def refresh(self):
        self.element.style = self.interface.style.__css__()

    def add_child(self, child):
        self.element.appendChild(child.element)

    def insert_child(self, index, child):
        self.element.insertBefore(child.element, self.element.childNodes[index])

    def remove_child(self, child):
        self.element.removeChild(child.element)


stub_methods(
    Widget, *[f"set_{name}" for name in [
        "app", "window",

        # These setters are unused because we handle style using CSS.
        "bounds", "alignment", "hidden", "font", "color", "background_color",
    ]]
)
