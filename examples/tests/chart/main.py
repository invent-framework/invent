import invent
import sys
import os
from pathlib import Path
from invent.tools import make_helper
from invent.ui import *

from invent.tools.common_ui import (
    back_link_widget,
    fail_html,
    make_status_setter,
    pass_html,
    publish_run,
    wait_html,
)

await invent.setup()


chart = Chart(
    chart_type="bar",
    data={
        "labels": ["A", "B", "C"],
        "datasets": [
            {
                "label": "Values",
                "data": [3, 5, 2],
                "backgroundColor": "rgba(54, 162, 235, 0.5)",
            }
        ],
    },
    options={"plugins": {"legend": {"display": True}}},
)

status_label = Label(text="Donkey starting...")
_set_chart_status = make_status_setter(invent, status_label, channel="chart")

default_code = (
    "# Inputs: chart_type, data, options\n"
    "# Assign a dict to result with optional data/options keys.\n"
    "new_data = dict(data)\n"
    "datasets = [dict(ds) for ds in data.get('datasets', [])]\n"
    "if datasets:\n"
    "    first = dict(datasets[0])\n"
    "    values = list(first.get('data', []))\n"
    "    first['data'] = [value * 2 for value in values]\n"
    "    first['label'] = 'Values x2'\n"
    "    datasets[0] = first\n"
    "new_data['datasets'] = datasets\n"
    "result = {'data': new_data}\n"
)

code_editor = CodeEditor(
    code=default_code,
    language="python",
    min_height="260px",
)

assert_worker = Html(html=wait_html("Worker not started."))
assert_run = Html(html=wait_html("Code not run."))

HELPER_CHANNEL = "chart-helper"

make_helper(src="chart_helper.py", channel=HELPER_CHANNEL)


def handle_helper_status(msg):
    state = getattr(msg, "state", None)
    detail = getattr(msg, "detail", None)
    if state == "starting":
        _set_chart_status("Starting donkey worker...")
    elif state == "ready":
        _set_chart_status("Donkey ready. Press Run Code.")
        assert_worker.html = pass_html("Donkey worker ready.")
    elif state == "busy":
        _set_chart_status("Running code...")
    elif state == "error":
        _set_chart_status(f"Failed to start donkey: {detail}")
        assert_worker.html = fail_html(f"Donkey worker failed: {detail}")


def handle_helper_result(msg):
    if msg.function != "run":
        return
    if msg.error:
        _set_chart_status(f"Worker error: {msg.error}")
        assert_run.html = fail_html(f"Code run failed: {msg.error}")
        return
    payload = msg.result
    if not isinstance(payload, dict):
        assert_run.html = fail_html("Result must be a dict.")
        _set_chart_status("Invalid chart result.")
        return
    if "data" in payload:
        chart.data = payload["data"]
    if "options" in payload:
        chart.options = payload["options"]
    assert_run.html = pass_html("Code run succeeded.")
    _set_chart_status("Done. Chart updated from donkey result.")


invent.subscribe(handle_helper_status, HELPER_CHANNEL, "status")
invent.subscribe(handle_helper_result, HELPER_CHANNEL, "result")


async def handle_controls(message):
    if getattr(message.source, "name", "") != "run_chart_code":
        return
    publish_run(
        invent,
        channel=HELPER_CHANNEL,
        function="run",
        args=[
            chart.chart_type,
            chart.data,
            chart.options,
            code_editor.code or "",
        ],
    )


invent.subscribe(
    handle_controls,
    to_channel="chart-controls",
    when_subject=["press"],
)

app = invent.App(
    name="Chart Donkey Interactive Test",
    pages=[
        Page(
            id="chart-donkey-test",
            children=[
                back_link_widget(),
                Label(text="# Chart Donkey Interactive Test"),
                Label(
                    text=(
                        "Run Python code in a donkey worker to transform "
                        "chart data and apply the result back to the "
                        "widget."
                    )
                ),
                chart,
                Button(
                    text="Run Code",
                    name="run_chart_code",
                    channel="chart-controls",
                ),
                code_editor,
                status_label,
                Label(text="## Assertions"),
                assert_worker,
                assert_run,
            ],
        ),
    ],
)

invent.go()
