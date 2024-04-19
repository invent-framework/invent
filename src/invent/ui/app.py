"""
Contains the definition of an Invent application.

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

import json
from pyscript import document

import invent
from ..i18n import load_translations, _


__all__ = [
    "App",
]


__app__ = None


class App:
    """
    An instance of App is the root object for an Invent application. General
    app related metadata hangs off an object of this type. E.g. name, author,
    icon, description, license and other such things. In addition, the content
    of Pages defines the UI tree.
    """

    def __init__(
        self,
        name,
        media_root=".",
        icon=None,
        description=None,
        author=None,
        license=None,
        content=None,
    ):
        global __app__
        if not __app__:
            __app__ = self

        self.name = name
        self.icon = icon
        self.description = description
        self.author = author
        self.license = license
        self.content = content or []
        self._current_page = None

        invent.set_media_root(media_root)

    def as_dict(self):
        """
        Return a dictionary representation of the object.
        """

        return dict(
            name=self.name,
            icon=self.icon,
            description=self.description,
            author=self.author,
            license=self.license,
            content=[item.as_dict() for item in self.content],
        )

    def as_json(self):
        return json.dumps(self.as_dict())

    @classmethod
    def app(cls):
        global __app__
        return __app__

    def get_component_by_id(self, component_id):
        """
        Return the component with the specified id or None if no such component
        exists.
        """

        from invent.ui.core import Component

        return Component.get_component_by_id(component_id)

    def get_page_by_id(self, page_id):
        """
        Return the page with the specified id or None if no such page exists.
        """

        for page in self.content:
            if page.id == page_id:
                break

        else:
            page = None

        return page

    def get_page_by_name(self, page_name):
        """
        Return the page with the specified name or None if no such page exists.
        """

        for page in self.content:
            if page.name == page_name:
                break

        else:
            page = None

        return page

    def show_page(self, page_name):
        if self._current_page:
            self._current_page.hide()

        page = self.get_page_by_name(page_name)
        if page is not None:
            self._current_page = page
            page.show()

    def go(self):
        """
        Start the universe.
        """
        # Load the i18n stuff.
        load_translations()
        # Render all the pages to the DOM.
        if self.content:
            for page in self.content:
                document.body.appendChild(page.element)
            # Show the first page.
            self.show_page(self.content[0].name)
        else:
            raise ValueError(_("No pages in the app!"))
