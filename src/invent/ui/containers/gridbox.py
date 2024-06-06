from ..core import Container
from .grid import set_position


class GridBox(Container):
    def render(self):
        element = super().render()
        element.style.display = "grid"
        return element


class Column(GridBox):
    """
    A vertical container box.
    """

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M104 32H64a16 16 0 0 0-16 16v160a16 16 0 0 0 16 16h40a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16m0 176H64V48h40Zm88-176h-40a16 16 0 0 0-16 16v160a16 16 0 0 0 16 16h40a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16m0 176h-40V48h40Z"/></svg>'  # noqa

    def update_child(self, child, index):
        child.element.style.setProperty("grid-column", 1)
        child.element.style.setProperty("grid-row", index)
        set_position(child.element, child.position)


class Row(GridBox):
    """
    A horizontal container box.
    """

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M208 136H48a16 16 0 0 0-16 16v40a16 16 0 0 0 16 16h160a16 16 0 0 0 16-16v-40a16 16 0 0 0-16-16m0 56H48v-40h160zm0-144H48a16 16 0 0 0-16 16v40a16 16 0 0 0 16 16h160a16 16 0 0 0 16-16V64a16 16 0 0 0-16-16m0 56H48V64h160z"/></svg>'  # noqa

    def update_children(self):
        self._update_template_columns()
        super().update_children()

    def update_child(self, child, index):
        child.element.style.setProperty("grid-column", index)
        child.element.style.setProperty("grid-row", 1)
        set_position(child.element, child.position)

    def _update_template_columns(self):
        template_columns = []
        for item in self.content:
            if (
                item.element.classList.contains("drop-zone")
                and len(self.content) > 1
            ):
                template_columns.append("0px")
            else:
                template_columns.append("auto")

        self.element.style.gridTemplateColumns = " ".join(template_columns)
