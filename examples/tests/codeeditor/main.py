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


source_editor = CodeEditor(
    code=(
        "Invent donkey plugins are composable.\n"
        "This text comes from the source editor."
    ),
    language="python",
    min_height="120px",
)

plugin_editor = CodeEditor(
    code=(
        "# Available variable: editor_code\n"
        "lines = editor_code.splitlines()\n"
        "summary = {\n"
        "    'line_count': len(lines),\n"
        "    'char_count': len(editor_code),\n"
        "    'preview': lines[0] if lines else '',\n"
        "}\n"
        "result = {'output': str(summary)}\n"
    ),
    language="python",
    min_height="260px",
)

output_label = Label(text="Output appears here after run.")
status_label = Label(text="Donkey starting...")
_set_codeeditor_status = make_status_setter(
    invent, status_label, channel="codeeditor"
)

assert_worker = Html(html=wait_html("Worker not started."))
assert_run = Html(html=wait_html("Code not run."))

HELPER_CHANNEL = "codeeditor-helper"

make_helper(src="codeeditor_helper.py", channel=HELPER_CHANNEL)


def handle_helper_status(msg):
    state = getattr(msg, "state", None)
    detail = getattr(msg, "detail", None)
    if state == "starting":
        _set_codeeditor_status("Starting donkey worker...")
    elif state == "ready":
        _set_codeeditor_status("Donkey ready. Press Run Code.")
        assert_worker.html = pass_html("Donkey worker ready.")
    elif state == "busy":
        _set_codeeditor_status("Running plugin...")
    elif state == "error":
        _set_codeeditor_status(f"Failed to start donkey: {detail}")
        assert_worker.html = fail_html(f"Donkey worker failed: {detail}")


def handle_helper_result(msg):
    if msg.function != "run":
        return
    if msg.error:
        _set_codeeditor_status(f"Worker error: {msg.error}")
        assert_run.html = fail_html(f"Code run failed: {msg.error}")
        return
    payload = msg.result
    if not isinstance(payload, dict):
        assert_run.html = fail_html("Result must be a dict.")
        return
    out = payload.get("output")
    if out is None:
        assert_run.html = fail_html("Result must include `output`.")
        return
    output_label.text = str(out)
    assert_run.html = pass_html("Code run succeeded.")
    _set_codeeditor_status("Done. Plugin updated output label.")


invent.subscribe(handle_helper_status, HELPER_CHANNEL, "status")
invent.subscribe(handle_helper_result, HELPER_CHANNEL, "result")


async def handle_controls(message):
    if getattr(message.source, "name", "") != "run_codeeditor_plugin":
        return
    publish_run(
        invent,
        channel=HELPER_CHANNEL,
        function="run",
        args=[
            source_editor.code or "",
            plugin_editor.code or "",
        ],
    )


invent.subscribe(
    handle_controls,
    to_channel="codeeditor-controls",
    when_subject=["press"],
)

app = invent.App(
    name="CodeEditor Donkey Interactive Test",
    pages=[
        Page(
            id="codeeditor-donkey-test",
            children=[
                back_link_widget(),
                Label(text="# CodeEditor Donkey Interactive Test"),
                Label(
                    text=(
                        "Run plugin code in a donkey worker. The plugin "
                        "reads source editor text via context and writes "
                        "an output message."
                    )
                ),
                Label(text="## Source Editor (context input)"),
                source_editor,
                Label(text="## Plugin Code"),
                plugin_editor,
                Button(
                    text="Run Code",
                    name="run_codeeditor_plugin",
                    channel="codeeditor-controls",
                ),
                Label(text="## Output"),
                output_label,
                status_label,
                Label(text="## Assertions"),
                assert_worker,
                assert_run,
            ],
        ),
    ],
)

invent.go()
