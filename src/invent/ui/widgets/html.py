"""
A button widget for the Invent framework.

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


from invent.ui.core import Widget, TextProperty
from pyscript import document


class Html(Widget):
    """
    An "escape-hatch" widget that allows arbitrary html :)
    """

    html = TextProperty("The raw HTML.", default_value="<div>With great power...</div>")

    events = TextProperty(
        "Comma separated list of the DOM events you want the widget to publish to its channel"
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M216 40H40a16 16 0 0 0-16 16v144a16 16 0 0 0 16 16h176a16 16 0 0 0 16-16V56a16 16 0 0 0-16-16m0 160H40V56h176z"/></svg>'  # noqa

    def on_html_changed(self):
        self.element.innerHTML = self.html

    def render(self):
        element = document.createElement("div")
        element.id = self.id
        element.innerHTML = self.html
        return element
