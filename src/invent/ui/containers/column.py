from pyscript import document
from ..core import Container


class Column(Container):
    """
    A vertical container box.
    """

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M104 32H64a16 16 0 0 0-16 16v160a16 16 0 0 0 16 16h40a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16m0 176H64V48h40Zm88-176h-40a16 16 0 0 0-16 16v160a16 16 0 0 0 16 16h40a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16m0 176h-40V48h40Z"/></svg>'  # noqa

    def create_child_wrapper(self, child, index):
        """
        Wrap the child element in a div with grid styles set appropriately.
        """
        child_wrapper = document.createElement("div")
        child_wrapper.style.setProperty("grid-column", 1)
        child_wrapper.style.setProperty("grid-row", index)
        child_wrapper.appendChild(child.element)
        child.set_position(child_wrapper)

        return child_wrapper

    def update_child_wrapper(self, child, index):
        """
        Wrap the child element in a div with grid styles set appropriately.
        """
        child_wrapper = child.element.parentElement
        child_wrapper.style.setProperty("grid-column", 1)
        child_wrapper.style.setProperty("grid-row", index)
        child_wrapper.appendChild(child.element)
        child.set_position(child_wrapper)
