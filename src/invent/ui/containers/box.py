from ..core import Container


class Box(Container):
    def render(self):
        element = super().render()
        element.style.display = "grid"
        return element
