"""
PyperCard is a simple HyperCard inspired framework for PyScript for building
graphical apps in Python.

Based on original pre-COVID work by [Nicholas H.Tollervey.](https://ntoll.org/)

Copyright (c) 2023 Anaconda Inc.

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
from .core import Card, App

try:
    from .datastore import DataStore
except Exception:
    # Sometimes, due to browser security policy, the localStorage object won't
    # be available, and so the DataStore import won't work. In which case, we
    # just re-use the standard Python dict.
    DataStore = dict


__all__ = [
    "Card",
    "App",
    "DataStore",
]
