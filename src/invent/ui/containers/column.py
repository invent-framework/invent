from ..core.component import align_self_property, BaseLayout
from .box import Box, flex_property, justify_content_property


class Column(Box):
    """
    A vertical container box.
    """

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M104 32H64a16 16 0 0 0-16 16v160a16 16 0 0 0 16 16h40a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16m0 176H64V48h40Zm88-176h-40a16 16 0 0 0-16 16v160a16 16 0 0 0 16 16h40a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16m0 176h-40V48h40Z"/></svg>'  # noqa

    flex_direction = "column"

    justify_content = justify_content_property("vertical")

    class Layout(BaseLayout):
        align_self = align_self_property("horizontal")
        flex = flex_property("vertical")
