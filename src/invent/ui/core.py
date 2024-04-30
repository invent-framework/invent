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

import invent
from invent.compatability import getmembers_static
from invent.i18n import _
from .properties import (
    BooleanProperty,
    ChoiceProperty,
    IntegerProperty,
    ListProperty,
    Property,
    TextProperty,
)


#: Valid flags for horizontal positions.
_VALID_HORIZONTALS = {"LEFT", "CENTER", "RIGHT"}
#: Valid flags for vertical positions.
_VALID_VERTICALS = {"TOP", "MIDDLE", "BOTTOM"}
#: T-shirt sizes used to indicate relative sizes of things.
_TSHIRT_SIZES = (
    None,
    "XS",
    "S",
    "M",
    "L",
    "XL",
)
#: The default icon for a component. https://github.com/phosphor-icons/core
_DEFAULT_ICON = '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M140 180a12 12 0 1 1-12-12a12 12 0 0 1 12 12M128 72c-22.06 0-40 16.15-40 36v4a8 8 0 0 0 16 0v-4c0-11 10.77-20 24-20s24 9 24 20s-10.77 20-24 20a8 8 0 0 0-8 8v8a8 8 0 0 0 16 0v-.72c18.24-3.35 32-17.9 32-35.28c0-19.85-17.94-36-40-36m104 56A104 104 0 1 1 128 24a104.11 104.11 0 0 1 104 104m-16 0a88 88 0 1 0-88 88a88.1 88.1 0 0 0 88-88"/></svg>'  # noqa


class MessageBlueprint:
    """
    An instance of this class represents a type of message potentially
    triggered in the life-cycle of a Widget object. The name assigned in the
    parent class definition should become the message's subject (an
    implementation detail left to the author of the Widget class).

    E.g.:

    click = MessageBlueprint("Sent when the widget it clicked.")
    hold = MessageBlueprint(
        "The button is held down.",
        duration="The amount of time the button was held down.",
    )
    double_click = MessageBlueprint()

    Instances may have an optional description to explain their intent, and
    key/value pairs describing the fields in the content of the message. This
    metadata is used in the visual builder.
    """

    def __init__(self, description=None, **kwargs):
        """
        Messages may have an optional description and key/value pairs
        describing the expected content of future messages.
        """
        self.description = description
        self.content = kwargs

    def create_message(self, name, **kwargs):
        """
        Returns an actual message to send to channels with the given content.

        Validates kwargs match the fields described in the blueprint's content
        specification.
        """
        for k in kwargs:
            if k not in self.content:
                raise ValueError(_("Unknown field in message content: ") + k)
        for k in self.content:
            if k not in kwargs:
                raise ValueError(_("Field missing from message content:") + k)
        return invent.Message(name, **kwargs)

    def as_dict(self):
        """
        Return a dictionary representation of the meta-data contained within
        this class.
        """
        return {
            "description": self.description,
            "content": self.content,
        }


