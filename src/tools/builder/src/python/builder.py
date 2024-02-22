import time
import invent


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
        Return a dictionary of available widgets in the form:

        {
            "Button": {
                "properties": {
                    "channel": {
                      "property_type": "TextProperty",
                      "description": "The channel[s] to which the widget broadcasts.",
                      "required": false,
                      "default_value": null,
                      "min_length": null,
                      "max_length": null
                    },
                    "id": {
                      "property_type": "TextProperty",
                      "description": "The id of the widget instance in the DOM.",
                      "required": false,
                      "default_value": null,
                      "min_length": null,
                      "max_length": null
                    },
                },
                "message_subjects": [
                    "click", "hold", "double-click"
                ],
                "preview" : "<button>Button</button>"
            },

            ...
        }
        """

        ...

    def get_app(self):
        """Might need this to return the app as a plain ol' dictionary."""

        return self._app.as_dict()

    def get_page(self, page_id_or_index):
        ...

    def add_page(self):
        ...

    def update_page(self, page, **properties_to_update):
        ...

    def delete_page(self, page):
        ...

    def add_widget_to_page(self, page, widget_definition, parent=None):
        # Create widget instance from definition.
        ...

        # Add it to the parent widget (if no parent).
        ...

    def delete_widget_from_page(self, widget_ref):
        ...
