import asyncio

import invent
from invent.tools import ChartDonkeyAdapter, DonkeyPluginFlow
from invent.ui import *

await invent.setup()

_PASS = "color:green;font-family:monospace;margin:4px 0"
_FAIL = "color:red;font-family:monospace;margin:4px 0"
_WAIT = "color:#555;font-family:monospace;margin:4px 0"


def _pass_html(text):
    return f'<p style="{_PASS}">[PASS] {text}</p>'


def _fail_html(text):
    return f'<p style="{_FAIL}">[FAIL] {text}</p>'


def _wait_html(text):
    return f'<p style="{_WAIT}">[ ] {text}</p>'


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

status = Label(text="Donkey starting...")

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

assert_worker = Html(html=_wait_html("Worker not started."))
assert_run = Html(html=_wait_html("Code not run."))

adapter = ChartDonkeyAdapter(
    chart_widget=chart,
    status_key="chart.worker.status",
    result_key="chart.worker.result",
)
flow = DonkeyPluginFlow(adapter=adapter, status_widget=status)


async def ensure_worker():
    result = await flow.ensure_worker(
        ready_text="Donkey ready. Press Run Code."
    )
    if result.get("ok"):
        assert_worker.html = _pass_html("Donkey worker started.")
        return
    error = result.get("error", "Unknown error.")
    assert_worker.html = _fail_html(f"Donkey worker failed to start: {error}")


async def run_chart_code():
    result = await flow.run_code(
        code_editor.code or "",
        success_text="Done. Chart updated from donkey result.",
    )
    if isinstance(result, dict) and result.get("ok"):
        assert_run.html = _pass_html("Code run succeeded.")
        return
    error = result.get("error", "Unknown error.")
    assert_run.html = _fail_html(f"Code run failed: {error}")


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
                status,
                Label(text="## Assertions"),
                assert_worker,
                assert_run,
            ],
        ),
    ],
)

invent.go()
