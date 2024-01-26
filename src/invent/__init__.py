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
from .pubsub import Message, subscribe, publish, unsubscribe
from .datastore import DataStore
from .page import Page
from .app import App
from .i18n import _
from .media import Media, set_media_root, get_media_root
from .utils import play_sound

__all__ = [
    "Message",
    "subscribe",
    "publish",
    "unsubscribe",
    "DataStore",
    "datastore",
    "App",
    "Page",
    "_",
    "Media",
    "media",
    "set_media_root",
    "get_media_root",
    "play_sound",
]


#: Default instance of the application's datastore.
datastore = DataStore()


#: The root from which all media files can be found.
media = Media([], "media")
