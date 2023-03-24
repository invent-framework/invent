A Complete Application
----------------------

The "hello world" of GUI applications is a temperature conversion tool:

* Type a number.
* Select to convert the value to celsius or farenheit.
* If the user doesn't provide a valid number, show an error message.

Here's how to do it with PyperCard::

    from pypercard import Inputs, Card, CardApp


    def to_c(data_store, form_value):
        try:
            val = float(form_value)
            data_store["result"] = (val - 32) * 5.0 / 9.0
            return "Result"
        except Exception:
            return "Error"


    def to_f(data_store, form_value):
        try:
            val = float(form_value)
            data_store["result"] = 9.0 / 5.0 * val + 32
            return "Result"
        except Exception:
            return "Error"


    stack = [
        Card(
            "GetValue",
            form=Inputs.TEXTBOX,
            text="Enter a number to convert...",
            buttons=[
                {"label": "Convert to Celsius", "target": to_c},
                {"label": "Convert to Farenheit", "target": to_f},
            ],
        ),
        Card(
            "Error",
            text="[b]ERROR[/b]\n\nPlease enter a number.",
            text_color="white",
            background="red",
            auto_advance=3,
            auto_target="GetValue",
        ),
        Card(
            "Result",
            text="{result:.2f}",
            text_size=98,
            buttons=[{"label": "Ok", "target": "GetValue"}],
        ),
    ]


    app = CardApp("Temperature Converter", stack=stack)
    app.run()

It should look like this:

.. image:: temperature.gif


Back to :doc:`tutorial4`. Continue to :doc:`tutorial6`.
