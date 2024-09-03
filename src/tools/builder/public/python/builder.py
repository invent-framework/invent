"""The Python-side of the Invent Builder."""


from collections import OrderedDict
import json
from pyscript import document
from pyscript.ffi import create_proxy

from invent import datastore
from invent.ui import (
    App, AVAILABLE_COMPONENTS, Column, Container, create_component, export, Grid, Page,
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
        self.app = App(name="Invent Demo", content=[])

        # The JS-side of the Invent-Builder.
        self._js_builder_model = None

        # The component currently being dragged or None if there is no such component.
        self._component_being_dragged = None

        # The current component insertion position.
        #
        # It will be one of "left", "right", "top", "bottom".
        self._insertion_position = None

    def set_js_builder_model(self, js_builder_model):
        """
        Connects the Python side of the view model to the JS side.
        """
        self._js_builder_model = js_builder_model
        self._js_builder_model.load()

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

        # Add elements to the DOM to visualize empty containers.
        self._manage_empty_elements_in_app(app)

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
        new_page = Page(name=page_name)

        self._app.content.append(new_page)

        # Inject the JS event handlers to make component selection and drag-and-drop
        # work.
        self._add_js_event_handlers_to_component(new_page)

        # Add elements to the DOM to visualize empty containers.
        self._manage_empty_element_in_container(new_page)

        self.pprint_app()

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

            blueprints[collection][component_klass_name] = component_klass.definition()

        return json.dumps(blueprints)

    def append_component(self, container, component):
        """
        Append a component to the specified container.
        """
        container.append(component)
        self._manage_empty_element_in_container(container)

        self._add_js_event_handlers_to_component(component)
        self.pprint_app()

    def create_and_append_component(self, parent_id, component_type_name):
        """
        Create and append a component to the specified parent.
        """
        parent = self._app.get_component_by_id(parent_id)
        if parent is None:
            raise ValueError(f"No such container: {parent_id}")

        self.append_component(parent, create_component(component_type_name))

    def delete_component(self, component_id):
        """
        Delete the component with the specified id.
        """
        component_to_delete = self._app.get_component_by_id(component_id)
        component_to_delete.parent.remove(component_to_delete)
        self._manage_empty_element_in_container(component_to_delete.parent)

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

        self._manage_empty_element_in_container(parent)

        self._add_js_event_handlers_to_component(component)
        self.pprint_app()

    def insert_component_before(self, before_component, component):
        """
        Create and insert a component before another (as a sibling).
        """

        parent = before_component.parent

        before_component_index = parent.content.index(before_component)
        parent.insert(before_component_index, component)
        self._manage_empty_element_in_container(parent)

        self._add_js_event_handlers_to_component(component)
        self.pprint_app()

    def get_component_properties(self, component_id):
        """
        Return a dictionary of properties for the specified component.
        """
        component = self._app.get_component_by_id(component_id)
        if component is None:
            raise ValueError(f"No such component: {component_id}")

        # Plain dicts aren't ordered yet in Micropython
        # (https://github.com/micropython/micropython/issues/6170).
        properties = OrderedDict()
        for name, value in sorted(component.properties().items()):
            properties[name] = value.as_dict()
            properties[name]["is_layout"] = False

        # The root component (Page) will have layout={}.
        layout = component.layout
        if layout:
            for name, value in sorted(layout.properties().items()):
                properties[name] = value.as_dict()
                properties[name]["is_layout"] = True

        for name, value in properties.items():
            if value["is_layout"]:
                target = component.layout
            else:
                target = component

            binding = target.get_from_datastore(name)
            if binding:
                value["is_from_datastore"] = True
                value["value"] = binding.key
            else:
                value["value"] = getattr(target, name)
            
        if component.is_container:
            properties.pop("content")

        return json.dumps(properties)
    
    def set_component_property(self, component_id, property_name, value, is_layout, is_from_datastore=False):
        """
        Set a property on a component (that has already been added to the page).
        """
        component = self._app.get_component_by_id(component_id)

        if is_layout:
            target = component.layout
        else:
            target = component

        if is_from_datastore:
            setattr(target, property_name, from_datastore(value))
        else:
            target.set_from_datastore(property_name, None)
            setattr(target, property_name, value)

    def show_page(self, page_id):
        result = self._app.get_page_by_id(page_id)
        if result:
            result.show()
            return result.element

    # Datastore ###################################################################

    def update_datastore(self, key, value):
        datastore[key] = value

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
                message_blueprints = widget_cls.events()
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
        print(f"{indent}{type(container).__name__}({container.name}, {container.id})")
        indent += "    "

        for item in container.content:
            if isinstance(item, Container):
                self.pprint_container(item, indent)

            else:
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

        def on_dragend(event):
            self._on_dragend_component(event, component)

        # Proxies if required by the underlying interpreter.
        #
        # It's a bit smelly, but we tag them onto the component so that we can remove
        # them if/when the component is deleted.
        component._on_click_proxy = create_proxy(on_click)
        component._on_dragstart_proxy = create_proxy(on_dragstart)
        component._on_dragover_proxy = create_proxy(on_dragover)
        component._on_dragleave_proxy = create_proxy(on_dragleave)
        component._on_dragend_proxy = create_proxy(on_dragend)

        component._on_drop_proxy = create_proxy(on_drop)

        element = component.element
        if component.parent is not None:
            element.setAttribute("draggable", "true")

        element.addEventListener("click", component._on_click_proxy)
        element.addEventListener("dragstart", component._on_dragstart_proxy)
        element.addEventListener("dragover", component._on_dragover_proxy)
        element.addEventListener("dragleave", component._on_dragleave_proxy)
        element.addEventListener("dragend", component._on_dragend_proxy)
        element.addEventListener("drop", component._on_drop_proxy)

        # Recursively...
        if component.is_container:
            for item in component.content:
                self._add_js_event_handlers_to_component(item)

    # JS event handlers ################################################################

    def _on_click_component(self, event, component):
        """
        Handle a JS "click" event on a component.
        """

        event.preventDefault()
        event.stopPropagation()
        self._open_properties(component)

    def _open_properties(self, component):
        self._js_builder_model.openPropertiesForComponent(
            json.dumps(type(component).blueprint()), component.id
        )

    def _on_dragend_component(self, event, component):
        """
        Handle a JS "dragend" event on a component.
        """

        event.preventDefault()
        event.stopPropagation()

        self._component_being_dragged = None

    def _on_dragleave_component(self, event, component):
        """
        Handle a JS "dragleave" event on a component.
        """

        event.preventDefault()

        self._remove_drop_zone_active_classes(component)

    def _on_dragover_component(self, event, component):
        """
        Handle a JS "dragover" event on a component.

        Note that in browser-ville, the data transfer data is NOT available on a
        "dragover" event.

        """

        event.stopPropagation()

        #self.find_nearest_component(event)

        # Rule 1: You can't drop a component onto itself.
        if self._component_being_dragged == component:
            return

        # Rule 2: You can't drop a container onto one of its own children!
        #
        # In JS, the data transfer data is NOT available on a "dragover" event. It is
        # only available when the element is dropped, hence we manually keep track of
        # the component being dragged.
        if isinstance(self._component_being_dragged, Container) and self._component_being_dragged.contains(component):
            return

        # In browser-ville, preventing the default on the dragover event means that
        # dropping here IS allowed and the browser will do whatever it does to indicate
        # that (e.g. on Chrome the user will see a "plus" icon).
        event.preventDefault()

        # 1) Remove any previous drop zone active classes from the component's element.
        self._remove_drop_zone_active_classes(component)

        # 2) Determine whether the current pointer position is above, below, to the
        # left or to the right of the component the pointer is over.
        self._insertion_position = self._get_insertion_position(event, component)

        # 3) Add an appropriate drop zone active class to the element to show where
        # the new element would be inserted
        self._add_drop_zone_active_classes(component)

    def _get_insertion_position(self, event, component):
        """
        Get the insertion position based on the location of the pointer on a component.
        """

        container = component if component.is_container else component.parent

        if isinstance(container, Column):
            insertion_position = "top" if event.offsetY <= (component.element.offsetHeight * .5) else "bottom"

        elif isinstance(container, Row) or isinstance(container, Grid):
            insertion_position = "left" if event.offsetX <= (component.element.offsetWidth * .5) else "right"

        else:
            raise ValueError("Unsupported container type:", container)

        return insertion_position

    def _on_dragstart_component(self, event, component):
        """
        Handle a JS "dragstart" event on a component.
        """
        event.stopPropagation()

        # You can't drag a Page anywhere :)
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

        self._component_being_dragged = None

        # Are we...
        #
        # a) Moving a component that is already on the page.
        move_data = event.dataTransfer.getData("move")
        if move_data:
            # Remove the component being moved from its old location.
            component_to_drop = Component.get_component_by_id(move_data)
            self._remove_js_event_handlers_from_component(component_to_drop)
            old_container = component_to_drop.parent
            component_to_drop.parent.remove(component_to_drop)

        # Or...
        #
        # b) Adding a new component to the page.
        else:
            old_container = None
            component_blueprint_json = event.dataTransfer.getData("widget")
            if component_blueprint_json:
                component_blueprint = json.loads(component_blueprint_json)
                component_to_drop = create_component(component_blueprint["name"])

            # Something that we have no interest in was dropped (i.e. maybe files etc).
            else:
                return

        # Remove any drop zone active classes ##########################################

        self._remove_drop_zone_active_classes(component)

        # Dropping onto a Widget or a Container? #######################################

        container = component if component.is_container else component.parent

        # When moving to a different container, clear the layout properties.
        if old_container is not container:
            component_to_drop.layout = {}

        # If the container is empty then a simple append will do...
        if len(container.content) == 0:
            self.append_component(container, component_to_drop)

        # Otherwise, insert the new component before or after as appropriate.
        else:
            if self._insertion_position in ["left", "top"]:
                insert_before = component.content[0] if component.is_container else component
                self.insert_component_before(insert_before, component_to_drop)
            else:
                insert_after = component.content[-1] if component.is_container else component
                self.insert_component_after(insert_after, component_to_drop)
        
        # Moving to a different container will clear the layout properties, so
        # refresh the properties panel.
        self._open_properties(component_to_drop)

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
        element = component.element
        if component.parent is not None:
            element.setAttribute("draggable", "false")

        element.removeEventListener("click", component._on_click_proxy)
        element.removeEventListener("dragstart", component._on_dragstart_proxy)
        element.removeEventListener("dragover", component._on_dragover_proxy)
        element.removeEventListener("dragleave", component._on_dragleave_proxy)
        element.removeEventListener("dragend", component._on_dragend_proxy)
        element.removeEventListener("drop", component._on_drop_proxy)

        # Recursively...
        if component.is_container:
            for item in component.content:
                self._remove_js_event_handlers_from_component(item)

    def _add_drop_zone_active_classes(self, component):
        """
        Add the appropriate drop zone active classes to a component.
        """
        element = component.element

        if component.is_container and len(component.content) == 0:
            element.classList.add("drop-zone-outside")

        else:
            drop_zone = document.createElement("div")
            element.parentElement.append(drop_zone)
            drop_zone.className = "drop-zone-inside"
            drop_zone.style.position = "absolute"

            if self._insertion_position in ["top", "bottom"]:
                self._position_drop_zone(
                    element, drop_zone, "top", "bottom", "height", "left", "width"
                )
            elif self._insertion_position in ["left", "right"]:
                self._position_drop_zone(
                    element, drop_zone, "left", "right", "width", "top", "height"
                )
            else:
                raise AssertionError(
                    f"unknown position {self._insertion_position!r}"
                )

    def _position_drop_zone(
        self,
        element,
        drop_zone,
        main_start_attr,
        main_end_attr,
        main_size_attr,
        cross_start_attr,
        cross_size_attr,
    ):
        # Converts e.g. "top" to "offsetTop"
        def offset(attr):
            return "offset" + attr[0].upper() + attr[1:]

        thickness = 4  # px

        main_start = getattr(element, offset(main_start_attr))
        main_size = getattr(element, offset(main_size_attr))
        if self._insertion_position == main_start_attr:
            setattr(drop_zone.style, main_start_attr, f"{main_start}px")
        elif self._insertion_position == main_end_attr:
            setattr(
                drop_zone.style,
                main_start_attr,
                f"{main_start + main_size - thickness}px",
            )
        else:
            raise AssertionError(
                f"unknown position {self._insertion_position!r}"
            )
        setattr(drop_zone.style, main_size_attr, f"{thickness}px")

        cross_start = getattr(element, offset(cross_start_attr))
        cross_size = getattr(element, offset(cross_size_attr))
        setattr(drop_zone.style, cross_start_attr, f"{cross_start}px")
        setattr(drop_zone.style, cross_size_attr, f"{cross_size}px")

    def _remove_drop_zone_active_classes(self, component):
        """
        Remove any drop zone active classes from a component.
        """
        element = component.element

        element.classList.remove("drop-zone-outside")
        drop_zone = element.parentElement.querySelector(".drop-zone-inside")
        if drop_zone:
            drop_zone.remove()

    def find_nearest_component(self, event):
        import math

        # Get the coordinates of the pointer.
        x = event.clientX
        y = event.clientY

        # Initialize variables to track the nearest element and its distance.
        nearest_component = None
        min_distance = float('inf')

        # Iterate through each draggable element.
        for component in Component._components_by_id.values():
            element = component.element

            # Get the position and dimensions of the element.
            rect = element.getBoundingClientRect()

            # Calculate the center coordinates of the element.
            center_x = rect.left + rect.width / 2
            center_y = rect.top + rect.height / 2

            # Calculate the distance between the pointer and the center of the element.
            distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

            # Update the nearest element if this element is closer.
            if distance < min_distance:
                min_distance = distance
                nearest_component = component

        print("Nearest component is:", nearest_component)
        return nearest_component

    def _manage_empty_elements_in_app(self, app):
        """
        Manage the elements shown when containers are empty.
        """
        for page in app.content:
            self._manage_empty_element_in_container(page)

    def _manage_empty_element_in_container(self, container):
        """
        Manage an element shown when the container is empty.
        """

        if container is None:
            # It has been deleted!
            return

        container.element.classList.remove("invent-empty")
        if hasattr(container, "_empty_element"):
            container._empty_element.remove()
            delattr(container, "_empty_element")

        if len(container.content) == 0:
            container._empty_element = document.createElement("div")
            container._empty_element.style.textAlign = "center"
            container._empty_element.innerText = f"Empty {type(container).__name__}"

            if not isinstance(container, Page):
                container.element.classList.add("invent-empty")

            container.element.appendChild(container._empty_element)

        for item in container.content:
            if item.is_container:
                self._manage_empty_element_in_container(item)
