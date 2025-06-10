"""
Core classes relating to the user interface aspects of the Invent framework.

Based on original pre-COVID work by [Nicholas H.Tollervey.](https://ntoll.org/)

Copyright (c) 2019-present Invent contributors.

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

import invent
from invent.utils import getmembers_static
from invent.i18n import _
from .property import (
    Property,
    BooleanProperty,
    ChoiceProperty,
    TextProperty,
    IntegerProperty,
)
from .event import Event
from .measures import TSHIRT_SIZES, GAP_SIZES, COMPONENT_DISTRIBUTION


#: The default icon for a component. https://github.com/phosphor-icons/core
_DEFAULT_ICON = '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M140 180a12 12 0 1 1-12-12a12 12 0 0 1 12 12M128 72c-22.06 0-40 16.15-40 36v4a8 8 0 0 0 16 0v-4c0-11 10.77-20 24-20s24 9 24 20s-10.77 20-24 20a8 8 0 0 0-8 8v8a8 8 0 0 0 16 0v-.72c18.24-3.35 32-17.9 32-35.28c0-19.85-17.94-36-40-36m104 56A104 104 0 1 1 128 24a104.11 104.11 0 0 1 104 104m-16 0a88 88 0 1 0-88 88a88.1 88.1 0 0 0 88-88"/></svg>'  # noqa


class Component:
    """
    A base class for all user interface components (Widget, Container).

    Ensures they all have optional names and ids. If they're not given, will
    auto-generate them for the user.
    """

    # Used for quick component look-up.
    _components_by_id = {}
    # Used for generating unique component names.
    _component_counter = 0

    id = TextProperty(_("The id of the component instance in the DOM."))

    name = TextProperty(
        _("The meaningful name of the component instance."),
        map_to_attribute="name",
    )

    enabled = BooleanProperty(
        _("Indicates if the component is enabled."), default_value=True
    )

    visible = BooleanProperty(
        _("The component is visible is set to True."), default_value=True
    )

    flex = TextProperty(
        _(
            "Sets how a component will grow or shrink (i.e. flex) to fit the "
            "space available. If blank won't stretch into available space, "
            "if 'auto' will stretch an equal portion of any available space, "
            "or an integer to stretch into the given proportion of the "
            "available space.",
        ),
        default_value=None,
        map_to_style="flex",
        group="layout",
    )

    column_span = IntegerProperty(
        _("Number of columns to fill in a grid container."),
        default_value=None,
        group="layout",
    )

    row_span = IntegerProperty(
        _("Number of rows to fill in a grid container."),
        default_value=None,
        group="layout",
    )

    horizontal_align = ChoiceProperty(
        _("The horizontal alignment of the widget."),
        choices=COMPONENT_DISTRIBUTION,
        group="layout",
    )

    vertical_align = ChoiceProperty(
        _("The vertical alignment of the widget."),
        choices=COMPONENT_DISTRIBUTION,
        group="layout",
    )

    background_color = TextProperty(
        _("The color of the component's background."), group="style"
    )

    border_color = TextProperty(
        _("The color of the component's border."), group="style"
    )

    border_width = ChoiceProperty(
        _("The size of the component's border."),
        choices=TSHIRT_SIZES,
        group="style",
    )

    border_style = ChoiceProperty(
        _("The style of the component's border."),
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
        group="style",
    )

    def __init__(self, **kwargs):
        if invent.is_micropython:  # pragma: no cover
            # When in MicroPython, ensure all the properties have a reference
            # to their name within this class.
            for property_name, property_obj in type(self).properties().items():
                property_obj.__set_name__(self, property_name)
        self.element = self.render()
        self._parent = None  # A reference to the parent container.
        self._parent_type = None  # Indicates the type of parent container.
        self.update(**kwargs)

        # Set default values.
        for property_name, property_obj in type(self).properties().items():
            if property_name not in kwargs:
                if property_obj.default_value is not None:
                    setattr(self, property_name, property_obj.default_value)

        type(self)._component_counter += 1
        if not self.id:
            self.id = type(self)._generate_unique_id()
        if not self.name:
            self.name = type(self)._generate_name()
        Component._components_by_id[self.id] = self

    def render(self):
        """
        In base classes, return the HTML element used to display the
        component.
        """
        raise NotImplementedError()  # pragma: no cover

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        """
        Ensure the layout from the new parent is handled properly for this
        component.
        """
        self._parent = parent
        self._parent_type = type(parent).__name__
        self.on_horizontal_align_changed()
        self.on_vertical_align_changed()

    def update(self, **kwargs):
        """
        Update the properties of the component with the specified keyword
        arguments.
        """
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                raise AttributeError(self, k)

    def get_from_datastore(self, property_name):
        """
        Return the "from_datastore" instance for a property, or None if it is
        an unbound property.
        """
        return self.properties()[property_name].get_from_datastore(self)

    def set_from_datastore(self, property_name, *args, **kwargs):
        """
        Set the "from_datastore" instance for a property. Pass None to make it
        an unbound property.
        """
        self.properties()[property_name].set_from_datastore(
            self, *args, **kwargs
        )

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
        self.element.style["visibility"] = (
            "visible" if self.visible else "hidden"
        )

    def on_column_span_changed(self):
        """
        Ensure the component spans the correct number of columns in a grid
        container.
        """
        if self.column_span is not None:
            self.element.style["grid-column"] = f"span {self.column_span}"

    def on_row_span_changed(self):
        """
        Ensure the component spans the correct number of rows in a grid
        container.
        """
        if self.row_span is not None:
            self.element.style["grid-row"] = f"span {self.row_span}"

    def on_background_color_changed(self):
        """
        Set the background color.
        """
        if self.background_color:
            self.element.style["background-color"] = self.background_color
        else:
            self.element.style.remove("background-color")

    def on_border_color_changed(self):
        """
        Set the border color.
        """
        if self.border_color:
            self.element.style["border-color"] = self.border_color
        else:
            self.element.style.remove("border-color")

    def on_border_width_changed(self):
        """
        Set the border width (translating from t-shirt sizes).
        """
        sizes = GAP_SIZES
        if self.border_width is not None:
            size = sizes[self.border_width.upper()]
            self.element.style["border-width"] = size
        else:
            self.element.style.remove("border-width")

    def on_border_style_changed(self):
        """
        Set the border style.
        """
        if self.border_style:
            self.element.style["border-style"] = self.border_style
        else:
            self.element.style.remove("border-style")

    def on_horizontal_align_changed(self):
        """
        Set the horizontal alignment of the widget.
        """
        if self._parent_type == "Row":
            self.element.style["justify-self"] = self.horizontal_align
        else:  # Column, Grid
            self.element.style["align-self"] = self.horizontal_align

    def on_vertical_align_changed(self):
        """
        Set the vertical alignment of the widget.
        """
        if self._parent_type == "Row":
            self.element.style["align-self"] = self.vertical_align
        else:  # Column, Grid
            self.element.style["justify-self"] = self.vertical_align

    @classmethod
    def properties(cls):
        """
        Return a dictionary of the component's properties.
        """
        return {
            name: value
            for name, value in getmembers_static(cls)
            if isinstance(value, Property)
        }

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

    @classmethod
    def icon(cls):
        """
        Return the SVG to display in the menu of available components in the
        UI builder.
        """
        return _DEFAULT_ICON
    
    @classmethod
    def category(cls):
        """
        Return the category name of the component. Defaults to "General", but
        is expected to be overridden by subclasses to something like:
        "Actions", "Media", "Data", "Navigation", "Inputs", "Layout", etc.

        Different categories will be displayed in different sections of the
        UI builder.
        """
        return "General"

    @classmethod
    def events(cls):
        """
        Returns a dictionary of the component's events that define the sort of
        messages a component may send during its lifetime.
        """
        return {
            name: value
            for name, value in getmembers_static(cls)
            if isinstance(value, Event)
        }

    @classmethod
    def definition(cls):
        """
        Return a dictionary defining all the essential information about the
        component: its name, properties, events and associated icon.
        """
        return {
            "name": cls.__name__,
            "properties": {
                name: prop.as_dict() for name, prop in cls.properties().items()
            },
            "events": {
                key: value.as_dict() for key, value in cls.events().items()
            },
            "icon": cls.icon(),
        }

    def as_dict(self):
        """
        Return a dict representation of the state of this instance.
        """
        properties = {}
        for property_name, property_obj in sorted(self.properties().items()):
            from_datastore = self.get_from_datastore(property_name)
            if from_datastore:
                property_value = repr(from_datastore)
            else:
                property_value = getattr(self, property_name)

            properties[property_name] = property_value

        # If the component is a Container, we format its content recursively.
        if hasattr(self, "children"):
            if not self.get_from_datastore("children"):
                properties["children"] = [
                    item.as_dict() for item in self.children
                ]

        return {
            "type": type(self).__name__,
            "properties": properties,
        }

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
