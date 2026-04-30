import asyncio

import invent
from invent.tools import (
    ChartDonkeyAdapter,
    StatusProxy,
    fail_html,
    make_assertion_callbacks,
    make_plugin_runner,
    pass_html,
    wait_html,
)
from invent.ui import *

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
status = StatusProxy(status_label, "chart")

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
callbacks = make_assertion_callbacks(
    worker_assert_widget=assert_worker,
    run_assert_widget=assert_run,
    pass_html=pass_html,
    fail_html=fail_html,
)

adapter = ChartDonkeyAdapter(
    chart_widget=chart,
    status_key="chart.worker.status",
    result_key="chart.worker.result",
)
_, ensure_worker, run_chart_code = make_plugin_runner(
    adapter=adapter,
    status_widget=status,
    code_getter=lambda: code_editor.code or "",
    success_text="Done. Chart updated from donkey result.",
    **callbacks,
)


async def handle_controls(message):
    if getattr(message.source, "name", "") == "run_chart_code":
        await run_chart_code()


invent.subscribe(
    handle_controls,
    to_channel="chart-controls",
    when_subject=["press"],
)

asyncio.create_task(ensure_worker())

app = invent.App(
    name="Chart Donkey Interactive Test",
    pages=[
        Page(
            id="chart-donkey-test",
            children=[
                Html(
                    html=(
                        '<p><a href="../index.html">'
                        "Back to interactive tests</a></p>"
                    )
                ),
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
