from ..core import Container, IntegerProperty


#: Valid flags for horizontal positions.
_VALID_HORIZONTALS = {"LEFT", "CENTER", "RIGHT", "FILL"}
#: Valid flags for vertical positions.
_VALID_VERTICALS = {"TOP", "MIDDLE", "BOTTOM", "FILL"}


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
        element = super().render()
        element.style.display = "grid"
        element.style.gridTemplateColumns = "auto " * self.columns
        element.style.columnGap = self.column_gap
        element.style.rowGap = self.row_gap
        return element

    def update_child(self, child, index):
        grid_row_span = child.row_span
        if grid_row_span:
            child.element.style.gridRow = "span " + str(grid_row_span)

        grid_column_span = child.column_span
        if grid_column_span:
            child.element.style.gridColumn = "span " + str(grid_column_span)

        set_position(child.element, child.position)


def parse_position(position):
    """
    Parse "position" as: "VERTICAL-HORIZONTAL", "VERTICAL" or "HORIZONTAL"
    values.

    Valid values are defined in _VALID_VERTICALS and _VALID_HORIZONTALS.

    Returns a tuple of (vertical_position, horizontal_position). Missing or
    invalid values will be replaced by FILL.
    """
    definition = position.upper().split("-")
    # Default values for the horizontal and vertical positions.
    horizontal_position = "FILL"
    vertical_position = "FILL"
    if len(definition) == 1:
        # Unary position (e.g. "TOP" or "CENTER")
        unary_position = definition[0]
        if unary_position in _VALID_HORIZONTALS:
            horizontal_position = unary_position
        if unary_position in _VALID_VERTICALS:
            vertical_position = unary_position
    elif len(definition) == 2:
        # Binary position (e.g. "TOP-CENTER" or "BOTTOM-RIGHT")
        if definition[0] in _VALID_VERTICALS:
            vertical_position = definition[0]
        if definition[1] in _VALID_HORIZONTALS:
            horizontal_position = definition[1]
    return vertical_position, horizontal_position


def set_position(element, position):
    """
    Given the value of "position", will adjust the CSS for the rendered
    "element" so the resulting HTML puts the element into the expected position
    in its grid cell.
    """
    try:
        vertical_position, horizontal_position = parse_position(position)
    except ValueError:
        return

    if vertical_position == "TOP":
        element.style.setProperty("align-self", "start")
    elif vertical_position == "MIDDLE":
        element.style.setProperty("align-self", "center")
    elif vertical_position == "BOTTOM":
        element.style.setProperty("align-self", "end")
    elif vertical_position == "FILL":
        element.style.setProperty("align-self", "stretch")

    if horizontal_position == "LEFT":
        element.style.setProperty("justify-self", "start")
    elif horizontal_position == "CENTER":
        element.style.setProperty("justify-self", "center")
    elif horizontal_position == "RIGHT":
        element.style.setProperty("justify-self", "end")
    elif horizontal_position == "FILL":
        element.style.setProperty("justify-self", "stretch")
