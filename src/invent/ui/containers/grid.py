from ..core import Container, ChoiceProperty, IntegerProperty
from ..core.component import (
    _TSHIRT_SIZES,
    ALIGNMENTS_STRETCH,
    Layout,
    align_self_property,
)


class GridLayout(Layout):
    align_self = align_self_property("vertical")
    justify_self = ChoiceProperty(
        "Horizontal alignment.",
        choices=ALIGNMENTS_STRETCH,
        default_value="stretch",
        map_to_style="justify-self",
    )

    column_span = IntegerProperty("Number of columns to fill.", 1)
    row_span = IntegerProperty("Number of rows to fill.", 1)

    def on_column_span_changed(self):
        self.element.style.gridColumn = f"span {self.column_span}"

    def on_row_span_changed(self):
        self.element.style.gridRow = f"span {self.row_span}"


class Grid(Container):
    """
    A grid.
    """

    layout_class = GridLayout

    column_gap = ChoiceProperty(
        "The gap between columns in the grid.",
        choices=_TSHIRT_SIZES,
        default_value="M",
    )
    row_gap = ChoiceProperty(
        "The gap between rows in the grid.",
        choices=_TSHIRT_SIZES,
        default_value="M",
    )

    columns = IntegerProperty("Number of columns.", 4)

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M216 48H40a16 16 0 0 0-16 16v128a16 16 0 0 0 16 16h176a16 16 0 0 0 16-16V64a16 16 0 0 0-16-16m-112 96v-32h48v32Zm48 16v32h-48v-32ZM40 112h48v32H40Zm64-16V64h48v32Zm64 16h48v32h-48Zm48-16h-48V64h48ZM88 64v32H40V64Zm-48 96h48v32H40Zm176 32h-48v-32h48z"/></svg>'  # noqa

    def on_column_gap_changed(self):
        self._set_gap(self.column_gap, "column-gap")

    def on_row_gap_changed(self):
        self._set_gap(self.row_gap, "row-gap")

    def on_columns_changed(self):
        self.element.style.gridTemplateColumns = "auto " * self.columns

    def render(self):
        """
        Render the component.
        """
        element = super().render()
        element.style.display = "grid"
        return element
