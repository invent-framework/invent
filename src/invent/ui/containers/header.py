"""
A header is a horizontal container used to show a navigation bar on the top of
the page. The header can be sticky, meaning it will stay at the top of the page
even when the user scrolls down. Typically the header contains a logo, a title,
and a menu.

```
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
```
"""

from invent.i18n import _
from .row import Row
from ..core.property import BooleanProperty


class Header(Row):
    """
    Header is a horizontal container used to show a navigation bar on the top
    of the page. The header can be sticky, meaning it will stay at the top of
    the page even when the user scrolls down. Typically the header contains a
    logo, a title, and a menu.

    The Header is useful for displaying a consistent navigation experience
    across different pages. The Header is a subclass of the Row container and
    inherits all of its properties and methods.
    """

    sticky = BooleanProperty(
        _(
            "Whether the header should be sticky (i.e. stay at the top of the page even when the user scrolls down)."
        ),
        default_value=False,
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 256 256"><path d="M216,40H40A16,16,0,0,0,24,56V200a16,16,0,0,0,16,16H216a16,16,0,0,0,16-16V56A16,16,0,0,0,216,40Zm0,16V88H40V56Zm0,144H40V104H216v96Z"></path></svg>'  # noqa

    def on_sticky_changed(self):
        """
        Update the header's CSS class when the sticky property changes.
        """
        if self.sticky:
            self.element.classes.add("invent-header--sticky")
        else:
            self.element.classes.remove("invent-header--sticky")
