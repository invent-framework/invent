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
from pyscript import document
from .i18n import load, _


__all__ = ["App"]


class App:
    """
    An instance of App is the root object for an Invent application. General
    app related data hangs off an object of this type. E.g. name, author,
    icon, description, license and other such things.
    """

    def __init__(self, name, icon=None, description=None, author=None, license=None, content=None):
        self.name = name
        self.icon = icon
        self.description = description
        self.author = author
        self.license = license
        self.content = content or []

    def go(self):
        """
        Start the universe.
        """
        # Load the i18n stuff.
        load()
        # Render all the pages to the DOM.
        if self.content:
            for page in self.content:
                document.body.appendChild(page.render())
            # Show the first page.
            self.content[0].show()
        else:
            raise ValueError("No pages in the app!")
