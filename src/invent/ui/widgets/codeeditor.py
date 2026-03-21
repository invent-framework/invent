"""
An interactive code editor widget for the Invent framework, powered by
CodeMirror 6. All JavaScript dependencies are loaded lazily within this
module and do not touch the top-level invent __init__.py. Additional
languages can be registered at runtime via register_language().

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
import js
from pyscript import js_import
from pyscript.ffi import create_proxy, to_js
from pyscript.web import div
from invent.i18n import _
from invent.ui.core import (
    Widget,
    BooleanProperty,
    ChoiceProperty,
    Event,
    TextProperty,
)

# Delay in seconds before the changed event fires after the user stops
# typing.
_DEBOUNCE_DELAY = 0.3

# CodeMirror convenience bundle: exports basicSetup and EditorView.
_cm = None
# @codemirror/state: exports EditorState (not in the convenience bundle).
_cm_state = None
# @codemirror/theme-one-dark: exports oneDark extension.
_cm_dark = None

# Cache of loaded language pack modules, keyed by language name.
_lang_packs = {}

# Known CodeMirror language pack ESM URLs. Follows the
# @codemirror/lang-<n> convention on esm.sh. Extend via
# register_language().
_LANG_URLS = {
    "python": "https://esm.sh/@codemirror/lang-python",
}


def register_language(name, url):
    """
    Register a CodeMirror language pack URL for on-demand loading.
    The URL must point to an ESM module exporting a zero-argument
    function named after the language (e.g. python(), javascript()).
    """
    _LANG_URLS[name] = url


async def _load_cm():
    """
    Load all core CodeMirror modules if not already loaded. Separated
    from widget init so the cost is paid once across all instances.
    """
    global _cm, _cm_state, _cm_dark
    if _cm is not None:
        return
    _cm, _cm_state, _cm_dark = await js_import(
        # Convenience bundle: basicSetup, EditorView.
        "https://esm.sh/codemirror",
        # State module: EditorState (not re-exported by the bundle).
        "https://esm.sh/@codemirror/state",
        # One-dark theme extension.
        "https://esm.sh/@codemirror/theme-one-dark",
    )


async def _load_lang_pack(language):
    """
    Load and cache the CodeMirror language pack for the given language.
    Returns the pack module, or None if the language is not registered
    in _LANG_URLS.
    """
    if language in _lang_packs:
        return _lang_packs[language]
    url = _LANG_URLS.get(language)
    if not url:
        return None
    (pack,) = await js_import(url)
    _lang_packs[language] = pack
    return pack


class CodeEditor(Widget):
    """
    An interactive code editor with syntax highlighting and debounced
    change events. Language packs are loaded on demand when the language
    property changes.
    """

    code = TextProperty(
        _("The code content of the editor."),
        default_value="",
    )

    language = TextProperty(
        _("The language for syntax highlighting."),
        default_value="python",
    )

    readonly = BooleanProperty(
        _("Whether the editor content can be edited."),
        default_value=False,
    )

    min_height = TextProperty(
        _("Minimum height of the editor as a CSS length (e.g. '200px')."),
        default_value="200px",
        group="style",
    )

    theme = ChoiceProperty(
        _("The colour theme of the editor."),
        default_value="auto",
        choices=["light", "dark", "auto"],
        group="style",
    )

    changed = Event(
        _("Fired when the user edits the code (debounced)."),
        code=_("The new code content after the change."),
    )

    @classmethod
    def icon(cls):
        """Return a pencil SVG icon for the Invent UI builder."""
        return '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256"><path d="M58.34,101.66l-32-32a8,8,0,0,1,0-11.32l32-32A8,8,0,0,1,69.66,37.66L43.31,64,69.66,90.34a8,8,0,0,1-11.32,11.32Zm40,0a8,8,0,0,0,11.32,0l32-32a8,8,0,0,0,0-11.32l-32-32A8,8,0,0,0,98.34,37.66L124.69,64,98.34,90.34A8,8,0,0,0,98.34,101.66ZM200,40H176a8,8,0,0,0,0,16h24V200H56V136a8,8,0,0,0-16,0v64a16,16,0,0,0,16,16H200a16,16,0,0,0,16-16V56A16,16,0,0,0,200,40Z"></path></svg>'  # noqa

    def __init__(self, **kwargs):
        """
        Initialise editor state before calling super().__init__() so
        that all instance variables exist when property changes fire
        during parent initialisation.
        """
        # The live CodeMirror EditorView instance.
        self._view = None
        # Guard: True while we are setting code programmatically, so
        # that on_code_changed does not dispatch back into CodeMirror.
        self._setting_code = False
        # Handle for the in-flight debounce coroutine.
        self._debounce_task = None
        # Proxy for the CodeMirror updateListener; kept alive so it
        # is not garbage-collected between reconfigurations.
        self._update_proxy = create_proxy(self._on_cm_update)
        # Proxy for the OS colour-scheme media query listener; only
        # set when theme is "auto".
        self._mq_proxy = None
        super().__init__(**kwargs)

    def render(self):
        """
        Render the editor container and kick off async CodeMirror init.
        """
        element = div(classes=["invent-code-editor"])
        element.style["min-height"] = self.min_height
        asyncio.create_task(self._init_editor())
        return element

    # ------------------------------------------------------------------
    # Dark mode helpers
    # ------------------------------------------------------------------

    def _is_dark(self):
        """
        Resolve whether the dark theme should be active, accounting for
        "auto" mode by reading the OS colour-scheme preference.
        """
        if self.theme == "dark":
            return True
        if self.theme == "auto":
            return js.window.matchMedia("(prefers-color-scheme: dark)").matches
        return False

    def _remove_mq_listener(self):
        """
        Remove the OS colour-scheme media query listener if one is
        active, and release the proxy to avoid a memory leak.
        """
        if self._mq_proxy is None:
            return
        js.window.matchMedia(
            "(prefers-color-scheme: dark)"
        ).removeEventListener("change", self._mq_proxy)
        self._mq_proxy.destroy()
        self._mq_proxy = None

    # ------------------------------------------------------------------
    # Editor initialisation and reconfiguration
    # ------------------------------------------------------------------

    async def _build_extensions(self):
        """
        Assemble the CodeMirror extensions list for the current property
        values, including theme, language pack, readonly state, and the
        update listener. Registers the OS theme-change listener when in
        auto mode. Returns a JS array for EditorState.create.
        """
        extensions = [_cm.basicSetup]
        if self._is_dark():
            extensions.append(_cm_dark.oneDark)
        pack = await _load_lang_pack(self.language)
        if pack:
            # Language packs export a zero-argument function named
            # after the language (e.g. python(), javascript(), html()).
            lang_fn = getattr(pack, self.language, None)
            if lang_fn:
                extensions.append(lang_fn())
        if self.readonly:
            extensions.append(_cm.EditorView.editable.of(False))
        extensions.append(_cm.EditorView.updateListener.of(self._update_proxy))
        # In auto mode, watch for OS theme changes and reconfigure.
        if self.theme == "auto" and self._mq_proxy is None:
            self._mq_proxy = create_proxy(
                lambda _e: asyncio.create_task(self._reconfigure())
            )
            js.window.matchMedia(
                "(prefers-color-scheme: dark)"
            ).addEventListener("change", self._mq_proxy)
        return to_js(extensions)

    async def _init_editor(self):
        """
        Load CodeMirror modules, then create the EditorState and mount
        the EditorView into the widget's DOM element. Sets min-height
        on the inner .cm-editor element to match the widget property.
        """
        await _load_cm()
        extensions = await self._build_extensions()
        state = _cm_state.EditorState.create(
            to_js({"doc": self.code or "", "extensions": extensions})
        )
        self._view = _cm.EditorView.new(
            to_js(
                {
                    "state": state,
                    "parent": self.element._dom_element,
                }
            )
        )
        # Set height on the CodeMirror element directly, since it
        # is only available after mount.
        cm_el = self.element._dom_element.querySelector(".cm-editor")
        if cm_el:
            cm_el.style.height = self.min_height

    async def _reconfigure(self):
        """
        Rebuild extensions and replace the editor state, preserving the
        current document content. Called after language, readonly, or
        theme changes.
        """
        if self._view is None:
            return
        extensions = await self._build_extensions()
        doc = self._view.state.doc.toString()
        state = _cm_state.EditorState.create(
            to_js({"doc": doc, "extensions": extensions})
        )
        self._view.setState(state)

    # ------------------------------------------------------------------
    # CodeMirror update listener and debounced event emission
    # ------------------------------------------------------------------

    def _on_cm_update(self, update):
        """
        Receive a CodeMirror transaction and schedule a debounced
        changed event if the document content has actually changed.
        """
        if not update.docChanged:
            return
        if self._debounce_task:
            self._debounce_task.cancel()
        self._debounce_task = asyncio.create_task(self._emit_changed())

    async def _emit_changed(self):
        """
        Wait for the debounce delay, then sync code to the property and
        publish the changed event.
        """
        await asyncio.sleep(_DEBOUNCE_DELAY)
        self._setting_code = True
        self.code = self._view.state.doc.toString()
        self._setting_code = False
        self.publish("changed", code=self.code)

    # ------------------------------------------------------------------
    # Property change handlers
    # ------------------------------------------------------------------

    def on_code_changed(self):
        """
        Push a new value into the CodeMirror view when code is set
        externally, without triggering the changed event feedback loop.
        """
        if self._setting_code or self._view is None:
            return
        self._view.dispatch(
            to_js(
                {
                    "changes": {
                        "from": 0,
                        "to": self._view.state.doc.length,
                        "insert": self.code or "",
                    }
                }
            )
        )

    def on_min_height_changed(self):
        """
        Apply the new minimum height to both the container and the
        inner .cm-editor element.
        """
        if self.element is None:
            return
        self.element.style["min-height"] = self.min_height
        cm_el = self.element._dom_element.querySelector(".cm-editor")
        if cm_el:
            cm_el.style.height = self.min_height

    def on_language_changed(self):
        """
        Load the new language pack and reconfigure the editor.
        """
        asyncio.create_task(self._reconfigure())

    def on_readonly_changed(self):
        """
        Toggle the editor's editable state by reconfiguring.
        """
        asyncio.create_task(self._reconfigure())

    def on_theme_changed(self):
        """
        Remove any active media query listener and reconfigure the
        editor with the appropriate theme.
        """
        self._remove_mq_listener()
        asyncio.create_task(self._reconfigure())