class Component:
    """
    A base class for all user interface components (Widget, Container).

    Ensures they all have optional names and ids. If they're not given, will
    auto-generate them for the user. The position of the component determines
    how it will be drawn in its parent.
    """

    # Used for quick component look-up.
    _components_by_id = {}
    # Used for generating unique component names.
    _component_counter = 0

    id = TextProperty("The id of the widget instance in the DOM.")
    name = TextProperty(
        "The meaningful name of the widget instance.",
        map_to_attribute="name",
    )
    enabled = BooleanProperty("Indicates if the component is enabled.")
    visible = BooleanProperty("The component is visible is set to True.")

    # Properties that are used by the container that a component is in.
    position = TextProperty(
        "The component's position inside it's parent.",
        default_value="FILL",
    )

    column_span = TextProperty(
        "The component's requested column-span in a grid",
        default_value="1",
    )

    row_span = TextProperty(
        "The component's requested row-span in a grid.",
        default_value="1",
    )

    def __init__(self, **kwargs):
        if invent.is_micropython:  # pragma: no cover
            # When in MicroPython, ensure all the properties have a reference
            # to their name within this class.
            for property_name, property_obj in type(self).properties().items():
                property_obj.__set_name__(self, property_name)
        self.element = self.render()
        self.update(**kwargs)
        type(self)._component_counter += 1
        if not self.id:
            self.id = type(self)._generate_unique_id()
        if not self.name:
            self.name = type(self)._generate_name()
        Component._components_by_id[self.id] = self
        # To reference the container's parent in the DOM tree.
        self.parent = None

    @property
    def is_container(self):
        """
        Return True if this component is a container, otherwise False.

        Just a convenience property in place of "isinstance".
        """
        return isinstance(self, Container)

    def update(self, **kwargs):
        """
        Given the **kwargs dict, iterate of the items and if the key identifies
        a property on this class, set the property's value to the associated
        value in the dict.
        """
        # Set values from the **kwargs
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
        # Set values from the property's own default_values.
        for property_name, property_obj in type(self).properties().items():
            if property_name not in kwargs:
                if property_obj.default_value is not None:
                    setattr(self, property_name, property_obj.default_value)

    def on_id_changed(self):
        """
        Automatically called to update the id of the HTML element associated
        with the component.
        """
        self.element.id = self.id

    def on_enabled_changed(self):
        """
        Ensure the underlying HTML element is enabled/disabled according to
        the value of the property.
        """
        self.element.disabled = not self.enabled

    def on_visible_changed(self):
        """
        Show / hide the element depending on the value of the property.
        """
        self.element.style.visibility = "visible" if self.visible else "hidden"

    def on_position_changed(self):
        """
        Automatically called to update the position information relating to
        the HTML element associated with the component.
        """
        if self.element.parentElement:
            self.set_position(self.element.parentElement)

    def on_column_span_changed(self):
        """
        Automatically called to update the column span information relating to
        the HTML element associated with the component.
        """
        if self.element.parentElement:
            self.parent.update_children()

    def on_row_span_changed(self):
        """
        Automatically called to update the row span information relating to
        the HTML element associated with the component.
        """
        if self.element.parentElement:
            self.parent.update_children()

    @classmethod
    def _generate_unique_id(cls):
        """
        Create a unique but meaningful id for the component.

        E.g.

        "invent-button-1"

        The pattern is "invent-classname-counter".
        """
        return f"invent-{cls.__name__.lower()}-{cls._component_counter}"

    @classmethod
    def _generate_name(cls):
        """
        Create a human friendly name for the component.

        E.g.

        "Button 1"
        """
        return f"{cls.__name__} {cls._component_counter}"

    @classmethod
    def get_component_by_id(cls, component_id):
        """
        Return the component with the specified id or None if no such
        component exists.
        """
        return Component._components_by_id.get(component_id)

    def render(self):
        """
        In base classes, return the HTML element used to display the
        component.
        """
        raise NotImplementedError()  # pragma: no cover

    @classmethod
    def icon(cls):
        """
        Return the SVG to display in the menu of available components in the
        UI builder.
        """
        return _DEFAULT_ICON

    @classmethod
    def properties(cls):
        """
        Returns a dictionary of properties associated with the component. The
        key is the property name, the value an instance of the relevant
        property class.

        Implementation detail: we branch on interpreter type because of the
        different behaviour of `getmembers`.
        """
        return {
            name: value
            for name, value in getmembers_static(cls)
            if isinstance(value, Property)
        }

    @classmethod
    def message_blueprints(cls):
        """
        Returns a dictionary of the message blueprints that define the sort of
        messages a component may send during its lifetime.

        Implementation detail: we branch on interpreter type because of the
        different behaviour of `getmembers`.
        """
        return {
            name: value
            for name, value in getmembers_static(cls)
            if isinstance(value, MessageBlueprint)
        }

    @classmethod
    def blueprint(cls):
        """
        Return a Python dictionary as a data structure representing all the
        essential information about the components, its properties, message
        blueprints and preview.
        """
        return {
            "name": cls.__name__,
            "properties": {
                name: prop.as_dict() for name, prop in cls.properties().items()
            },
            "message_blueprints": {
                key: value.as_dict()
                for key, value in cls.message_blueprints().items()
            },
            "icon": cls.icon(),
        }

    def as_dict(self):
        """
        Return a dict representation of the state of this instance's
        properties and message blueprints.
        """
        properties = {
            key: getattr(self, key) for key in type(self).properties()
        }

        return {
            "type": type(self).__name__,
            "properties": properties,
            "message_blueprints": {
                key: value.as_dict()
                for key, value in type(self).message_blueprints().items()
            },
        }

    def parse_position(self):
        """
        Parse "self.position" as: "VERTICAL-HORIZONTAL", "VERTICAL" or
        "HORIZONTAL" values.

        Valid values are defined in _VALID_VERTICALS and _VALID_HORIZONTALS.

        Returns a tuple of (vertical_position, horizontal_position). Each
        return value could be None.
        """
        definition = self.position.upper().split("-")
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
        return vertical_position, horizontal_position

    def set_position(self, container):
        """
        Given the value of "self.position", will adjust the CSS for the
        rendered "self.element", and its container, so the resulting HTML puts
        the element into the expected position in the container.
        """

        def reset():
            """
            Reset the style state for the component and its parent container.
            """
            self.element.style.removeProperty("width")
            self.element.style.removeProperty("height")
            container.style.removeProperty("align-self")
            container.style.removeProperty("justify-self")

        if self.position.upper() == "FILL":
            reset()
            # Fill the full extent of the container.
            self.element.style.width = "100%"
            self.element.style.height = "100%"
            return

        # Parse into horizontal and vertical positions.
        try:
            vertical_position, horizontal_position = self.parse_position()
            reset()
        except ValueError:
            return

        # Check vertical position and adjust the container via CSS magic.
        if vertical_position == "TOP":
            container.style.setProperty("align-self", "start")
        elif vertical_position == "MIDDLE":
            container.style.setProperty("align-self", "center")
        elif vertical_position == "BOTTOM":
            container.style.setProperty("align-self", "end")
        # Check the horizontal position and adjust the container.
        if horizontal_position == "LEFT":
            container.style.setProperty("justify-self", "start")
        elif horizontal_position == "CENTER":
            container.style.setProperty("justify-self", "center")
        elif horizontal_position == "RIGHT":
            container.style.setProperty("justify-self", "end")
        # Ensure a vertical only position ensures a full horizontal fill.
        if not horizontal_position:
            container.style.setProperty("justify-self", "stretch")
            self.element.style.width = "100%"
        # Ensure a horizontal only position ensures a full vertical fill.
        if not vertical_position:
            container.style.setProperty("align-self", "stretch")
            self.element.style.height = "100%"

    def update_attribute(self, attribute_name, attribute_value):
        """
        Convenience method to update an HTML attribute on self.element. If
        the attribute_value is false-y, the attribute is removed.
        Otherwise, the named attribute is set to the given value.
        """
        if attribute_value:
            self.element.setAttribute(attribute_name, str(attribute_value))
        else:
            self.element.removeAttribute(attribute_name)


