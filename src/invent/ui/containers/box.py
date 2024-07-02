from ...compatability import capitalize
from ..core import Container, ChoiceProperty, TextProperty
from ..core.component import _TSHIRT_SIZES, ALIGNMENTS


def justify_content_property(direction):
    return ChoiceProperty(
        f"{capitalize(direction)} alignment of children.",
        choices=ALIGNMENTS,
        default_value="start",
        map_to_style="justify-content"
    )


def flex_property(direction):
    # TODO: validate input
    return TextProperty(
        f"How much {direction} space to consume. " +
        "May be blank to take no extra space, "
        "'auto' to take an equal portion of any free space, "
        "or an integer to take the given proportion of the total space.",
        map_to_style="flex",
    )


class Box(Container):
    """
    Common base class for Row and Column.
    """

    gap = ChoiceProperty(
        "The gap between items in the container",
        choices=_TSHIRT_SIZES,
        default_value="M",
    )

    def render(self):
        element = super().render()
        element.style.display = "flex"
        element.style.flexDirection = self.flex_direction
        return element

    def on_gap_changed(self):
        """
        Set the gap between elements in the container (translating from t-shirt
        sizes).
        """
        self._set_gap(self.gap, "gap")
