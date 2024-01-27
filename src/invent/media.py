"""
A media resolution class for the Invent framework.

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


__all__ = [
    "set_media_root",
    "get_media_root",
    "Media",
]


#: The URL root from which the Media class builds the full path.
__root__ = ""


def set_media_root(root):
    """
    Set the URL root for the media assets.
    """
    global __root__
    __root__ = root


def get_media_root():
    """
    Return the current value of the media root path, under which all media
    objects for an app are found.
    """
    global __root__
    return __root__


class Media:
    """
    Represents the path to a media asset.

    Chain instances of this class together to resolve the desired media asset.

    e.g.

    invent.media.images.goose.png

    Will resolve to the "/media/images/goose.png" asset.

    The path for all Media objects starts with a media root that defaults to
    "". Use the set_media_root() function to override this on a per-app
    basis.
    """

    def __init__(self, path, name):
        """
        The path contains the parent's path as a list. The name is
        (potentially) the end of a path, which should be a file extension
        (like, .jpg, .mp3 etc...).

        If this class becomes a parent to yet another Media object (see:
        __getattribute__), the name is assumed NOT to be a file extension.
        """
        self._path = path
        self._name = name

    def __getattr__(self, attr_name):
        """
        Return a new child Media object.
        """
        return Media(
            self._path
            + [
                self._name,
            ],
            attr_name,
        )

    def __str__(self):
        """
        Get the full URL path for this object (including the file extension).
        """
        global __root__
        full_path = [
            __root__,
        ] + self._path
        return "/".join(full_path) + "." + self._name
