"""
A table widget for the Invent framework.

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

from invent.i18n import _
from pyscript.web import table, caption, thead, tbody, tr, th, td
from invent.ui.core import Widget, ListProperty, TextProperty, BooleanProperty


class Table(Widget):
    """
    A table widget for displaying tabular data.
    """

    data = ListProperty(
        _("The text/numeric data to display in the table."),
        default_value=[
            ["Header 1", "Header 2"],
            ["Row 1, Cell 1", "Row 1, Cell 2"],
            ["Row 2, Cell 1", "Row 2, Cell 2"],
        ],
    )

    label = TextProperty(
        _("An optional label for the table."), default_value=""
    )

    column_headers = BooleanProperty(
        _("A flag to indicate if the first row of the table is a header row."),
        default_value=True,
        group="style",
    )

    row_headers = BooleanProperty(
        _("A flag to indicate if the first item in each row is a header."),
        default_value=False,
        group="style",
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><path fill="currentColor" d="M224 48H32a8 8 0 0 0-8 8v136a16 16 0 0 0 16 16h176a16 16 0 0 0 16-16V56a8 8 0 0 0-8-8M40 112h40v32H40Zm56 0h120v32H96Zm120-48v32H40V64ZM40 160h40v32H40Zm176 32H96v-32h120z"/></svg>'  # noqa

    def _tabulate(self):
        """
        Convert the data into a table, given the current settings.
        """
        # Reset the table in the DOM.
        self._table_head._dom_element.replaceChildren()
        self._table_body._dom_element.replaceChildren()
        # If there's no data, there's nothing to do.
        if self.data:
            temp_data = self.data[:]
            # If the first row contains the column headers, use it as such.
            if self.column_headers:
                self._table_head.append(
                    tr(*[th(header) for header in temp_data[0]])
                )
                temp_data = temp_data[1:]
            # If the first item in each row is a header, use it as such.
            if self.row_headers:
                self._table_body.append(
                    [
                        tr(th(row[0]), *[td(cell) for cell in row[1:]])
                        for row in temp_data
                    ]
                )
            else:
                self._table_body.append(
                    [tr(*[td(cell) for cell in row]) for row in temp_data]
                )

    def on_data_changed(self):
        self._tabulate()

    def on_column_headers_changed(self):
        self._tabulate()

    def on_row_headers_changed(self):
        self._tabulate()

    def on_label_changed(self):
        self._caption.innerText = self.label

    def render(self):
        self._caption = caption(self.label)
        self._table_head = thead()
        self._table_body = tbody()

        return table(
            self._caption,
            self._table_head,
            self._table_body,
            id=self.id,
        )
