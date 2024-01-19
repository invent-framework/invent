"""
Core classes relating to the user interface aspects of the Invent framework.

Based on original pre-COVID work by [Nicholas H.Tollervey.](https://ntoll.org/)

Copyright (c) 2024 Invent contributors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from pyscript import document
from .utils import random_id


#: Valid flags for horizontal positions.
_VALID_HORIZONTALS = {"LEFT", "CENTER", "RIGHT"}
#: Valid flags for vertical positions.
_VALID_VERTICALS = {"TOP", "MIDDLE", "BOTTOM"}


class Widget:
    """
    All widgets have these things:

    * A mandatory unique human friendly name that's meaningful in the context
      of the application.
    * A unique id (if none is given, one is automatically generated).
    * An indication of the widget's preferred position (default: top left).
    * A render_into function that takes the widget's container and renders
      itself as an HTML element into the container.
    * An optional channel name to which it broadcasts its messages (defaults to
      the id)
    """

    def __init__(self, name, id=None, position="TOP-LEFT", channel=None):
        self.name = name
        self.id = id if id else random_id()
        self.channel = channel if channel else self.id
        self.position = position
        # Reference to the HTML element (once rendered).
        self.element = None

    def render_into(self, container):
        raise NotImplementedError()  # pragma: no cover

    def set_position(self, container):
        """
        Given the value of self.position, will adjust the CSS for the rendered
        self.element, and its container, so the resulting HTML puts the element
        into the expected position in the container.
        """
        pos = self.position.upper()
        if pos == "FILL":
            # Fill the full extent of the container.
            self.element.style.width = "100%"
            self.element.style.height = "100%"
            return
        # Parse the position as: "VERTICAL-HORIZONTAL", "VERTICAL" or
        # "HORIZONTAL" values.
        # Valid values are defined in _VALID_VERTICALS and _VALID_HORIZONTALS.
        definition = pos.split("-")
        # Default values for the horizontal and vertical positions.
        horizontal_position = None
        vertical_position = None
        if len(definition) == 1:
            # Unary position (e.g. "TOP" or "CENTER")
            unary_position = definition[0]
            if unary_position in _VALID_HORIZONTALS:
                horizontal_position = unary_position
            elif unary_position in _VALID_VERTICALS:
                vertical_position = unary_position
        elif len(definition) == 2:
            # Binary position (e.g. "TOP-CENTER" or "BOTTOM-RIGHT")
            if definition[0] in _VALID_VERTICALS:
                vertical_position = definition[0]
            if definition[1] in _VALID_HORIZONTALS:
                horizontal_position = definition[1]
        if not (horizontal_position or vertical_position):
            # Bail out if we don't have a valid position state.
            raise ValueError(f"'{self.position}' is not a valid position.")
        # Check vertical position and adjust the container via CSS magic.
        if vertical_position == "TOP":
            container.style["align-self"] = "start"
        elif vertical_position == "MIDDLE":
            container.style["align-self"] = "center"
        elif vertical_position == "BOTTOM":
            container.style["align-self"] = "end"
        # Check the horizontal position and adjust the container.
        if horizontal_position == "LEFT":
            container.style["justify-self"] = "start"
        elif horizontal_position == "CENTER":
            container.style["justify-self"] = "center"
        elif horizontal_position == "RIGHT":
            container.style["justify-self"] = "end"
        # Ensure a unary vertical only position ensures a full horizontal fill.
        if not horizontal_position:
            container.style["justify-self"] = "stretch"
            self.element.style.width = "100%"
        # Ensure a unary horizontal only position ensures a full vertical fill.
        if not vertical_position:
            container.style["align-self"] = "stretch"
            self.element.style.height = "100%"


class Container(list):
    """
    All containers have these things:

    * A mandatory unique human friendly name that's meaningful in the context
      of the application.
    * A unique id (if none is given, one is automatically generated).
    * Is a list of children (that are either widgets or further containers).
    * A notion of relative width/height to the containing element (defaults
      100%).
    * A render function that returns an HTML element representing the
      container to insert into the DOM. Child classes override this method to
      insert the children into the container in the correct manner.
    """

    def __init__(
        self,
        name,
        id=None,
        children=None,
        width=100,
        height=100,
        background_color=None,
        border_color=None,
        border_width=None,
        border_style=None,
    ):
        self.name = name
        # To reference the div in the DOM that renders this container.
        self._container = None
        self.id = id if id else random_id()
        self.parent = None
        self.width = width
        self.height = height
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_style = border_style

    def append(self, item):
        item.parent = self
        super().append(item)

    def render(self):
        """
        Return a div element representing the container (set with the expected
        height and width).

        Sub classes should call this, then override with the specific details
        for how to add their children in a way that reflects the way they
        layout their widgets.
        """
        if not self._container:
            self._container = document.createElement("div")
            self._container.id = self.id
            self._container.style.display = "grid"
        self._container.style.height = f"{self.height}%"
        self._container.style.width = f"{self.width}%"
        self._container.style["background-color"] = self.background_color
        self._container.style["border-color"] = self.border_color
        self._container.style["border-width"] = self.border_width
        self._container.style["border-style"] = self.border_style
        # TODO: Add children via sub-class.
        return self._container


class Column(Container):
    """
    A vertical container box.
    """

    def render(self):
        super().render()
        for counter, child in enumerate(self, start=1):
            child_container = document.createElement("div")
            child_container.style["grid-column"] = 1
            child_container.style["grid-row"] = counter
            child.render_into(child_container)
            self._container.appendChild(child_container)
        return self._container


class Row(Container):
    """
    A horizontal container box.
    """

    def render(self):
        super().render()
        for counter, child in enumerate(self, start=1):
            child_container = document.createElement("div")
            child_container.style["grid-column"] = counter
            child_container.style["grid-row"] = 1
            child.render_into(child_container)
            self._container.appendChild(child_container)
        return self._container
