"""
A chart widget that wraps the Chart.js library. See the developer documentation
here: https://www.chartjs.org/docs/latest/.

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
from invent.ui.core import Widget, Event, ChoiceProperty, JSONProperty
from pyscript.web import div, canvas
from pyscript.ffi import to_js, create_proxy
from pyscript import window


#: The types of chart that can be rendered.
_CHARTS = [
    "bar",
    "bubble",
    "doughnut",
    "line",
    "pie",
    "polarArea",
    "radar",
    "scatter",
]


class Chart(Widget):
    """
    Display a chart with the given data. This is a thin wrapper around the
    Chart.js library. See the developer documentation here:

    https://www.chartjs.org/docs/latest/

    The chart property should be one of the following: bar, bubble, doughnut,
    line, polarArea, radar, scatter.

    The data property should be a dictionary that conforms to the Chart.js
    data structure for the type of chart you're rendering. For example, a bar
    chart might look like this:

    ```
    {
        "labels": ["January", "February", "March", "April", "May", "June", "July"],
        "datasets": [
            {
                "label": "My First Dataset",
                "data": [65, 59, 80, 81, 56, 55, 40],
                "fill": False,
                "backgroundColor": "rgb(255, 99, 132)",
                "borderColor": "rgba(255, 99, 132, 0.2)"
            }
        ]
    }
    ```
    """

    chart_type = ChoiceProperty(
        _("The type of chart to display."),
        default_value="bar",
        choices=_CHARTS,
    )

    data = JSONProperty(
        _("The data to display in the chart."),
        default_value={},
    )

    options = JSONProperty(
        _("The options to use when rendering the chart."),
        default_value={},
    )

    chart_updated = Event(
        _("The chart has been updated."),
        chart_type=_("The type of chart to render."),
        data=_("The data to display in the chart."),
        options=_("The options used to render the chart."),
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" width="48px" height="48px" viewBox="0 0 256 256"><path fill="#000" d="M232 208a8 8 0 0 1-8 8H32a8 8 0 0 1-8-8V48a8 8 0 0 1 16 0v94.37L90.73 98a8 8 0 0 1 10.07-.38l58.81 44.11L218.73 90a8 8 0 1 1 10.54 12l-64 56a8 8 0 0 1-10.07.38l-58.81-44.09L40 163.63V200h184a8 8 0 0 1 8 8"/></svg>'  # noqa

    def __init__(self, *args, **kwargs):
        # The canvas element that will contain the chart.
        self.chart_canvas = None
        # The Chart.js instance.
        self.chart_instance = None
        super().__init__(*args, **kwargs)

    def on_data_changed(self):
        """
        Update the chart when the data is updated.
        """
        self._update_chart()

    def on_options_changed(self):
        """
        Update the chart when the options are updated.
        """
        self._update_chart()

    def _update_chart(self):
        """
        If required, kick off Chart.js with the required canvas and given
        settings. Otherwise, update the chart with the current state of the
        options and data.
        """
        if self.parent:
            from invent import chart_js

            chart_args = {"data": self.data}
            if self.chart_type:
                chart_args["type"] = self.chart_type
            if self.options:
                chart_args["options"] = self.options
            if self.chart_instance:
                self.chart_instance.data = to_js(self.data)
                self.chart_instance.options = to_js(self.options)
                self.chart_instance.update()
            else:
                self.chart_instance = chart_js.Chart.new(
                    self.chart_canvas._dom_element, to_js(chart_args)
                )
            # Publish the chart updated event.
            self.publish(
                "chart_updated",
                chart_type=self.chart_type,
                data=self.data,
                options=self.options,
            )

    def render(self):
        element = div(id=self.id)
        self.chart_canvas = canvas()
        element.append(self.chart_canvas)
        # Ensures the chart is properly rendered once added to the DOM.
        window.requestAnimationFrame(
            create_proxy(lambda x: self._update_chart())
        )
        return element
