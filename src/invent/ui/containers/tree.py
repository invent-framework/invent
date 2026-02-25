"""
A tree container for the Invent framework. Great for displaying collapsible
hierarchical data (such as a filesystem).

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

from invent.i18n import _
from pyscript.web import nav, details, summary, div

from invent.ui.core import Widget, DictProperty
from invent.ui.widgets.label import Label


class Tree(Widget):
    """
    A tree container for displaying hierarchical data.
    """

    data = DictProperty(
        _(
            "The data to be displayed in the tree. Should be a nested dictionary."
        ),
        default_value={},
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="#000000" viewBox="0 0 256 256"><path d="M176,152h32a16,16,0,0,0,16-16V104a16,16,0,0,0-16-16H176a16,16,0,0,0-16,16v8H88V80h8a16,16,0,0,0,16-16V32A16,16,0,0,0,96,16H64A16,16,0,0,0,48,32V64A16,16,0,0,0,64,80h8V192a24,24,0,0,0,24,24h64v8a16,16,0,0,0,16,16h32a16,16,0,0,0,16-16V192a16,16,0,0,0-16-16H176a16,16,0,0,0-16,16v8H96a8,8,0,0,1-8-8V128h72v8A16,16,0,0,0,176,152ZM64,32H96V64H64ZM176,192h32v32H176Zm0-88h32v32H176Z"></path></svg>'  # noqa

    def on_data_changed(self):
        """
        Re-render the tree when the data changes.
        """
        self.element = self.render()

    def make_tree(self, parent, data):
        """
        Recursively build the tree structure from the provided data.
        """
        for key, value in data.items():
            if isinstance(value, dict):
                # If the value is a dictionary, create a collapsible section
                self.make_branch(parent, key, value)
            else:
                # If the value is not a dictionary, render the element or
                # display the text as a leaf node.
                self.make_leaf(parent, key, value)

    def make_leaf(self, parent, key, value):
        """
        Render a leaf node in the tree, which can be either a widget or a text
        value. A text value is automatically adjusted to a standard label
        widget.
        """
        wrapper = div(classes=["invent-tree-leaf"])
        parent.append(wrapper)
        if isinstance(value, Widget):
            wrapper.append(value.render())
        else:
            wrapper.append(Label(name=key, text=f"{value}").render())

    def make_branch(self, parent, label, subtree):
        """
        Recursive details/summary structure for a branch of the tree.
        """
        details_element = details(summary(Label(name=label, text=label).render()))
        self.make_tree(details_element, subtree)
        parent.append(details_element)

    def render(self):
        """
        Recursively render the tree data as nested HTML elements.
        """
        element = nav(
            classes=[
                "invent-tree",
            ]
        )
        self.make_tree(element, self.data)
        return element
