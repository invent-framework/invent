"""The Python-side of the Invent Builder."""


import json
from pyscript import document, window
from pyscript.ffi import create_proxy

import invent
from invent.ui import export
from invent.ui.core import Container, Component, Widget, from_datastore
from invent.ui import create_component, AVAILABLE_COMPONENTS


class Builder:
    """The Python-side of the Invent Builder."""

    def __init__(self):
        """The Python-side of the Invent builder.

        The model-view for the builder is split into two parts: JS and Python.
        """

        # The Invent app that the builder is building.
        self._app = invent.ui.App(
            name="Invent Demo",
            content=[
                invent.ui.Page(
                    name="Page 1",
                    content=[
                        BuilderDropZone(self),
                    ]
                )
            ]
        )

        # The JS-side of the Invent-Builder.
        self._builder_model = None

    def set_view_model(self, builder_model):
        """
        Connects the Python side of the view model to the JS side.
        """
        self._builder_model = builder_model

    # App ##############################################################################

    @property
    def app(self):
        """
        The app that we are building.
        """
        return self._app

    def get_app_as_dict(self):
        """
        Return the JSON-ified app.
        """
        return json.dumps(self._app.as_dict())

    def get_app_from_dict(self, app_dict):
        """
        Create an App instance from the specified dictionary representation.

        This sets created app to be the one that the builder is building.
        """
        self._app = export.from_dict({"app": json.loads(app_dict)})

    # Pages ############################################################################

    def add_page(self, page_name):
        """
        Add an empty page with the specified name.
        """
        new_page = invent.ui.Page(name=page_name)

        self._app.content.append(new_page)

        return json.dumps(new_page.as_dict())

    def delete_page(self, page_name):
        """
        Delete the page with the specified name.
        """
        page = self._app.get_page_by_name(page_name)
        if page is None:
            raise(ValueError(f"No such page: {page_name}"))

        ...

    def get_pages(self):
        """
        Return a list of all the pages in the app.
        """
        return json.dumps(self._app.as_dict()["content"])

    def update_page(self, page_name, **properties_to_update):
        """
        Update the properties of the page with the specified name.
        """
        ...

    # Widgets ##########################################################################

    def get_available_components(self):
        """
        Return a dictionary of available component blueprints by name.
        """
        blueprints = {"containers": {}, "widgets": {}}
        for component_klass_name, component_klass in AVAILABLE_COMPONENTS.items():
            if issubclass(component_klass, Container):
                collection = "containers"

            else:
                collection = "widgets"

            blueprints[collection][component_klass_name] = component_klass.blueprint()

        return json.dumps(blueprints)

    def append_component(self, parent_id, component_type_name):
        """
        Append a component to the specified parent.
        """
        parent = self._app.get_component_by_id(parent_id)
        if parent is None:
            raise ValueError(f"No such container: {parent_id}")

        self.insert_component_after(parent.content[-1], component_type_name)

    def insert_component_after(self, after_component, component_type_name):
        """
        Insert a component after another (as a sibling).
        """

        parent = after_component.parent
        after_component_index = parent.content.index(after_component)

        component = create_component(component_type_name)

        if after_component_index == len(parent.content) - 1:
            parent.append(component)
            parent.append(BuilderDropZone(self))

        else:
            parent.insert(after_component_index + 1, component)
            parent.insert(after_component_index + 2, BuilderDropZone(self))

        if isinstance(component, Container):
            component.append(BuilderDropZone(self))

        def on_click_on_component(event):
            """
            Called when a JS "click" event is fired on a component in a page.
            """

            event.stopPropagation()

            self._builder_model.onComponentClicked(
                create_proxy(type(component).blueprint()), create_proxy(component)
            )

        component.element.addEventListener("click", create_proxy(on_click_on_component))

    def delete_component(self, component_id):
        """
        Delete the component with the specified id.
        """
        component_to_delete = self._app.get_component_by_id(component_id)
        component_to_delete.parent.remove(component_to_delete)

    def get_component_element_by_id(self, component_id):
        """
        Return the component with the specified id or None if no such component exists.
        """

        component = self._app.get_component_by_id(component_id)
        if component is None:
            return None

        return component.element

    def get_component_properties(self, component_id):
        """
        Return a dictionary of properties for the specified component.
        """
        component = self._app.get_component_by_id(component_id)
        if component is None:
            raise ValueError(f"No such component: {component_id}")

        properties = type(component).blueprint()["properties"]
        for name, value in properties.items():
            if hasattr(component, f"_{name}_from_datastore"):
                value["is_from_datastore"] = True
                datastore_value = getattr(component, f"_{name}_from_datastore")
                value["value"] = datastore_value.key
            else:
                value["value"] = getattr(component, name)
            
        if isinstance(component, Container):
            properties.pop("content")

        return json.dumps(properties)
    
    def update_component_property(self, component_id, property_name, value, is_from_datastore=False):
        """
        Update a property on a component (that has already been added to the page).
        """
        component = self._app.get_component_by_id(component_id)
        if is_from_datastore:
            setattr(component, property_name, from_datastore(value))
        else:
            setattr(component, property_name, value)

    def get_page_element_by_id(self, page_id):
        result = self._app.get_page_by_id(page_id)
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


class BuilderDropZone(Widget):
    """
    A drop zone used ONLY in the builder to position components on a page.
    """

    def __init__(self, builder, **kwargs):
        super().__init__(**kwargs)
        self.builder = builder

    def on_dragover(self, event):
        event.preventDefault()
        event.stopPropagation()
        self.element.classList.add("drop-zone-active")

    def on_dragleave(self, event):
        event.preventDefault()
        event.stopPropagation()
        self.element.classList.remove("drop-zone-active")

    def on_drop(self, event):
        event.preventDefault()
        event.stopPropagation()
        self.element.classList.remove("drop-zone-active")
        component_blueprint = json.loads(event.dataTransfer.getData("widget"))

        self.builder.insert_component_after(
            after_component=self, component_type_name=component_blueprint["name"]
        )

    def render(self):
        """
        Create the component's HTML element.
        """
        element = document.createElement("div")
        element.id = self.id
        element.classList.add("drop-zone")
        element.addEventListener("dragover", create_proxy(self.on_dragover))
        element.addEventListener("dragleave", create_proxy(self.on_dragleave))
        element.addEventListener("drop", create_proxy(self.on_drop))
        return element
