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
