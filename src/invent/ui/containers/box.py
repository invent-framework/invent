from ..core import Container, ChoiceProperty
from ..core.component import _TSHIRT_SIZES, ALIGNMENTS

justify_content_kwargs = dict(
    choices=ALIGNMENTS,
    default_value="start",
    map_to_style="justify-content"
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
