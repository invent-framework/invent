from pypercard import Inputs, Card, CardApp


def get_name(data_store, form_value):
    """
    Gets the name of the user from the form field and stores it in the
    data_store. If no name is given, causes an error to be displayed.
    """
    if form_value:
        data_store["name"] = form_value
        return "hello"
    else:
        return "error"


stack = [
    Card(
        "get_value",
        form=Inputs.TEXTBOX,
        text="What is your name..?",
        buttons=[
            {"label": "OK", "target": get_name}  # Use the function!
        ]
    ),
    Card(
        "hello",
        text="Hello {name}!",
        buttons=[
            {"label": "OK", "target": "get_value"}
        ]
    ),
    Card(
        "error",
        text="ERROR\n\nPlease enter a name!",
        text_color="white",
        background="red",
        auto_advance=3,
        auto_target="get_value"
    ),
]

app = CardApp(stack=stack)
app.run()
