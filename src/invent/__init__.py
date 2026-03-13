"""
The core classes, objects and utility functions of the Invent framework.

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

from pyscript import js_import
from pyscript import storage
from pyscript.web import link, style, page
from .channels import Message, subscribe, publish, unsubscribe, when
from .datastore import DataStore, IndexDBBackend
from .i18n import _, load_translations
from .media import Media, set_media_root, get_media_root
from .app import App
from .utils import show_page, is_micropython

__all__ = [
    "Message",
    "subscribe",
    "publish",
    "unsubscribe",
    "when",
    "datastore",
    "_",
    "load_translations",
    "Media",
    "set_media_root",
    "get_media_root",
    "App",
    "show_page",
    "is_micropython",
    "go",
    "init",
    "marked",
    "shiki",
]


#: Default instance of the application's datastore.
datastore = None
#: The default name for the datastore
datastore_name = "invent"


async def start_datastore(_backend=None, **kwargs):
    """
    Ensure the datastore is started and referenced properly.
    """
    global datastore
    if not datastore:
        if _backend is None:
            # Default null storage backend.
            backend_instance = None
        elif _backend == IndexDBBackend:
            # PyScript IndexDB storage backend. Needs awaiting on instantiation.
            backend_instance = await storage(
                datastore_name, storage_class=_backend
            )
        else:
            # Another given storage backend.
            backend_instance = _backend()
        datastore = DataStore(_backend=backend_instance, **kwargs)


#: The marked JavaScript module for parsing markdown.
marked = None
#: The DOMPurify JavaScript module for sanitising HTML.
purify = None
#: The leaflet JavaScript module for mapping.
leaflet = None
#: The chart.js JavaScript module for charting.
chart_js = None
#: The Shiki JavaScript module for syntax highlighting.
shiki = None
#: The Shiki transformers module for line highlighting etc.
shiki_transformers = None


# CSS required by Shiki. The @media block activates Shiki's dark theme tokens
# (embedded as CSS custom properties on each token span). The .highlighted
# rule styles lines marked by transformerMetaHighlight with a neutral tint
# that works in both light and dark mode.
_SHIKI_CSS = """
@media (prefers-color-scheme: dark) {
    .shiki, .shiki span {
        color: var(--shiki-dark) !important;
        background-color: var(--shiki-dark-bg) !important;
    }

    /* Re-assert highlight on the line and all token spans within it. */
    pre.shiki .line.highlighted,
    pre.shiki .line.highlighted span {
        background-color: rgba(255, 200, 0, 0.12) !important;
    }
}

/* Line numbers: CSS counter on Shiki's generated .line spans.
   The line-numbers class on <pre> acts as the toggle. */
pre.shiki.line-numbers {
    counter-reset: line;
}

pre.shiki.line-numbers .line::before {
    counter-increment: line;
    content: counter(line);
    display: inline-block;
    /* Enough width for 3-4 digit line counts. */
    width: 2rem;
    margin-right: 1rem;
    text-align: right;
    /* Muted so numbers don't compete with code. */
    color: #888;
    user-select: none;
}

/* Highlighted lines: neutral tint with a subtle left accent. Works in
   both light and dark mode without needing separate colour values. */
pre.shiki .line.highlighted {
    background-color: rgba(255, 200, 0, 0.15) !important;
    /* Inset box-shadow gives the left accent without affecting layout. */
    box-shadow: inset 3px 0 0 rgba(255, 200, 0, 0.6);
    padding-left: 3px;
}
"""


async def load_js_modules():
    """
    Load the JavaScript modules required by the Invent framework.
    """
    global marked, purify, leaflet, chart_js, shiki, shiki_transformers
    marked, purify, leaflet, chart_js, shiki, shiki_transformers = (
        await js_import(
            # TODO: esm.run all the things here... ;-)
            "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js",
            "https://esm.run/dompurify",
            "https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet-src.esm.js",
            "https://esm.run/chart.js/auto",
            "https://esm.sh/shiki@3",
            "https://esm.sh/@shikijs/transformers",
        )
    )
    # CSS needed for leaflet.
    leaflet_css = link(
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css",
    )
    page.head.append(leaflet_css)
    # CSS needed for Shiki dark mode token activation.
    shiki_style = style(_SHIKI_CSS)
    page.head.append(shiki_style)


#: The root from which all media files can be found.
media = Media([], "media")


async def setup(_databackend=None, **kwargs):
    """
    Setup all the things required by the Invent framework (e.g. datastore / JS
    requirements).

    Takes optional start values for the datastore. The _databackend argument
    can be used to specify the storage backend for the datastore. If not
    provided, the default storage backend is used. Any other keyword arguments
    are passed to the datastore's start method as initial values to seed the
    datastore.
    """
    await start_datastore(_databackend, **kwargs)
    await load_js_modules()


def go():
    """
    Start the app.
    """
    App.app().go()
