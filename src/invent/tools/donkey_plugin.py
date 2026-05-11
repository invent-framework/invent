"""Helpers for building user-facing donkey plugin pages."""


class DonkeyPluginFlow:
    """
    Handle common donkey plugin page workflow.

    This keeps page-level `main.py` files small by centralising startup,
    run-state text, and standard error handling.
    """

    def __init__(self, adapter, status_widget):
        self._adapter = adapter
        self._status = status_widget

    @staticmethod
    def _error_from_result(result):
        if isinstance(result, dict):
            error = result.get("error")
            if error:
                return str(error)
        return "Unknown error."

    async def ensure_worker(
        self,
        *,
        ready_text="Donkey ready.",
        starting_text="Starting donkey worker...",
    ):
        if self._adapter.ready:
            self._status.text = ready_text
            return {"ok": True}
        self._status.text = starting_text
        try:
            await self._adapter.initialize()
            self._status.text = ready_text
            return {"ok": True}
        except Exception as exc:
            error = str(exc)
            self._status.text = f"Failed to start donkey: {error}"
            return {"ok": False, "error": error}

    async def run_code(
        self,
        code,
        *,
        running_text="Running code...",
        success_text="Done.",
        not_ready_text="Donkey not ready.",
        empty_code_text="Write plugin code first.",
    ):
        if not self._adapter.ready:
            self._status.text = not_ready_text
            return {"ok": False, "error": not_ready_text}
        if not (code or "").strip():
            self._status.text = empty_code_text
            return {"ok": False, "error": empty_code_text}
        self._status.text = running_text
        result = await self._adapter.run(code)
        if isinstance(result, dict) and result.get("ok"):
            self._status.text = success_text
            return result
        error = self._error_from_result(result)
        self._status.text = f"Worker error: {error}"
        return {"ok": False, "error": error}


def make_plugin_runner(
    *,
    adapter,
    status_widget,
    code_getter,
    ready_text="Donkey ready. Press Run Code.",
    success_text="Done.",
    on_worker_ready=None,
    on_worker_error=None,
    on_run_success=None,
    on_run_error=None,
):
    """
    Return standard `ensure_worker` and `run_code` callables.

    This helper reduces repetitive workflow wiring in user-facing pages.
    """
    flow = DonkeyPluginFlow(adapter=adapter, status_widget=status_widget)

    async def ensure_worker():
        result = await flow.ensure_worker(ready_text=ready_text)
        if result.get("ok"):
            if callable(on_worker_ready):
                on_worker_ready(result)
            return result
        if callable(on_worker_error):
            on_worker_error(result)
        return result

    async def run_code():
        result = await flow.run_code(
            code_getter(),
            success_text=success_text,
        )
        if result.get("ok"):
            if callable(on_run_success):
                on_run_success(result)
            return result
        if callable(on_run_error):
            on_run_error(result)
        return result

    return flow, ensure_worker, run_code


def make_assertion_callbacks(
    *,
    worker_assert_widget,
    run_assert_widget,
    pass_html,
    fail_html,
):
    """Return standard assertion callbacks for plugin runner hooks."""

    def on_worker_ready(_result):
        worker_assert_widget.html = pass_html("Donkey worker started.")

    def on_worker_error(result):
        error = result.get("error", "Unknown error.")
        worker_assert_widget.html = fail_html(
            f"Donkey worker failed to start: {error}"
        )

    def on_run_success(_result):
        run_assert_widget.html = pass_html("Code run succeeded.")

    def on_run_error(result):
        error = result.get("error", "Unknown error.")
        run_assert_widget.html = fail_html(f"Code run failed: {error}")

    return {
        "on_worker_ready": on_worker_ready,
        "on_worker_error": on_worker_error,
        "on_run_success": on_run_success,
        "on_run_error": on_run_error,
    }
