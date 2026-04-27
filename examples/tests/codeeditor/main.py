import asyncio

import invent
from invent.tools import (
    CodeEditorDonkeyAdapter,
    make_assertion_callbacks,
    make_plugin_runner,
)
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


def _set_codeeditor_status(text):
    # Set visible label and publish a status message.
    status_label.text = text
    invent.publish(
        invent.Message("status", status=text), to_channel="codeeditor"
    )


class _StatusProxy:
    # Minimal proxy exposing `text` for plugin runners.
    @property
    def text(self):
        return status_label.text

    @text.setter
    def text(self, value):
        _set_codeeditor_status(value)


status = _StatusProxy()
assert_worker = Html(html=_wait_html("Worker not started."))
assert_run = Html(html=_wait_html("Code not run."))
callbacks = make_assertion_callbacks(
    worker_assert_widget=assert_worker,
    run_assert_widget=assert_run,
    pass_html=_pass_html,
    fail_html=_fail_html,
)

adapter = CodeEditorDonkeyAdapter(
    code_editor_widget=source_editor,
    output_widget=output_label,
    status_key="codeeditor.worker.status",
    result_key="codeeditor.worker.result",
)
_, ensure_worker, run_plugin_code = make_plugin_runner(
    adapter=adapter,
    status_widget=status,
    code_getter=lambda: plugin_editor.code or "",
    success_text="Done. Plugin updated output label.",
    **callbacks,
)


async def handle_controls(message):
    if getattr(message.source, "name", "") == "run_codeeditor_plugin":
        await run_plugin_code()


invent.subscribe(
    handle_controls,
    to_channel="codeeditor-controls",
    when_subject=["press"],
)

asyncio.create_task(ensure_worker())

app = invent.App(
    name="CodeEditor Donkey Interactive Test",
    pages=[
        Page(
            id="codeeditor-donkey-test",
            children=[
                Html(
                    html=(
                        '<p><a href="../index.html">'
                        "Back to interactive tests</a></p>"
                    )
                ),
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
