from pyscript import document
from ..core import Container


class Row(Container):
    """
    A horizontal container box.
    """

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M208 136H48a16 16 0 0 0-16 16v40a16 16 0 0 0 16 16h160a16 16 0 0 0 16-16v-40a16 16 0 0 0-16-16m0 56H48v-40h160zm0-144H48a16 16 0 0 0-16 16v40a16 16 0 0 0 16 16h160a16 16 0 0 0 16-16V64a16 16 0 0 0-16-16m0 56H48V64h160z"/></svg>'  # noqa

    def render_children(self, element):
        """
        Render the container's children.
        """
        self._update_template_columns(element)
        super().render_children(element)

    def update_children(self):
        """
        Update the container's children.
        """
        self._update_template_columns(self.element)
        super().update_children()

    def create_child_wrapper(self, child, index):
        """
        Wrap the child element in a div with grid styles set appropriately.
        """
        child_wrapper = document.createElement("div")
        child_wrapper.style.setProperty("grid-column", index)
        child_wrapper.style.setProperty("grid-row", 1)
        child_wrapper.appendChild(child.element)
        child.set_position(child_wrapper)

        return child_wrapper

    def update_child_wrapper(self, child, index):
        """
        Wrap the child element in a div with grid styles set appropriately.
        """
        child_wrapper = child.element.parentElement
        child_wrapper.style.setProperty("grid-column", index)
        child_wrapper.style.setProperty("grid-row", 1)
        child_wrapper.appendChild(child.element)
        child.set_position(child_wrapper)

    def _update_template_columns(self, element):
        """
        Update the container's template columns.
        """

        template_columns = []
        for item in self.children:
            if (
                item.element.classList.contains("drop-zone")
                and len(self.children) > 1
            ):
                template_columns.append("0px")

            else:
                template_columns.append("auto")

        element.style.gridTemplateColumns = " ".join(template_columns)
