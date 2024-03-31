"""The Python-side of the Invent Builder."""


import json
from pyscript import document, window
from pyscript.ffi import create_proxy

import invent
from invent.ui import AVAILABLE_COMPONENTS, create_component, export
from invent.ui.core import Column, Container, Component, Row, Widget, from_datastore
from invent.ui.page import Page


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
                invent.ui.Page(name="Page 1")
            ]
        )

        # Inject JS event handlers into all components in the app.
        self._inject_js_event_handlers_into_app(self._app)

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
        app = export.from_dict({"app": json.loads(app_dict)})
        self._inject_js_event_handlers_into_app(app)
        self._app = app

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

        self._inject_js_event_handlers_into_component(component)
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

        self._inject_js_event_handlers_into_component(component)
        self.pprint_app()

    def insert_component_before(self, before_component, component):
        """
        Create and insert a component before another (as a sibling).
        """

        parent = before_component.parent

        before_component_index = parent.content.index(before_component)
        parent.insert(before_component_index, component)

        self._inject_js_event_handlers_into_component(component)
        self.pprint_app()

    def delete_component(self, component_id):
        """
        Delete the component with the specified id.
        """
        component_to_delete = self._app.get_component_by_id(component_id)
        component_to_delete.parent.remove(component_to_delete)

        component_to_delete._remove_js_event_handlers()

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

        print(f"{indent}{type(container).__name__}({container.name, container.id}) -> {parent_id}")
        indent += "    "

        for item in container.content:
            if isinstance(item, Container):
                self.pprint_container(item, indent)

            else:
                parent_id = None if not item.parent else item.parent.id
                print(f"{indent}{type(item).__name__}({item.name, item.id}) -> {parent_id}")

    # Internal #########################################################################

    def _inject_js_event_handlers_into_app(self, app):
        """
        Inject JS event handlers into the specified app.

        We inject handlers to:-

        a) catch click events so that we can show a component's property sheet.
        b) handle drag and drop events.
        """

        for page in app.content:
            self._inject_js_event_handlers_into_container(page)

    def _inject_js_event_handlers_into_container(self, container):
        """
        Recursively Inject JS event handlers into the specified container.
        """

        self._inject_js_event_handlers_into_component(container)

        for item in container.content[:]:
            if isinstance(item, Container):
                self._inject_js_event_handlers_into_container(item)

            else:
                self._inject_js_event_handlers_into_component(item)

    def _inject_js_event_handlers_into_component(self, component):
        """
        Recursively Inject JS event handlers into the specified component.
        """

        def remove_js_event_handlers():
            print("removing js", component.name, component.id)
            component.element.setAttribute("draggable", "false")
            component.element.removeEventListener("dragstart", component._on_dragstart_proxy)
            component.element.addEventListener("dragover", component._on_dragover_proxy)
            component.element.addEventListener("dragleave", component._on_dragleave_proxy)
            component.element.addEventListener("drop", component._on_drop_proxy)

            if isinstance(component, Container):
                for child in component.content:
                    child._remove_js_event_handlers()

        component._remove_js_event_handlers = remove_js_event_handlers

        def on_click_on_component(event):
            """
            Called when a JS "click" event is fired on a component in a page.
            """

            event.stopPropagation()

            self._builder_model.onComponentClicked(
                create_proxy(type(component).blueprint()), create_proxy(component)
            )

        component.element.addEventListener("click", create_proxy(on_click_on_component))

        def on_dragstart(event):
            if isinstance(component, Page):
                event.preventDefault()
                event.stopPropagation()

            else:
                event.stopPropagation()
                print("on_dragstart:", component.name)
                event.dataTransfer.setData("move", component.id);

        def on_drop(event):
            print("on_drop:", component.name)
            event.preventDefault()
            event.stopPropagation()

            # Moving or adding? ########################################################

            move_data = event.dataTransfer.getData("move")
            print("MOVE COMPONENT", move_data)
            if move_data == component.id:
                return

            if move_data:
                component_to_move = Component.get_component_by_id(move_data)

                print("Ok, so I think I need to delete the moving", component_to_move.name, component_to_move.id, component_to_move.parent)
                self.delete_component(component_to_move.id)
                new_component = component_to_move.clone()

            else:
                component_blueprint = json.loads(event.dataTransfer.getData("widget"))
                component_type_name = component_blueprint["name"]
                new_component = create_component(component_type_name)

            # Dropping on a Widget or a Container? #####################################
            if isinstance(component, Container):
                container = component
                component.element.classList.remove("drop-zone-active")

            else:
                container = component.parent
                component.element.parentNode.classList.remove(f"drop-zone-active-{self.mode}")

            if isinstance(component, Container) and len(component.content) == 0:
                self.append_component(container.id, new_component)

            else:
                if self.mode in ["left", "above"]:
                    if isinstance(component, Container):
                        insert_before = component.content[0]

                    else:
                        insert_before = component

                    print("Inserting before:", self.mode, insert_before)
                    self.insert_component_before(insert_before, new_component)
                else:
                    if isinstance(component, Container):
                        insert_after = component.content[-1]

                    else:
                        insert_after = component
                    print("Inserting after:", self.mode, insert_after)
                    self.insert_component_after(insert_after, new_component)


        def on_dragover(event):
            """
            Handle a JS "dragover" event on a component.
            """
            #print("on_dragover:", component.name)
            event.preventDefault()
            event.stopPropagation()

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
                    self.mode = "above"

                elif pointer_offset_y > (component_height * .5):
                    self.mode = "below"

            elif isinstance(container, Row):
                if pointer_offset_x < (component_width * .5):
                    self.mode = "left"

                elif pointer_offset_x > (component_width * .5):
                    self.mode = "right"

            else:
                return
                #raise ValueError("Shouldn't get here!!!", container)

            if isinstance(component, Container):
                component.element.classList.add(f"drop-zone-active")

            else:
                for class_name in component.element.parentNode.classList:
                    if class_name.startswith("drop-zone-active"):
                        component.element.parentNode.classList.remove(class_name)

                component.element.parentNode.classList.add(f"drop-zone-active-{self.mode}")

        def on_dragleave(event):
            #print("on_dragleave:", component.name)
            event.preventDefault()

            if isinstance(component, Container):
                component.element.classList.remove("drop-zone-active")

            component.element.parentNode.classList.remove(f"drop-zone-active-{self.mode}")

        component.element.setAttribute("draggable", "true")

        component._on_dragstart_proxy = create_proxy(on_dragstart)
        component._on_dragover_proxy = create_proxy(on_dragover)
        component._on_dragleave_proxy = create_proxy(on_dragleave)
        component._on_drop_proxy = create_proxy(on_drop)

        component.element.addEventListener("dragstart", component._on_dragstart_proxy)
        component.element.addEventListener("dragover", component._on_dragover_proxy)
        component.element.addEventListener("dragleave", component._on_dragleave_proxy)
        component.element.addEventListener("drop", component._on_drop_proxy)

        if isinstance(component, Container):
            for item in component.content:
                self._inject_js_event_handlers_into_component(item)