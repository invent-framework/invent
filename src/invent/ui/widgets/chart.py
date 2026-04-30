"""
A chart widget that wraps the Chart.js library. See the developer documentation
here: https://www.chartjs.org/docs/latest/.

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

import asyncio
from pyscript import js_import, window
from pyscript.web import div, canvas
from pyscript.ffi import to_js, create_proxy
from invent.i18n import _
from invent.ui.core import Widget, Event, ChoiceProperty, JSONProperty

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

# Module-level Chart.js reference, loaded once on first use.
_chart_js = None
_chart_js_error = None

# Candidate ESM sources for Chart.js. We try these in order.
_CHART_JS_SOURCES = [
    "https://esm.sh/chart.js@4.5.1/auto?bundle-deps",
    "https://cdn.jsdelivr.net/npm/chart.js@4.5.1/auto/+esm",
    "https://esm.run/chart.js/auto",
]


async def _ensure_chart_js():
    """
    Load Chart.js the first time a Chart widget is rendered.
    """
    global _chart_js, _chart_js_error
    if _chart_js is not None:
        return
    if _chart_js_error is not None:
        raise RuntimeError(_chart_js_error)
    for source in _CHART_JS_SOURCES:
        try:
            (_chart_js,) = await js_import(source)
            _chart_js_error = None
            return
        except Exception as ex:
            _chart_js_error = f"{type(ex).__name__}: {ex}"
    raise RuntimeError(
        "Could not load Chart.js from any configured source. "
        f"Last error: {_chart_js_error}"
    )


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
        options and data. Assumes _ensure_chart_js() has already been awaited
        during render().
        """
        if self.parent:
            if _chart_js is None:
                raise RuntimeError(
                    "Chart.js is not loaded. "
                    "Cannot render chart without JS runtime."
                )
            chart_args = {
                "data": self.data,
                "responsive": True,
                "maintainAspectRatio": False,
            }
            if self.chart_type:
                chart_args["type"] = self.chart_type
            if self.options:
                chart_args["options"] = self.options
            if self.chart_instance:
                self.chart_instance.data = to_js(self.data)
                self.chart_instance.options = to_js(self.options)
                self.chart_instance.update()
            else:
                existing = _chart_js.Chart.getChart(
                    self.chart_canvas._dom_element
                )
                destroy = getattr(existing, "destroy", None)
                if callable(destroy):
                    destroy()
                self.chart_instance = _chart_js.Chart.new(
                    self.chart_canvas._dom_element, to_js(chart_args)
                )
            # Publish the chart updated event.
            self.publish(
                self.chart_updated,
                chart_type=self.chart_type,
                data=self.data,
                options=self.options,
            )

    async def _init_chart(self):
        """
        Load Chart.js then trigger the initial render. Runs as a background
        task started by render() so that render() itself stays synchronous.
        """
        try:
            await _ensure_chart_js()
            window.requestAnimationFrame(
                create_proxy(lambda x: self._update_chart())
            )
        except Exception as ex:
            if self.chart_instance:
                try:
                    self.chart_instance.destroy()
                except Exception:
                    pass
                self.chart_instance = None
            print(f"Chart initialisation failed: {ex}")

    def render(self):
        """
        Return the container element immediately and schedule Chart.js
        loading and initial rendering as a background task.
        """
        element = div(
            id=self.id,
            style={
                "max-width": "100%",
                "overflow": "hidden",
                "display": "block",
                "min-width": "0",
                "position": "relative",
            },
        )
        self.chart_canvas = canvas()
        element.append(self.chart_canvas)
        asyncio.create_task(self._init_chart())
        return element
