import time
import invent
import json
from pyscript import document
import random

# Mock Info
pages = {
    "Page1": {
        "name": "Page 1",
        "content": []
    }
}


class Builder:
    def __init__(self):
        self._app = invent.ui.App(
            name="Untitled Cool App",
            content=[
                invent.ui.Page(
                    name="Page 1",
                    content=[]
                )
            ]
        )


    @property
    def app(self):
        return self._app

    def get_available_widgets(self):
        """
        Return a dictionary of available widgets.
        """

        widgets = {
            "Button": {
                "properties": {
                    "channel": {
                      "property_type": "TextProperty",
                      "description": "The channel[s] to which the widget broadcasts.",
                      "required": False,
                      "default_value": None,
                      "min_length": None,
                      "max_length": None
                    },
                    "id": {
                      "property_type": "TextProperty",
                      "description": "The id of the widget instance in the DOM.",
                      "required": False,
                      "default_value": None,
                      "min_length": None,
                      "max_length": None
                    },
                },
                "message_blueprints": [
                    "click", "hold", "double-click"
                ],
                "preview" : "<button>Button</button>"
            }
        }

        return json.dumps(widgets)

    def get_app(self):
        """Might need this to return the app as a plain ol' dictionary."""

        return self._app.as_dict()

    def get_pages(self):
        return json.dumps(pages)

    def add_page(self, page_name):
        page_id = f"Page{len(pages)+1}"

        pages[page_id] = {
            "name": page_name,
            "content": []
        }

    def update_page(self, page, **properties_to_update):
        ...

    def delete_page(self, page):
        ...

    def add_widget_to_page(self, parent=None):
        # Create widget instance from definition.
        button = document.createElement("button")
        button.id = f"button{random.randint(0,100)}"
        button.innerText = "Button"
        target = document.getElementById(parent)
        target.appendChild(button)

        return button.id


    def delete_widget_from_page(self, widget_ref):
        ...

    def get_widget_properties(self, widget_ref):
        """
        Return a dictionary of properties from a widget reference.
        """
        properties = {
            "channel": {
                "property_type": "TextProperty",
                "description": "The channel[s] to which the widget broadcasts.",
                "required": False,
                "value": None,
                "min_length": None,
                "max_length": None
            },
            "label": {
                "property_type": "TextProperty",
                "description": "The text on the button.",
                "required": False,
                "value": "Button",
                "min_length": None,
                "max_length": None
            },
            "name": {
                "property_type": "TextProperty",
                "description": "The meaningful name of the widget instance.",
                "required": False,
                "value": None,
                "min_length": None,
                "max_length": None
            },
            "position": {
                "property_type": "TextProperty",
                "description": "The widget's preferred position.",
                "required": False,
                "value": None,
                "min_length": None,
                "max_length": None
            }
        }

        return json.dumps(properties)
    
    def update_widget_property(self, widget_ref, value):
        ...
