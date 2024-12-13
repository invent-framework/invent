"""
The core container base class that holds other components for organising layout
of widgets in the UI of the Invent framework.

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

from pyscript.web import div

from .component import Component
from invent.i18n import _
from .property import ListProperty
from .measures import GAP_SIZES


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

    children = ListProperty(
        _("The child components of the container."),
        default_value=None,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for item in self.children:
            item.parent = self

    def on_children_changed(self):
        self.element.innerHTML = ""
        for child in self.children:
            self.element.append(child.element)

    def _set_gap(self, gap, attr):
        sizes = GAP_SIZES
        size = sizes.get(gap.upper(), "0px")
        self.element.style[attr] = size

    def append(self, item):
        """
        Append like a list.
        """
        # Update the object model.
        item.parent = self
        self.children.append(item)

        # Update the DOM.
        self.element.append(item.element)

    def insert(self, index, item):
        """
        Insert like a list.
        """
        # Update the object model.
        item.parent = self
        self.children.insert(index, item)

        # Update the DOM.
        if item is self.children[-1]:
            self.element.appendChild(item.element)
        else:
            self.element.insertBefore(
                item.element, self.element.childNodes[index]
            )

    def remove(self, item):
        """
        Remove like a list.
        """
        # Update the object model.
        item.parent = None
        self.children.remove(item)

        # Update the DOM.
        item.element.remove()

    def __getitem__(self, index):
        """
        Index items like a list.
        """
        return self.children[index]

    def __iter__(self):
        """
        Iterate like a list.
        """
        return iter(self.children)

    def __delitem__(self, item):
        """
        Delete like a list.
        """
        self.remove(item)

    def contains(self, component):
        """
        Return True if the specified component is in this container.

        This is recursive, so this really means "is a descendant of".
        """
        for item in self.children:
            if item is component:
                return True

            if item.is_container:
                if item.contains(component):
                    return True

        return False

    def render(self):
        """
        Return a div element representing the container.

        Subclasses should call this, then override with the specific details
        for how to add their children in a way that reflects the way they
        lay out their widgets.
        """
        element = div()
        element.classes.add(f"invent-{type(self).__name__.lower()}")
        return element
