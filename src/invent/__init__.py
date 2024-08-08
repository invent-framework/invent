"""
The core classes, objects and utility functions of the Invent framework.

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

from pyscript import storage
from .channels import Message, subscribe, publish, unsubscribe, when
from .compatability import is_micropython
from .datastore import DataStore
from .i18n import _, load_translations
from .media import Media, set_media_root, get_media_root
from .ui.app import App
from .utils import get_filenames, play_sound, read_files, show_page
from .speech import listen, say, set_voice
from .task import Task


__all__ = [
    "Message",
    "subscribe",
    "publish",
    "unsubscribe",
    "when",
    "is_micropython",
    "datastore",
    "_",
    "load_translations",
    "Media",
    "media",
    "set_media_root",
    "get_media_root",
    "play_sound",
    "get_filenames",
    "read_files",
    "show_page",
    "go",
    "listen",
    "say",
    "set_voice",
    "Task",
]


#: Default instance of the application's datastore.
datastore = None


async def start_datastore():
    """
    Ensure the datastore is started and referenced properly.
    """
    global datastore
    if not datastore:
        datastore = await storage("invent", storage_class=DataStore)


#: The root from which all media files can be found.
media = Media([], "media")


async def go():
    """
    Start the app.
    """
    await start_datastore()
    App.app().go()