class Widget(Component):
    """
    A widget is a UI component drawn onto the interface in some way.

    All widgets have these things:

    * A unique human friendly name that's meaningful in the context of the
      application (if none is given, one is automatically generated).
    * A unique id (if none is given, one is automatically generated).
    * An indication of the widget's preferred position.
    * A render function that takes the widget's container and renders
      itself as an HTML element into the container.
    * An optional indication of the channel[s] to which it broadcasts
      messages (defaults to the id).
    * A publish method that takes the name of a message blueprint, and
      associated kwargs, and publishes it to the channel[s] set for the
      widget.
    """

    channel = TextProperty(
        "A comma separated list of channels to which the widget broadcasts.",
        default_value=None,
    )

    def publish(self, blueprint, **kwargs):
        """
        Given the name of one of the class's MessageBlueprints, publish
        a message to all the widget's channels with the message content
        defined in kwargs.
        """
        # Ensure self.channel is treated as a comma-separated list of channel
        # names.
        if self.channel is not None:
            channels = [
                channel.strip()
                for channel in self.channel.split(",")
                if channel.strip()
            ]
            message = getattr(self, blueprint).create_message(
                blueprint, **kwargs
            )
            invent.publish(message, to_channel=channels)


class Container(Component):
    """
    All containers have these things:

    * A unique human friendly name that's meaningful in the context of the
      application (if none is given, one is automatically generated).
    * A unique id (if none is given, one is automatically generated).
    * Is a list of children (that are either widgets or further containers).
    * A notion of relative width/height to the containing element (defaults
      100%).
    * A render function that returns an HTML element representing the
      container to insert into the DOM. Child classes override this method to
      insert the children into the container in the correct manner.
    """

    content = ListProperty(
        "The contents of the container",
        default_value=None,
    )

    column_width = IntegerProperty(
        "The default width of the container.",
        default_value=100,
        maximum=100,
        minimum=0,
    )
    height = IntegerProperty(
        "The default height of the container.",
        default_value=100,
        maximum=100,
        minimum=0,
    )
    gap = ChoiceProperty(
        "The gap between items in the container",
        choices=_TSHIRT_SIZES,
        default_value="M",
    )
    background_color = TextProperty("The color of the container's background.")
    border_color = TextProperty("The color of the container's border.")
    border_width = ChoiceProperty(
        "The size of the container's border.",
        choices=_TSHIRT_SIZES,
    )
    border_style = ChoiceProperty(
        "The style of the container's border.",
        choices=[
            None,
            "Dotted",
            "Dashed",
            "Solid",
            "Double",
            "Groove",
            "Ridge",
            "Inset",
            "Outset",
        ],
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for item in self.content:
            item.parent = self

    def on_content_changed(self):
        self.element.innerHTML = ""
        self.render_children(self.element)

    def on_height_changed(self):
        self.element.style.height = f"{self.height}%"

    def on_width_changed(self):
        self.element.style.width = f"{self.width}%"

    def on_background_color_changed(self):
        if self.background_color:
            self.element.style.setProperty(
                "background-color", self.background_color
            )
        else:
            self.element.style.removeProperty("background-color")

    def on_border_color_changed(self):
        if self.border_color:
            self.element.style.setProperty("border-color", self.border_color)
        else:
            self.element.style.removeProperty("border-color")

    def on_border_width_changed(self):
        """
        Set the border with (transliating from t-shirt sizes).
        """
        sizes = {
            "XS": "2px",
            "S": "4px",
            "M": "8px",
            "L": "16px",
            "XL": "32px",
        }
        if self.border_width is not None:
            size = sizes[self.border_width.upper()]
            self.element.style.setProperty("border-width", size)
        else:
            self.element.style.removeProperty("border-width")

    def on_border_style_changed(self):
        if self.border_style:
            self.element.style.setProperty("border-style", self.border_style)
        else:
            self.element.style.removeProperty("border-style")

    def on_gap_changed(self):
        """
        Set the gap between elements in the container (translating from t-shirt
        sizes).
        """
        sizes = {
            "XS": "2px",
            "S": "4px",
            "M": "8px",
            "L": "16px",
            "XL": "32px",
        }
        size = "0px"

        if self.gap is not None:
            size = sizes[self.gap.upper()]
        self.element.style.setProperty("gap", size)

    def append(self, item):
        """
        Append like a list.
        """
        # Update the object model.
        item.parent = self
        self.content.append(item)

        # Update the DOM.
        self.element.appendChild(
            self.create_child_wrapper(item, len(self.content))
        )

        # Update the grid indices of the container's children.
        self.update_children()

    def insert(self, index, item):
        """
        Insert like a list.
        """
        # Update the object model.
        item.parent = self
        self.content.insert(index, item)

        # Update the DOM.
        #
        # We wrap all children in a <div> that is a grid area.
        wrapper = self.create_child_wrapper(item, index)
        if index == len(self.element.childNodes):
            self.element.appendChild(wrapper)

        else:
            self.element.insertBefore(wrapper, self.element.childNodes[index])

        # Update the grid indices of the container's children.
        self.update_children()

    def remove(self, item):
        """
        Remove like a list.
        """
        # Update the object model.
        item.parent = None
        self.content.remove(item)

        # Update the DOM.
        item.element.parentElement.remove()

        # Update the grid indices of the container's children.
        self.update_children()

    def __getitem__(self, index):
        """
        Index items like a list.
        """
        return self.content[index]

    def __iter__(self):
        """
        Iterate like a list.
        """
        return iter(self.content)

    def __delitem__(self, item):
        """
        Delete like a list.
        """
        self.remove(item)

    def contains(self, component):
        """Return True if the specified component is in this container.

        This is recursive, so this really means "is a descendant of".
        """
        for item in self.content:
            if item is component:
                return True

            if item.is_container:
                if item.contains(component):
                    return True

        return False

    def render(self):
        """
        Return a div element representing the container (set with the expected
        height and width).

        Subclasses should call this, then override with the specific details
        for how to add their children in a way that reflects the way they
        lay out their widgets.
        """
        element = document.createElement("div")
        element.style.display = "grid"
        element.classList.add(f"invent-{type(self).__name__.lower()}")

        # Render the container's children.
        #
        # See Column, Grid and Row classes for implementation details.
        self.render_children(element)

        return element

    def render_children(self, element):
        """
        Render the container's children.
        """
        for index, child in enumerate(self.content, start=1):
            element.appendChild(self.create_child_wrapper(child, index))

    def update_children(self):
        """
        Update the container's children.
        """
        for counter, child in enumerate(self.content, start=1):
            self.update_child_wrapper(child, counter)

    def as_dict(self):
        """
        Return a dict representation of the container, including the ordered
        content of children.
        """
        result = super().as_dict()
        result["properties"]["content"] = [
            child.as_dict() for child in self.content
        ]
        return result


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
        for item in self.content:
            if (
                item.element.classList.contains("drop-zone")
                and len(self.content) > 1
            ):
                template_columns.append("0px")

            else:
                template_columns.append("auto")

        element.style.gridTemplateColumns = " ".join(template_columns)
