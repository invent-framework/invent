from ..core import BooleanProperty, Container
from ..core.component import ALIGNMENTS, ALIGNMENTS_STRETCH


align_items_kwargs = dict(
    choices=ALIGNMENTS_STRETCH,
    default_value="stretch",
    map_to_style="align-items"
)

justify_content_kwargs = dict(
    choices=ALIGNMENTS,
    default_value="start",
    map_to_style="justify-content"
)


class Box(Container):
    """
    Common base class for Row and Column.
    """
    def render(self):
        element = super().render()
        element.style.display = "flex"
        element.style.flexDirection = self.flex_direction
        return element

    flex_wrap = BooleanProperty(
        "Whether children can wrap onto multiple lines",
        default_value=False,
    )

    def on_flex_wrap_changed(self):
        self.element.style.flexWrap = "wrap" if self.flex_wrap else ""
