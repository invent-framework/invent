"""
A rich text editor widget for the Invent framework, powered by
Quill 2. All JavaScript dependencies are loaded lazily within this
module and do not touch the top-level invent __init__.py.

Markdown conversion uses:
  - quill-delta-to-markdown (frysztak) for Delta ops → Markdown.
  - markdown-to-quill-delta (frysztak) for Markdown → Delta ops.

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

import asyncio
import json
import js
from pyscript import js_import
from pyscript.ffi import create_proxy
from pyscript.web import div
from invent.i18n import _
from invent.ui.core import (
    Widget,
    DictProperty,
    Event,
    TextProperty,
)

# Delay in seconds before the changed event fires after the user
# stops typing.
_DEBOUNCE_DELAY = 0.3

# CDN URLs for Quill and its Snow theme stylesheet.
_QUILL_JS = "https://esm.sh/quill@2.0.3"
_QUILL_CSS = "https://cdn.jsdelivr.net/npm/quill@2.0.3/dist/quill.snow.css"

# ESM-compatible URLs for the Markdown ↔ Delta conversion libraries.
# esm.sh wraps CommonJS packages as ES modules automatically.
_DELTA_TO_MD_JS = "https://esm.sh/quill-delta-to-markdown@0.6.0"
_MD_TO_DELTA_JS = "https://esm.sh/markdown-to-quill-delta@1.0.1"

# Default Quill 2 toolbar and editor configuration.
_DEFAULT_CONFIG = {
    "modules": {
        "toolbar": [
            [{"header": [1, 2, False]}],
            ["bold", "italic", "underline"],
            ["image", "code-block"],
        ],
    },
    "placeholder": "Compose an epic...",
    "theme": "snow",
}


class TextEditor(Widget):
    """
    A rich text editor with formatting options and debounced change
    events. Quill 2 is used as the underlying editor.

    The `text` property exposes editor content as Markdown. The
    `delta` property exposes the raw Quill Delta structure. Both are
    kept in sync automatically.

    Configuration is supplied once at construction via the `config`
    keyword argument and cannot be changed afterwards.
    """

    text = TextProperty(
        _("The textual content of the editor as Markdown."),
        default_value="",
    )

    delta = DictProperty(
        _(
            "The underlying Quill Delta representation of the "
            "editor content."
        ),
        default_value={},
    )

    min_height = TextProperty(
        _("Minimum height of the editor as a CSS length " "(e.g. '200px')."),
        default_value="200px",
        group="style",
    )

    changed = Event(
        _("Fired when the user edits the text (debounced)."),
        text=_("The new Markdown textual content after the change."),
    )

    def __init__(self, config=None, **kwargs):
        # _config must be set before super().__init__() because
        # render() is called from within the parent's __init__.
        self._config = config if config is not None else _DEFAULT_CONFIG
        self._quill = None  # Quill instance; set after async init.
        self._updating = False  # Guards against feedback loops.
        self._debounce_task = None  # Current debounce coroutine.
        super().__init__(**kwargs)

    @classmethod
    def icon(cls):
        """Return a pencil SVG icon for the Invent UI builder."""
        return (
            '<svg xmlns="http://www.w3.org/2000/svg"'
            ' fill="currentColor" viewBox="0 0 256 256">'
            '<path d="M128,96H232a8,8,0,0,1,0,16H128a8,8,0,0,1,'
            "0-16Zm104,32H128a8,8,0,0,0,0,16H232a8,8,0,0,0,0-16Zm"
            "0,32H80a8,8,0,0,0,0,16H232a8,8,0,0,0,0-16Zm0,32H80a8,"
            "8,0,0,0,0,16H232a8,8,0,0,0,0-16ZM96,144a8,8,0,0,0,0-"
            "16H88V64h32v8a8,8,0,0,0,16,0V56a8,8,0,0,0-8-8H32a8,8,"
            "0,0,0-8,8V72a8,8,0,0,0,16,0V64H72v64H64a8,8,0,0,0,0,"
            '16Z"/></svg>'
        )

    def render(self):
        """
        Create the editor container and schedule Quill initialisation.
        Returns the outer pyscript.web div that becomes self.element.
        """
        container = div()
        container.classList.add("invent-text-editor")
        # Quill requires a native DOM element as its mount target.
        # A raw JS element is used here to avoid PyScript proxy
        # unwrapping issues when passing it to the Quill constructor.
        self._mount = js.document.createElement("div")
        container._dom_element.appendChild(self._mount)
        asyncio.create_task(self._init_quill())
        return container

    async def _init_quill(self):
        """
        Dynamically load Quill and the conversion libraries, then
        mount the editor on self._mount.
        """
        # Inject the Quill Snow CSS into <head> once per page.
        if not js.document.querySelector(f'link[href="{_QUILL_CSS}"]'):
            link = js.document.createElement("link")
            link.rel = "stylesheet"
            link.href = _QUILL_CSS
            js.document.head.appendChild(link)

        # Fetch all three JS modules in parallel.
        quill_mod, delta_to_md_mod, md_to_delta_mod = await js_import(
            _QUILL_JS, _DELTA_TO_MD_JS, _MD_TO_DELTA_JS
        )

        # quill-delta-to-markdown: named export deltaToMarkdown(ops).
        # markdown-to-quill-delta: default export markdownToDelta(md).
        Quill = quill_mod.default
        self._delta_to_markdown = delta_to_md_mod.deltaToMarkdown
        self._markdown_to_delta = md_to_delta_mod.default

        # Mount Quill. Config is serialised via JSON to guarantee that
        # Python booleans (e.g. False in header levels) become JS
        # booleans rather than Python proxy objects.
        config_js = js.JSON.parse(json.dumps(self._config))
        self._quill = Quill.new(self._mount, config_js)

        # Apply any property values that were set before Quill was
        # ready.
        self.on_min_height_changed()
        if self.text:
            self._load_markdown(self.text)
        elif self.delta.get("ops"):
            self._load_delta(self.delta)

        # Attach a debounced listener for all user-driven changes.
        def _on_change(delta, old, source):
            """Reschedule the debounced sync on every edit."""
            if self._debounce_task:
                self._debounce_task.cancel()
            self._debounce_task = asyncio.create_task(self._debounced_sync())

        self._quill.on("text-change", create_proxy(_on_change))

    async def _debounced_sync(self):
        """
        Wait for typing to pause, then read Quill's content, update
        both Python properties, and publish the changed event.
        """
        try:
            await asyncio.sleep(_DEBOUNCE_DELAY)
        except asyncio.CancelledError:
            return
        if self._quill is None:
            return

        # Read ops from Quill as a JS array and convert to Python.
        ops_js = self._quill.getContents().ops
        markdown = str(self._delta_to_markdown(ops_js))
        ops = json.loads(str(js.JSON.stringify(ops_js)))

        # Update both properties without triggering their own
        # on_*_changed handlers, which would push content back into
        # Quill and create an infinite loop.
        self._updating = True
        try:
            self.delta = {"ops": ops}
            self.text = markdown
        finally:
            self._updating = False

        self.publish("changed", text=self.text)

    def _load_markdown(self, markdown):
        """
        Convert markdown to a Quill Delta and load it into the editor
        silently, without triggering the changed event.
        """
        if self._quill is None:
            return
        ops_js = self._markdown_to_delta(markdown)
        # Wrap the ops array in a plain JS object for setContents.
        delta_obj = js.Object.new()
        delta_obj.ops = ops_js
        self._quill.setContents(delta_obj, "silent")

    def _load_delta(self, delta_dict):
        """
        Load a Python delta dict into the editor silently, without
        triggering the changed event.
        """
        if self._quill is None:
            return
        delta_js = js.JSON.parse(json.dumps(delta_dict))
        self._quill.setContents(delta_js, "silent")

    def on_text_changed(self):
        """
        Push a new Markdown value into the editor when text is set
        externally. Skipped if the change originates from Quill itself
        to prevent a feedback loop.
        """
        if self._updating:
            return
        self._load_markdown(self.text)

    def on_delta_changed(self):
        """
        Load a new delta into the editor when the property is set
        externally. Skipped if the change originates from Quill itself
        to prevent a feedback loop.
        """
        if self._updating:
            return
        self._load_delta(self.delta)

    def on_min_height_changed(self):
        """
        Apply the min-height to the outer container and to Quill's
        inner editor area (once it exists).
        """
        self.element.style["min-height"] = self.min_height
        ql_editor = self._mount.querySelector(".ql-editor")
        if ql_editor:
            ql_editor.style.setProperty("min-height", self.min_height)
