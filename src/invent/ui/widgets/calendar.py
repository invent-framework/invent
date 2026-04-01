"""
A calendar is used to display a calendar like view for a given month, and
potentially containing events. Specific dates can be highlighted for further
interaction.

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
from invent.ui.core import Widget, DictProperty, IntegerProperty, Event
from datetime import date, datetime, timedelta
from pyscript import web
from pyscript.ffi import create_proxy

# List of month names for display purposes. The first entry is an empty string
# to make the month numbers 1-indexed for easier readability.
MONTH_NAMES = [
    "",
    _("January"),
    _("February"),
    _("March"),
    _("April"),
    _("May"),
    _("June"),
    _("July"),
    _("August"),
    _("September"),
    _("October"),
    _("November"),
    _("December"),
]

# Day labels ordered Monday-first; rotated by _week_config() for Sunday.
_DAY_NAMES = [
    _("Mon"),
    _("Tue"),
    _("Wed"),
    _("Thu"),
    _("Fri"),
    _("Sat"),
    _("Sun"),
]


class Calendar(Widget):
    """
    A calendar widget for displaying a calendar view for a given month, and
    potentially containing events. Specific dates can be highlighted for
    further interaction.
    """

    # Constants for the days of the week, used for the first_weekday argument
    # to the calendar_weeks() and rednder() methods to specify the first day
    # of the week.
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    year = IntegerProperty(
        _("The year to display."), default_value=date.today().year
    )

    month = IntegerProperty(
        _("The month to display (1=January, 2=February, ..., 12=December)."),
        default_value=date.today().month,
    )

    appointments = DictProperty(
        _(
            "A dictionary of individual appointments to be displayed on the "
            "calendar. The keys should be ISO datetime strings, and the "
            "values should be content to display."
        ),
        default_value={},
    )

    first_day_of_week = IntegerProperty(
        _("The first day of the week. 0=Monday, 1=Tuesday, ..., 6=Sunday."),
        default_value=MONDAY,
    )

    event_clicked = Event(
        _("Triggered when a calendar event is clicked."),
        date=_("The date of the event."),
        time=_("The time of the event."),
        content=_("The content of the event."),
    )

    date_clicked = Event(
        _("Triggered when a date is clicked."),
        date=_("The date that was clicked."),
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 256 256"><path d="M208,32H184V24a8,8,0,0,0-16,0v8H88V24a8,8,0,0,0-16,0v8H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32ZM72,48v8a8,8,0,0,0,16,0V48h80v8a8,8,0,0,0,16,0V48h24V80H48V48ZM208,208H48V96H208V208Zm-68-76a12,12,0,1,1-12-12A12,12,0,0,1,140,132Zm44,0a12,12,0,1,1-12-12A12,12,0,0,1,184,132ZM96,172a12,12,0,1,1-12-12A12,12,0,0,1,96,172Zm44,0a12,12,0,1,1-12-12A12,12,0,0,1,140,172Zm44,0a12,12,0,1,1-12-12A12,12,0,0,1,184,172Z"></path></svg>'  # noqa

    def _days_in_month(self, year, month):
        """
        Return the number of days in the given month and year.
        """
        if month == 12:
            next_month = date(year + 1, 1, 1)
        else:
            next_month = date(year, month + 1, 1)
        return (next_month - timedelta(days=1)).day

    def _day_names(self, first_weekday=MONDAY):
        """
        Return day-name labels rotated so first_weekday is first.
        """
        return _DAY_NAMES[first_weekday:] + _DAY_NAMES[:first_weekday]

    def _group_by_date(self, events):
        """
        Group events by local date, sorted chronologically within each day.

        The input is a dict mapping ISO datetime strings to event content. The
        output is a dict mapping date objects to lists of (time, content) tuples,
        where time is a (hour, minute) tuple.
        """
        by_date = {}
        for iso_str, content in events.items():
            dt = datetime.fromisoformat(iso_str)
            by_date.setdefault(dt.date(), []).append(
                ((dt.hour, dt.minute), content)
            )
        for d in by_date:
            by_date[d].sort()
        return by_date

    def calendar_weeks(self, year, month, events, first_weekday=MONDAY):
        """
        Return the monthly grid as a list of weeks (rows).

        The first_weekday argument controls which day opens each row; use the
        class constants (Calendar.MONDAY, Calendar.TUESDAY, ->
        Calendar.SUNDAY). Each week is a list of 7 items. Padding cells
        outside the current month are None.

        Active cells are dicts with:

            - 'date':   a date object.
            - 'events': sorted list of ((hour, minute), content) tuples.
        """
        by_date = self._group_by_date(events)
        # Column index of the 1st: shift so first_weekday lands on column 0.
        col = (date(year, month, 1).weekday() - first_weekday) % 7
        weeks = []
        row = [None] * col
        for day in range(1, self._days_in_month(year, month) + 1):
            d = date(year, month, day)
            row.append({"date": d, "events": by_date.get(d, [])})
            if len(row) == 7:
                weeks.append(row)
                row = []
        if row:
            weeks.append(row + [None] * (7 - len(row)))
        return weeks

    def _format_time(self, hm):
        """
        Format an (hour, minute) tuple as HH:MM; midnight becomes 'All day'.
        """
        h, m = hm
        if h == 0 and m == 0:
            return "All day"
        return f"{h:02d}:{m:02d}"

    def _day_cell(self, cell, today):
        """
        Build and return a <td> element for an active day cell.
        """
        d = cell["date"]
        evts = cell["events"]
        classes = ["calendar-day"]
        if evts:
            classes.append("has-events")
        if d == today:
            classes.append("calendar-today")
        content = web.div(
            web.span(str(d.day), classes=["calendar-day-num"]),
        )
        content.addEventListener(
            "click",
            create_proxy(
                lambda e, date=d: self.publish(self.date_clicked, date=date)
            ),
        )
        if evts:
            items = []
            for hm, description in evts:
                item = web.li(
                    web.time(self._format_time(hm)), f" {description}"
                )
                item.addEventListener(
                    "click",
                    create_proxy(
                        lambda e, hm=hm, description=description: self.publish(
                            self.event_clicked,
                            date=d,
                            time=hm,
                            content=description,
                        )
                    ),
                )
                items.append(item)
            content.append(web.ul(*items, classes=["calendar-events"]))
        return web.td(content, classes=classes)

    def render_table(self, *args, **kwargs):
        """
        Build and return the calendar table as a pyscript.web table element.

        Events is a dict of ISO 8601 datetime strings -> arbitrary content.
        first_weekday controls the opening day of each row; use the module
        constants (MONDAY, TUESDAY, … SUNDAY).

        Marks today's cell; defaults to the current date when not supplied.
        """
        today = date.today()
        month_name = MONTH_NAMES[self.month]
        weeks = self.calendar_weeks(
            self.year, self.month, self.appointments, self.first_day_of_week
        )

        header_row = web.tr(
            *[web.th(name) for name in self._day_names(self.first_day_of_week)]
        )

        nav = web.nav(
            self.previous_button,
            web.h2(f"{month_name} {self.year}"),
            self.next_button,
            classes=["invent-calendar-nav"],
        )

        body_rows = []
        for week in weeks:
            cells = []
            for cell in week:
                if cell is None:
                    cells.append(web.td(classes=["calendar-empty"]))
                else:
                    cells.append(self._day_cell(cell, today))
            body_rows.append(web.tr(*cells))

        table = web.table(
            web.thead(header_row),
            web.tbody(*body_rows),
        )

        # clear previous content and add the new table
        self.element.replaceChildren()
        self.element.append(nav)
        self.element.append(table)

    # Ensure the table is re-rendered when any of these properties change.
    on_appointments_changed = render_table
    on_year_changed = render_table
    on_month_changed = render_table
    on_first_day_of_week_changed = render_table

    def previous(self, event):
        """
        Navigate to the previous month.
        """
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1

    def next(self, event):
        """
        Navigate to the next month.
        """
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1

    def render(self):
        """
        Return the calendar widget as a pyscript.web div element that
        will contain the calendar table and navigation controls.
        """

        self.previous_button = web.button("‹", classes=["calendar-prev"])
        self.previous_button.addEventListener(
            "click", create_proxy(self.previous)
        )
        self.next_button = web.button("›", classes=["calendar-next"])
        self.next_button.addEventListener("click", create_proxy(self.next))
        return web.div(classes=["invent-calendar"])
