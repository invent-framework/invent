"""
A Python terminal widget for the Invent framework.

This is a lightweight shim around PyScript's built-in terminal capabilities.

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

from invent.i18n import _
from pyscript.web import script, page
from invent.ui.core import Widget, TextProperty

_INTERPRETERS = {"py", "mpy"}


class Terminal(Widget):
    """
    A terminal widget for executing Python code and displaying output.
    """

    evaluate = TextProperty(
        _("Dynamically evaluated Python code to execute in the terminal."),
        default_value=None,
    )

    @classmethod
    def icon(cls):
        return '<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256"><path d="M128,128a8,8,0,0,1-3,6.25l-40,32a8,8,0,1,1-10-12.5L107.19,128,75,102.25a8,8,0,1,1,10-12.5l40,32A8,8,0,0,1,128,128Zm48,24H136a8,8,0,0,0,0,16h40a8,8,0,0,0,0-16Zm56-96V200a16,16,0,0,1-16,16H40a16,16,0,0,1-16-16V56A16,16,0,0,1,40,40H216A16,16,0,0,1,232,56ZM216,200V56H40V200H216Z"></path></svg>'  # noqa

    def __init__(self, **kwargs):
        """
        Initialize the Terminal widget.

        The following keyword arguments are supported in addition to the
        standard Widget properties:

        * `src` (str, optional): An optional path to a Python script to
          execute in the terminal. If provided, the script will be executed
          once when the widget is initialized.
        * `worker` (bool, optional): A flag to indicate whether the terminal
          should run in a Web Worker. Defaults to True. If False, the terminal
          will run in the main thread, which may cause UI blocking for
          long-running code.
        * `interpreter` (str, optional): The Python interpreter to use for
          executing code in the terminal. Valid options are "py" for the
          Pyodide (CPython) interpreter and "mpy" for MicroPython. Defaults to
          "py".
        """
        self._init_code = kwargs.pop("code", None)
        self._src_path = kwargs.pop("src", None)
        if self._src_path and self._init_code:
            raise ValueError(
                "Cannot specify both 'code' and 'src' for Terminal widget."
            )
        self._worker_flag = kwargs.pop("worker", True)
        self._interpreter = kwargs.pop("interpreter", "py")
        if self._interpreter not in _INTERPRETERS:
            raise ValueError(
                f"Invalid interpreter '{self._interpreter}'. Valid options are: {_INTERPRETERS}"
            )
        super().__init__(**kwargs)

    def on_evaluate_changed(self):
        """
        Send the new value of the evaluate property to the Python interpreter
        associated with this terminal widget.
        """
        term = page.find(f"{self.id}")
        if term:
            term._dom_element.process(self.evaluate)

    def render(self):
        """
        Emit a properly configured script tag to set up the terminal widget
        in the DOM.
        """
        element = script()
        element.setAttribute("type", self._interpreter)
        element.setAttribute("terminal", "")
        if self._worker_flag:
            element.setAttribute("worker", "")
        if self._src_path:
            element.setAttribute("src", self._src_path)
        if self._init_code:
            element.innerHTML = self._init_code
        return element
