import asyncio

import invent
from invent.tools import CodeEditorDonkeyAdapter
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
assert_worker = Html(html=_wait_html("Worker not started."))
assert_run = Html(html=_wait_html("Code not run."))

adapter = CodeEditorDonkeyAdapter(
    code_editor_widget=source_editor,
    output_widget=output_label,
    status_key="codeeditor.worker.status",
    result_key="codeeditor.worker.result",
)


async def ensure_worker():
    if adapter.ready:
        status_label.text = "Donkey ready."
        assert_worker.html = _pass_html("Donkey worker started.")
        return
    status_label.text = "Starting donkey worker..."
    try:
        await adapter.initialize()
        status_label.text = "Donkey ready. Press Run Code."
        assert_worker.html = _pass_html("Donkey worker started.")
    except Exception as exc:
        status_label.text = f"Failed to start donkey: {exc}"
        assert_worker.html = _fail_html(
            f"Donkey worker failed to start: {exc}"
        )


async def run_plugin_code():
    if not adapter.ready:
        status_label.text = "Donkey not ready."
        return
    code = plugin_editor.code or ""
    if not code.strip():
        status_label.text = "Write plugin code first."
        return
    status_label.text = "Running code..."
    result = await adapter.run(code)
    if isinstance(result, dict) and result.get("ok"):
        status_label.text = "Done. Plugin updated output label."
        assert_run.html = _pass_html("Code run succeeded.")
        return
    error = None
    if isinstance(result, dict):
        error = result.get("error")
    if not error:
        error = "Unknown error."
    status_label.text = f"Worker error: {error}"
    assert_run.html = _fail_html(f"Code run failed: {error}")


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
