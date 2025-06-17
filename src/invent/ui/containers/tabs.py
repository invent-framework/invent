"""
The tabs container is used to show a row of columns in a tabbed format.

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

from pyscript.web import div, input_

from invent.i18n import _
from .row import Row

class Tabs(Row):
    """
    Tabs is a horizontal container used to show a row of columns in a tabbed
    format. The Tabs container automatically handles the visibility of its
    children based on the selected child. The Tabs container is useful for
    displaying a large number of child components in a compact manner. The Tabs
    container is a subclass of the Row container and inherits all of its
    properties and methods.
    """

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M255.66 165.7a.2.2 0 0 0 0-.08L233.37 91.4A15.89 15.89 0 0 0 218.05 80H208a8 8 0 0 0 0 16h10.05l19.2 64H206l-20.63-68.6A15.89 15.89 0 0 0 170.05 80H160a8 8 0 0 0 0 16h10.05l19.2 64H158l-20.63-68.6A15.89 15.89 0 0 0 122.05 80H38a15.89 15.89 0 0 0-15.37 11.4L.37 165.6v.13A8.1 8.1 0 0 0 0 168a8 8 0 0 0 8 8h240a8 8 0 0 0 7.66-10.3M38 96h84.1l19.2 64H18.75Z"/></svg>'  # noqa

    def on_children_changed(self):
        """
        Instead of appending children to the element, we create a tree
        structure from divs that allows for tab-like behaviour.

        Each child is wrapped in a div containing a hidden radio input that
        controls its visibility. The radio inputs are grouped by the
        tab's id, allowing only one child to be visible at a time.

        The `tab-item` class is used to style each item, and the
        `tab-title` and `tab-content` classes are used to style
        the title and content divs of each item respectively. The
        tab-title div contains the name of the child component, and
        the tab-content div contains the child element itself.
        """
        self.element.replaceChildren()
        for i, child in enumerate(self.children):
            item = div(
                input_(type="radio", name=self.id, checked=i ==0),
                div(child.name, classes="tab-title"),
                div(child.element, classes="tab-content"),
                classes="tab-item",
            )
            self.element.append(item)
    
    def on_id_changed(self):
        """
        Automatically called to update the id of the HTML element associated
        with the component.
        """
        super().on_id_changed()
        self.on_children_changed()
