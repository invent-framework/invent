"""The Python-side of the Invent Builder."""


import json
from pyscript import document, window

import invent
from invent.ui import export
from invent.ui.core import Container, Component, Widget, from_datastore
from invent.ui import AVAILABLE_COMPONENTS


class Builder:
    """The Python-side of the Invent Builder."""

    def __init__(self):
        # The app that we are building.
        self._app = invent.ui.App(
            name="Invent Demo",
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

    def get_available_components(self):
        """
        Return a dictionary of available component blueprints by name.

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
            "containers": {},
            "widgets": {}
        }

        for component_klass_name, component_klass in AVAILABLE_COMPONENTS.items():
            if issubclass(component_klass, Container):
                collection = "containers"

            else:
                collection = "widgets"

            blueprints[collection][component_klass_name] = component_klass.blueprint()

        return json.dumps(blueprints)

    def add_widget_to_page(self, page, widget_blueprint, parent_id=None):
        """
        Create a widget from a blueprint and add it to the specified page.
        """

        page = self._get_page_by_id(page.id)
        if page is None:
            raise ValueError(f"No such page: {page.name}")

        component_klass = AVAILABLE_COMPONENTS.get(widget_blueprint.name)
        if component_klass is None:
            raise ValueError(f"No such widget: {widget_blueprint.name}")

        component = component_klass()

        if parent_id is None:
            page.append(component)

        else:
            parent = self._get_widget_by_id(parent_id)
            parent.append(component)

        if widget_blueprint.name == "Column" or widget_blueprint.name == "Row":
            component.element.classList.add("drop-zone")
        else:
            component.element.style.pointerEvents = "none"
            component.element.parentElement.style.cursor = "crosshair"

        return component.element

    def delete_widget(self, widget_id):
        widget_to_delete = self._get_widget_by_id(widget_id)
        widget_to_delete.parent.remove(widget_to_delete)

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
            if hasattr(widget, f"_{name}_from_datastore"):
                value["is_from_datastore"] = True
                datastore_value = getattr(widget, f"_{name}_from_datastore")
                value["value"] = datastore_value.key
            else:
                value["value"] = getattr(widget, name)
            
        if issubclass(component_klass, Container):
            properties.pop("content")

        return json.dumps(properties)
    
    def update_widget_property(self, widget_blueprint, widget_id, property_name, value, is_from_datastore=False):
        """
        Update a property on a widget (that has already been added to the page).
        """

        # window.console.log(f"update_widget_property: {widget_blueprint}, {widget_id}, {property_name} {value}")

        component = self._get_widget_by_id(widget_id)
        if is_from_datastore:
            setattr(component, property_name, from_datastore(value))
        else:
            setattr(component, property_name, value)

    def get_page_element_by_id(self, page_id):
        result = self._get_page_by_id(page_id)
        if result:
            return result.element
        
    # Channels ####################################################################
        
    def get_channels(self):
        channels = set()
        for component in Component._components_by_id.values():
            if isinstance(component, Widget) and component.channel:
                channels.add(component.channel)
        channels.add("store-data")
        channels.add("delete-data")
        return json.dumps(list(channels))
    
    def get_subjects(self):
        subjects = set()
        for component in Component._components_by_id.values():
            if isinstance(component, Widget):
                widget_cls = type(component)
                message_blueprints = widget_cls.message_blueprints()
                subjects.update(message_blueprints.keys())
        return json.dumps(list(subjects))


    # Import/export ####################################################################

    def export_as_pyscript_app(self, datastore, code) -> str:
        """
        Export the Invent App as a PyScript app.

        Returns a dictionary containing the contents of index.html, main.py, and
        pyscript.toml files in the form:

        {
            "index.html" : str,
            "main.py": str,
            "pyscript.toml": str
        }

        """

        index_html, main_py, pyscript_toml = export.as_pyscript_app(
            self._app, datastore=datastore, code=code
        )

        return json.dumps({
            "index.html": index_html,
            "main.py": main_py,
            "pyscript.toml": pyscript_toml

        })

    # Internal #########################################################################

    def _get_page_by_id(self, page_id):
        """
        Return the page with the specified id or None if no such page exists.
        """

        for page in self._app.content:
            if page.id == page_id:
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
