"""The Python-side of the Invent Builder."""


import json
from pyscript.ffi import create_proxy

import invent
from invent.ui import (
    App, AVAILABLE_COMPONENTS, Column, Container, create_component, export, Page,
    Row, Widget, from_datastore
)
from invent.ui.core import Component


class Builder:
    """The Python-side of the Invent Builder."""

    def __init__(self):
        """The Python-side of the Invent builder.

        The model-view for the builder is split into two parts: JS and Python.
        """

        # The Invent app that the builder is building.
        self._app = None

        # The JS-side of the Invent-Builder.
        self._js_builder_model = None

        # The component currently being dragged or None if there is no such component.
        self._component_being_dragged = None

        # The current component insertion mode/direction.
        #
        # It will be one of "left", "right", "above", "below".
        self._insertion_mode = None

        # TODO: We might eventually open with an existing app, but here we just create
        # one with a single, empty page.
        self.app = App(name="Invent Demo", content=[Page(name="Page 1")])

    def set_js_builder_model(self, js_builder_model):
        """
        Connects the Python side of the view model to the JS side.
        """
        self._js_builder_model = js_builder_model

    # App ##############################################################################

    @property
    def app(self):
        """
        Get the app that we are building.
        """
        return self._app

    @app.setter
    def app(self, app):
        """
        Set the app that we are building.
        """
        if self._app is not None:
            # If there was a previous app, remove all the JS event handlers from it.
            self._remove_js_event_handlers_from_app(self._app)

        # Inject the JS event handlers to make component selection and drag-and-drop
        # work.
        self._add_js_event_handlers_to_app(app)

        # The builder is now officially managing the rehydrated app!
        self._app = app
        self.pprint_app()

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
        self.app = export.from_dict({"app": json.loads(app_dict)})

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

    def append_component(self, parent_id, component):
        """
        Create and append a component to the specified parent.
        """
        parent = self._app.get_component_by_id(parent_id)
        if parent is None:
            raise ValueError(f"No such container: {parent_id}")

        parent.append(component)

        self._add_js_event_handlers_to_component(component)
        self.pprint_app()

    def delete_component(self, component_id):
        """
        Delete the component with the specified id.
        """
        component_to_delete = self._app.get_component_by_id(component_id)
        component_to_delete.parent.remove(component_to_delete)

        self._remove_js_event_handlers_from_component(component_to_delete)
        self.pprint_app()

    def insert_component_after(self, after_component, component):
        """
        Create and insert a component after another (as a sibling).
        """

        parent = after_component.parent

        after_component_index = parent.content.index(after_component)
        if after_component_index == len(parent.content) - 1:
            parent.append(component)

        else:
            parent.insert(after_component_index + 1, component)

        self._add_js_event_handlers_to_component(component)
        self.pprint_app()

    def insert_component_before(self, before_component, component):
        """
        Create and insert a component before another (as a sibling).
        """

        parent = before_component.parent

        before_component_index = parent.content.index(before_component)
        parent.insert(before_component_index, component)

        self._add_js_event_handlers_to_component(component)
        self.pprint_app()

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
    
    def set_component_property(self, component_id, property_name, value, is_from_datastore=False):
        """
        Set a property on a component (that has already been added to the page).
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

    def pprint_app(self):
        """
        Pretty print the basic structure of the app.
        """
        print(f"App({self._app.name})")

        indent = "    "
        for page in self._app.content:
            self.pprint_container(page, indent)

    def pprint_container(self, container, indent):
        """
        Pretty print a container.
        """

        parent_id = None if not container.parent else container.parent.id
        parent_pid = None if not container.parent else id(container.parent)

        # Uncomment for more detail :)
        # print(f"{indent}{type(container).__name__}({container.name}, {container.id}, {id(container)}) -> {parent_id}:{parent_pid}")
        print(f"{indent}{type(container).__name__}({container.name}, {container.id})")
        indent += "    "

        for item in container.content:
            if isinstance(item, Container):
                self.pprint_container(item, indent)

            else:
                parent_id = None if not item.parent else item.parent.id
                parent_pid = None if not item.parent else id(item.parent)
                # Uncomment for more detail :)
                # print(f"{indent}{type(item).__name__}({item.name}, {item.id}, {id(item)}) -> {parent_id}:{parent_pid}")
                print(f"{indent}{type(item).__name__}({item.name}, {item.id})")

    # Internal #########################################################################

    def _add_js_event_handlers_to_app(self, app):
        """
        Add JS event handlers to all components in the specified app.

        We add handlers to:-

        a) catch click events so that we can show a component's property sheet.
        b) handle drag and drop events for adding/moving components on a page.
        """
        for page in app.content:
            self._add_js_event_handlers_to_component(page)

    def _add_js_event_handlers_to_component(self, component):
        """
        Recursively add JS event handlers to the specified component.
        """

        def on_click(event):
            self._on_click_component(event, component)

        def on_dragstart(event):
            self._on_dragstart_component(event, component)

        def on_drop(event):
            self._on_drop_component(event, component)

        def on_dragover(event):
            self._on_dragover_component(event, component)

        def on_dragleave(event):
            self._on_dragleave_component(event, component)

        # Proxies if required by the underlying interpreter.
        #
        # It's a bit smelly, but we tag them onto the component so that we can remove
        # them if/when the component is deleted.
        component._on_click_proxy = create_proxy(on_click)
        component._on_dragstart_proxy = create_proxy(on_dragstart)
        component._on_dragover_proxy = create_proxy(on_dragover)
        component._on_dragleave_proxy = create_proxy(on_dragleave)
        component._on_drop_proxy = create_proxy(on_drop)

        # Pages...
        if component.parent is None:
            element = component.element

        # Everything else...
        else:
            # Attach to the *wrapper* we put around each grid item.
            element = component.element.parentNode
            element.setAttribute("draggable", "true")

        element.addEventListener("click", component._on_click_proxy)
        element.addEventListener("dragstart", component._on_dragstart_proxy)
        element.addEventListener("dragover", component._on_dragover_proxy)
        element.addEventListener("dragleave", component._on_dragleave_proxy)
        element.addEventListener("drop", component._on_drop_proxy)

        # Recursively...
        if isinstance(component, Container):
            for item in component.content:
                self._add_js_event_handlers_to_component(item)

    # JS event handlers ################################################################

    def _on_click_component(self, event, component):
        """
        Handle a JS "click" event on a component.
        """

        event.stopPropagation()

        self._js_builder_model.openPropertiesForComponent(
            create_proxy(type(component).blueprint()), component.id
        )

    def _on_dragleave_component(self, event, component):
        """
        Handle a JS "dragleave" event on a component.
        """

        event.preventDefault()

        if isinstance(component, Container):
            component.element.classList.remove("drop-zone-active")

        # Mode might be None as we don't set if when dragging over self.
        if self._insertion_mode:
            component.element.parentNode.classList.remove(f"drop-zone-active-{self._insertion_mode}")

    def _on_dragover_component(self, event, component):
        """
        Handle a JS "dragover" event on a component.
        """

        event.preventDefault()
        event.stopPropagation()

        # You can't drop a container onto one of its children!
        if isinstance(self._component_being_dragged, Container):
            for item in self._component_being_dragged.content:
                if item.id == component.id:
                    return

        # In JS, the data transfer data is NOT available on a "dragover" event. It is
        # only available when the element is dropped.
        if self._component_being_dragged == component:
            if isinstance(component, Container):
                component.element.classList.remove(f"drop-zone-active")

                # You can't drop a container onto one of its children!
                if isinstance(self._component_being_dragged, Container):
                    for item in self._component_being_dragged.content:
                        if item.id == component.id:
                            return


            else:
                for class_name in component.element.parentNode.classList:
                    if class_name.startswith("drop-zone-active"):
                        component.element.parentNode.classList.remove(class_name)

            return

        pointer_offset_x = event.offsetX
        pointer_offset_y = event.offsetY
        component_width = component.element.offsetWidth
        component_height = component.element.offsetHeight

        if isinstance(component, Container):
            container = component

        else:
            container = component.parent

        if isinstance(container, Column):
            if pointer_offset_y < (component_height * .5):
                self._insertion_mode = "above"

            elif pointer_offset_y > (component_height * .5):
                self._insertion_mode = "below"

        elif isinstance(container, Row):
            if pointer_offset_x < (component_width * .5):
                self._insertion_mode = "left"

            elif pointer_offset_x > (component_width * .5):
                self._insertion_mode = "right"

        else:
            raise ValueError("Unsupported container type:", container)

        if isinstance(component, Container):
            component.element.classList.add(f"drop-zone-active")

        else:
            for class_name in component.element.parentNode.classList:
                if class_name.startswith("drop-zone-active"):
                    component.element.parentNode.classList.remove(class_name)

            component.element.parentNode.classList.add(f"drop-zone-active-{self._insertion_mode}")

    def _on_dragstart_component(self, event, component):
        """
        Handle a JS "dragstart" event on a component.
        """
        event.stopPropagation()

        if isinstance(component, Page):
            event.preventDefault()

        else:
            # In JS, the data transfer data is NOT available on a "dragover" event.
            # Hence, we track the component being moved manually.
            self._component_being_dragged = component
            event.dataTransfer.setData("move", component.id)

    def _on_drop_component(self, event, component):
        """
        Handle a JS "drop" event on a component.
        """
        event.preventDefault()
        event.stopPropagation()

        # Moving or adding? ########################################################

        move_data = event.dataTransfer.getData("move")
        widget_data = event.dataTransfer.getData("widget")

        if move_data:
            print("moving:", move_data, "onto:", component.name)

            component_to_move = Component.get_component_by_id(move_data)

            # You can't drop a container onto one of its children!
            if isinstance(component_to_move, Container):
                for item in component_to_move.content:
                    if item.id == component.id:
                        return

        if widget_data:
            print("adding:", widget_data)

        # You can't drop a component onto itself :)
        if move_data == component.id:
            return

        if widget_data:
            component_blueprint = json.loads(widget_data)
            new_component = create_component(component_blueprint["name"])

        else:
            self.delete_component(component_to_move.id)
            new_component = component_to_move.clone()

        # Dropping on a Widget or a Container? #########################################

        if isinstance(component, Container):
            container = component
            component.element.classList.remove("drop-zone-active")

        else:
            container = component.parent
            component.element.parentNode.classList.remove(f"drop-zone-active-{self._insertion_mode}")

        if isinstance(component, Container) and len(component.content) == 0:
            self.append_component(container.id, new_component)

        else:
            if self._insertion_mode in ["left", "above"]:
                insert_before = component.content[0] if isinstance(component, Container) else component
                self.insert_component_before(insert_before, new_component)
            else:
                insert_after = component.content[-1] if isinstance(component, Container) else component
                self.insert_component_after(insert_after, new_component)

    def _remove_js_event_handlers_from_app(self, app):
        """
        Remove JS event handlers from all components in the specified app.
        """
        for page in app.content:
            self._remove_js_event_handlers_from_component(page)

    def _remove_js_event_handlers_from_component(self, component):
        """
        Recursively remove JS event handlers from the specified component.
        """
        # Pages...
        if component.parent is None:
            element = component.element

        # Everything else...
        else:
            # Remove from the *wrapper* we put around every grid item.
            element = component.element.parentNode
            element.setAttribute("draggable", "false")

        element.removeEventListener("click", component._on_click_proxy)
        element.removeEventListener("dragstart", component._on_dragstart_proxy)
        element.addEventListener("dragover", component._on_dragover_proxy)
        element.addEventListener("dragleave", component._on_dragleave_proxy)
        element.addEventListener("drop", component._on_drop_proxy)

        # Recursively...
        if isinstance(component, Container):
            for item in component.content:
                self._remove_js_event_handlers_from_component(item)
