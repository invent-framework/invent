"""
Create a JSON representation of all the widgets defined in the
invent.ui.widgets namespace.
"""

import sys
import json
from unittest import mock

# Mock away the "pyscript" module.
sys.modules["pyscript"] = mock.MagicMock()

from invent.ui import _COMPONENTS


def get_widgets():
    """
    Get all the components from the UI layer, and turn them into
    JSON serializable dicts.
    """
    result = {}
    for component in _COMPONENTS:
        result[component.__name__] = component.as_dict()
    return result


if __name__ == "__main__":
    if sys.version_info < (3, 11):
        print("Need Python > 3.11")
    else:
        widgets = get_widgets()
        with open("widgets.json", "w") as f:
            json.dump(widgets, f, indent=2)
        print("Done")
