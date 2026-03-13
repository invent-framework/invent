"""
A code display widget for the Invent framework.

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

from pyscript.ffi import to_js
from pyscript.web import div
from invent.i18n import _
from invent.ui.core import Widget, TextProperty, BooleanProperty

_default = """
def hello(name="world"):
    return f"Hello, {name}"
"""

# Themes passed to Shiki for light and dark mode. Shiki embeds both as CSS
# custom properties on each token; the dark values are activated by the
# @media rule injected into the page head by load_js_modules().
_THEMES = {"light": "github-light", "dark": "github-dark"}


class Code(Widget):
    """
    Display syntax-highlighted code in the UI.
    """

    code = TextProperty(
        _("The code to display."),
        default_value=_default,
    )

    language = TextProperty(
        _("The language of the code."),
        default_value="python",
    )

    line_numbers = BooleanProperty(
        _("Flag for displaying line numbers."),
        default_value=False,
    )

    highlight = TextProperty(
        _("Lines to highlight, e.g. '1' or '1,3-5'."),
        default_value=None,
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M69.12 94.15L28.5 128l40.62 33.85a8 8 0 1 1-10.24 12.29l-48-40a8 8 0 0 1 0-12.29l48-40a8 8 0 0 1 10.24 12.3m176 27.7l-48-40a8 8 0 1 0-10.24 12.3L227.5 128l-40.62 33.85a8 8 0 1 0 10.24 12.29l48-40a8 8 0 0 0 0-12.29m-82.39-89.37a8 8 0 0 0-10.25 4.79l-64 176a8 8 0 0 0 4.79 10.26A8.14 8.14 0 0 0 96 224a8 8 0 0 0 7.52-5.27l64-176a8 8 0 0 0-4.79-10.25"/></svg>'  # noqa

    async def _highlight_code(self):
        """
        Re-render the highlighted code block using Shiki. Imported lazily to
        avoid a circular import at module load time.
        """
        from invent import (
            shiki,
            shiki_transformers,
        )  # Avoid circular import at module load time.

        options = {"lang": self.language, "themes": _THEMES}
        if self.highlight:
            # Wrap the highlight spec in braces as Shiki's meta string format
            # requires, e.g. '1,3-5' becomes '{1,3-5}'.
            options["meta"] = {"__raw": "{" + self.highlight + "}"}
            options["transformers"] = [
                shiki_transformers.transformerMetaHighlight()
            ]
        options = to_js(options)
        html = await shiki.codeToHtml(self.code, options)
        self._container.replaceChildren()
        self._container._dom_element.innerHTML = html
        self._update_line_numbers()

    def _update_line_numbers(self):
        """
        Add or remove the line-numbers CSS class on the Shiki-generated
        <pre> element without triggering a full re-highlight.
        """
        pre_results = self._container.find("pre")
        if not pre_results:
            # No <pre> element found, probably because the code is empty.
            return
        pre = pre_results[0]
        if self.line_numbers:
            pre.classes.add("line-numbers")
        else:
            pre.classes.remove("line-numbers")

    async def on_code_changed(self):
        """
        Re-highlight when the code content changes.
        """
        await self._highlight_code()

    async def on_language_changed(self):
        """
        Re-highlight when the language changes.
        """
        await self._highlight_code()

    def on_line_numbers_changed(self):
        """
        Toggle line numbers without re-highlighting.
        """
        self._update_line_numbers()

    async def on_highlight_changed(self):
        """
        Re-highlight when the highlighted lines change.
        """
        await self._highlight_code()

    def render(self):
        """
        Return a container div. Shiki generates its own <pre> block which is
        inserted as innerHTML.
        """
        self._container = div(id=self.id)
        return self._container
