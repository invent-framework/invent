"""
A file upload widget for the Invent framework.

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

from invent.i18n import _
from pyscript.web import input_
from pyscript.ffi import create_proxy

from invent.ui.core import Widget, ListProperty


class FileUpload(Widget):
    """
    A file upload widget.
    """

    # JS Proxy objects are not JSON serializable, which means we can't put them
    # in the datastore. Hence, this widget just maintains a dictionary that
    # maps a filename to its associated proxy.
    _files_ = {}

    @classmethod
    def get_file_by_name(cls, filename):
        """
        Return the File object with the specified name.
        """
        return cls._files_.get(filename)

    @classmethod
    def get_filenames(cls):
        """
        Return the filenames of all files.
        """
        return cls._files_.keys()

    files = ListProperty(_("The files to upload"))

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><g fill="currentColor"><path d="M208 88h-56V32Z" opacity="0.2"/><path d="m213.66 82.34l-56-56A8 8 0 0 0 152 24H56a16 16 0 0 0-16 16v176a16 16 0 0 0 16 16h144a16 16 0 0 0 16-16V88a8 8 0 0 0-2.34-5.66M160 51.31L188.69 80H160ZM200 216H56V40h88v48a8 8 0 0 0 8 8h48zm-42.34-77.66a8 8 0 0 1-11.32 11.32L136 139.31V184a8 8 0 0 1-16 0v-44.69l-10.34 10.35a8 8 0 0 1-11.32-11.32l24-24a8 8 0 0 1 11.32 0Z"/></g></svg>'  # noqa

    def on_change(self, event):
        """
        Bound to the js "change" event on the widget's element.
        """
        file = event.target.files.item(0)
        # Put the jsproxy in the class-scope dictionary since we can't json
        # serialize it if the files property if bound to the datastore.
        FileUpload._files_[file.name] = file
        # We do list addition here to make the property change (just mutating
        # the list would be unnoticeable).
        self.files = self.files + [file.name]

    def render(self):
        element = input_(type="file", id=self.id)
        element.addEventListener("change", create_proxy(self.on_change))
        return element
