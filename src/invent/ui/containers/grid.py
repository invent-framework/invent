from pyscript import document
from ..core import Container, IntegerProperty


class Grid(Container):
    """
    A grid.
    """

    columns = IntegerProperty("Number of columns", 4)
    column_gap = IntegerProperty("Space between columns", 0)
    row_gap = IntegerProperty("Space between rows", 0)

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M216 48H40a16 16 0 0 0-16 16v128a16 16 0 0 0 16 16h176a16 16 0 0 0 16-16V64a16 16 0 0 0-16-16m-112 96v-32h48v32Zm48 16v32h-48v-32ZM40 112h48v32H40Zm64-16V64h48v32Zm64 16h48v32h-48Zm48-16h-48V64h48ZM88 64v32H40V64Zm-48 96h48v32H40Zm176 32h-48v-32h48z"/></svg>'  # noqa

    def on_columns_changed(self):
        self.element.style.gridTemplateColumns = "auto " * self.columns

    def render(self):
        """
        Render the component.
        """
        element = document.createElement("div")
        element.style.display = "grid"
        element.style.gridTemplateColumns = "auto " * self.columns
        element.style.columnGap = self.column_gap
        element.style.rowGap = self.row_gap
        element.classList.add(f"invent-{type(self).__name__.lower()}")

        # Render the container's children.
        self.render_children(element)

        # Implementation detail: add child elements in the child class's own
        # render method. See Column and Row classes for examples of this.
        return element

    def create_child_wrapper(self, child, index):
        """
        Wrap the child element in a div with grid styles set appropriately.
        """
        child_wrapper = document.createElement("div")

        grid_row_span = child.row_span
        if grid_row_span:
            child_wrapper.style.gridRow = "span " + str(grid_row_span)

        grid_column_span = child.column_span
        if grid_column_span:
            child_wrapper.style.gridColumn = "span " + str(grid_column_span)

        child_wrapper.appendChild(child.element)
        child.set_position(child_wrapper)

        return child_wrapper

    def update_child_wrapper(self, child, index):
        """
        Wrap the child element in a div with grid styles set appropriately.
        """
        child_wrapper = child.element.parentElement
        grid_row_span = child.row_span
        if grid_row_span:
            child_wrapper.style.gridRow = "span " + str(grid_row_span)

        grid_column_span = child.column_span
        if grid_column_span:
            child_wrapper.style.gridColumn = "span " + str(grid_column_span)

        child_wrapper.appendChild(child.element)
        child.set_position(child_wrapper)
