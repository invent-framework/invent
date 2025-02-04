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

import os

from pyscript.web import page as dom  # Avoid name collision with page.
import toga

import invent
from .i18n import load_translations, _


__all__ = [
    "App",
]


# Singleton instance of the App class. There can be only one app running at a
# time.
__app__ = None


class App:
    """
    An instance of App is the root object for an Invent application. General
    app related metadata hangs off an object of this type. E.g. name, author,
    icon, description, license and other such things.

    In addition the user interface, defined by classes found in the invent.ui
    namespace, is rooted in the pages attribute. This is a list of Page
    objects that define the structure of the app. The show_page method is used
    to display a specific page by name. Append new Page instances to the app
    or remove them with the remove method and the name of the page to remove.

    Convenience methods, as_dict and get_page, are provided to return a
    dictionary representation of the app and to retrieve a page by name. The
    app method is a class method that returns the singleton instance of the
    App.

    The go method is used to start the app. This is typically called at the end
    of the script that defines the app.
    """

    def __init__(
        self,
        *args,
        name="",
        media_root=".",
        icon=None,
        description=None,
        author=None,
        license=None,
        pages=None,
    ):
        """
        Create a new instance of App.

        Pass in one or more Page objects as arguments to define the structure
        of the app. Alternatively, pass in a list of Page objects as the
        content argument.

        Every app must have a name. The media_root is the root URL for
        media files (sounds, images etc). The icon is a URL to an image that
        represents the app. This will be used in the user's operating system to
        identify the app. The description should explain what the application
        does. The author is a string that identifies the author[s] of the app
        and how to contact them. The license is a string containing the license
        under which the app is released. The content is a list of Page objects
        that define the structure of the app (as an explicit alternative to
        passing them in as arguments).
        """
        global __app__
        if not __app__:
            __app__ = self
        if not name:
            raise ValueError(_("An app must have a name."))
        self.name = name
        self.icon = icon
        self.description = description
        self.author = author
        self.license = license
        self._pages = []  # Ordered list of pages.
        self._page_lookup_table = {}  # A dict to easily look up pages by name.

        # We don't use any features of the App class, but the Window requires
        # it to exist.
        os.environ["TOGA_BACKEND"] = "toga_invent"
        self.toga_app = toga.App(self.name, "io.github.invent-framework")

        # toga_invent uses the window ID as a CSS selector determining which
        # element to display the content in.
        self.toga_window = toga.Window("body")

        if args:
            self.append(*args)
        if pages:
            self.append(*pages)
        invent.set_media_root(media_root)

    @property
    def pages(self):
        """
        Return a list of all the pages in the app.
        """
        return self._pages

    def append(self, *pages):
        """
        Append one or more Page objects to the app.
        """
        for page in pages:
            if page.id in self._page_lookup_table:
                raise ValueError(
                    _("A page with the id {name} already exists.").format(
                        name=page.id
                    )
                )
            self._pages.append(page)
            self._page_lookup_table[page.id] = page

    def remove(self, *page_ids):
        """
        Remove one or more Page objects, referenced by id, from the app.
        """
        for page_id in page_ids:
            if page_id in self._page_lookup_table:
                page = self._page_lookup_table[page_id]
                self._pages.remove(page)
                del self._page_lookup_table[page_id]
            else:
                raise KeyError(
                    _("No page with the id: {page_id}").format(page_id=page_id)
                )

    def as_dict(self):
        """
        Return a dictionary representation of the application. This should be
        serializable to JSON.
        """
        return dict(
            name=self.name,
            icon=self.icon,
            description=self.description,
            author=self.author,
            license=self.license,
            pages=[page.as_dict() for page in self.pages],
        )

    @classmethod
    def app(cls):
        """
        Return the singleton instance of the App class.
        """
        global __app__
        return __app__

    def get_page(self, page_id):
        """
        Return the page with the specified id or raise a KeyError if no such
        page exists.
        """
        if page_id in self._page_lookup_table:
            return self._page_lookup_table[page_id]
        else:
            raise KeyError(
                _("No page with the id: {page_id}").format(page_id=page_id)
            )

    def show_page(self, page_id):
        """
        Show the page with the specified id. Hide the current page if there
        is one.
        """
        self.toga_window.content = self.get_page(page_id)

    def go(self):
        """
        Start the universe.
        """
        # Set the page title.
        dom.title = self.name
        # Load the i18n assets.
        load_translations()

        if self.pages:
            # Show the first page.
            self.show_page(self.pages[0].id)
        else:
            raise ValueError(_("No pages in the app!"))
