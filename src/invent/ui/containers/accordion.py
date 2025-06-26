"""
Contains a definition of an accordian container. This is a vertical
container box in which only one child component is visible at a time.

Based on original pre-COVID work by [Nicholas H.Tollervey](https://ntoll.org/).

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

from pyscript.web import div, input_

from invent.i18n import _
from .column import Column


class Accordion(Column):
    """
    Accordion is a vertical container box in which only one child component is
    visible at a time. The Accordion container automatically handles the
    visibility of its children based on the selected child.

    The Accordion container is useful for displaying a large number of child
    components in a compact manner. The Accordion container is a subclass of
    the Column container and inherits all of its properties and methods.
    """

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M208 88H48a16 16 0 0 0-16 16v96a16 16 0 0 0 16 16h160a16 16 0 0 0 16-16v-96a16 16 0 0 0-16-16m0 112H48v-96h160zM48 64a8 8 0 0 1 8-8h144a8 8 0 0 1 0 16H56a8 8 0 0 1-8-8m16-32a8 8 0 0 1 8-8h112a8 8 0 0 1 0 16H72a8 8 0 0 1-8-8"/></svg>'  # noqa

    def on_children_changed(self):
        """
        Instead of appending children to the element, we create a tree
        structure from divs that allows for accordion-like behaviour.

        Each child is wrapped in a div containing a hidden radio input that
        controls its visibility. The radio inputs are grouped by the
        accordion's id, allowing only one child to be visible at a time.

        The `accordion-item` class is used to style each item, and the
        `accordion-title` and `accordion-content` classes are used to style
        the title and content divs of each item respectively. The
        accordion-title div contains the name of the child component, and
        the accordion-content div contains the child element itself.
        """
        self.element.replaceChildren()
        for i, child in enumerate(self.children):
            item = div(
                input_(type="checkbox", name=self.id, checked=i == 0),
                div(child.name, classes="accordion-title"),
                div(child.element, classes="accordion-content"),
                classes="accordion-item",
            )
            self.element.append(item)

    def on_id_changed(self):
        """
        Automatically called to update the id of the HTML element associated
        with the component.
        """
        super().on_id_changed()
        self.on_children_changed()
