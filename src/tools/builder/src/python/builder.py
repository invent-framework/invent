"""The Python-side of the Invent Builder."""


import invent
from invent.ui.core import Component
from invent.ui import AVAILABLE_COMPONENTS
import json
from pyscript import document, window


class Builder:
    """The Python-side of the Invent Builder."""

    def __init__(self):
        # The app that we are building.
        self._app = invent.ui.App(
            name="Untitled Cool App",
            content=[
                invent.ui.Page(
                    name="Page 1",
                    content=[]
                )
            ]
        )

    # App ##############################################################################

    @property
    def app(self):
        """
        The app that we are building.
        """
        return self._app

    def get_app(self):
        """Might need this to return the app as a plain ol' dictionary."""

        return self._app.as_dict()

    # Pages ############################################################################

    def add_page(self, page_name):
        """
        Add an empty page with the specified name to the app.
        """
        new_page = invent.ui.Page(name=page_name)

        self._app.content.append(new_page)

        return json.dumps(new_page.as_dict())

    def delete_page(self, page_name):
        """
        Delete the page with the specified name.
        """
        ...

    def get_pages(self):
        """
        Return a list of all the pages in the app.
        """
        return json.dumps(self.get_app()["content"])

    def update_page(self, page_name, **properties_to_update):
        """
        Update the properties of the page with the specified name.
        """
        ...

    # Widgets ##########################################################################

    def get_available_widgets(self):
        """
        Return a dictionary of available widget blueprints by name.

        e.g.

        {
            "Button": {
                "properties": {
                    "id": {
                      "property_type": "TextProperty",
                      "description": "The id of the widget instance in the DOM.",
                      "required": False,
                      "default_value": None,
                      "min_length": None,
                      "max_length": None
                    },
                    ...
                },
                "message_blueprints": [
                    "click", "double-click", "hold"
                ],
                "preview" : "<button>Button</button>"
            },
            ...
        }

        """
        blueprints = {
            widget_klass_name: widget_klass.blueprint()

            for widget_klass_name, widget_klass in AVAILABLE_COMPONENTS.items()
        }

        return json.dumps(blueprints)

    def add_widget_to_page(self, page_name, widget_blueprint, parent_id=None):
        """
        Create a widget from a blueprint and add it to the specified page.
        """

        window.console.log(f"page_name: {page_name}")
        window.console.log(f"widget_blueprint: {widget_blueprint}")

        page = self._get_page_by_name(page_name)
        if page is None:
            raise ValueError(f"No such page: {page_name}")

        widget_klass = AVAILABLE_COMPONENTS.get(widget_blueprint.name)
        if widget_klass is None:
            raise ValueError(f"No such widget: {widget_blueprint.name}")

        widget = widget_klass()

        page.append(widget)

        target = document.getElementById(parent_id)
        target.appendChild(widget.element)

        return widget.id

    def delete_widget_from_page(self, widget_id):
        ...

    def get_widget_properties(self, widget_blueprint, widget_id):
        """
        Return a dictionary of properties from a widget reference.
        """
        component_klass = AVAILABLE_COMPONENTS.get(widget_blueprint.name)
        if component_klass is None:
            raise ValueError(f"No such component: {widget_blueprint.name}")

        widget = self._get_widget_by_id(widget_id)
        if widget is None:
            raise ValueError(f"No such widget: {widget_id}")

        properties = component_klass.blueprint()["properties"]
        for name, value in properties.items():
            value["value"] = getattr(widget, name)

        window.x = json.dumps(properties)
        return json.dumps(properties)
    
    def update_widget_property(self, widget_id, value):
        """
        Update a property on a widget (that has already been added to the page).
        """

        window.console.log(f"update_widget_property: {widget_id}, {value}")

    # Internal #########################################################################

    def _get_page_by_name(self, page_name):
        """
        Return the page with the specified name or None if no such page exists.
        """

        for page in self._app.content:
            if page.name == page_name:
                break

        else:
            page = None

        return page

    def _get_widget_by_id(self, widget_id):
        """
        Return the widget with the specified id or None if no such widget exists.
        """

        from invent.ui.core import Component

        return Component.get_component_by_id(widget_id)
