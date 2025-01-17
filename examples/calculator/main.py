import invent
from invent.ui import *


# Datastore ############################################################################


await invent.setup(
    numbers="0", value="", left=0, right=0, operator="+"
)  # Load default values for the datastore.


# Code #################################################################################


def when_any_button_is_clicked(message):
    data = invent.datastore
    button = message.button

    if button.text in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
        data["numbers"] = data["value"] = (
            data["value"].lstrip("0") + button.text
        )

    elif button.text == "+/-":
        data["numbers"] = data["value"] = str(float(data["value"] or "0") * -1)

    elif button.text == "%":
        data["numbers"] = data["value"] = str(
            float(data["value"] or "0") / float(100)
        )

    elif button.text == ".":
        if "." not in data["value"]:
            data["numbers"] = data["value"] = (data["value"] or "0") + "."

    elif button.text == "AC":
        data["value"] = ""
        data["left"] = data["right"] = 0  # Decimal(0)
        data["operator"] = "+"
        data["numbers"] = "0"

    elif button.text == "C":
        data["value"] = ""
        data["numbers"] = "0"

    elif button.text in ("+", "-", "÷", "x"):
        data["right"] = float(
            data["value"] or "0"
        )  # Decimal(data["value"] or "0")
        calculate(data)
        data["operator"] = button.text

    elif button.text == "=":
        if data["value"]:
            data["right"] = float(data["value"])
        calculate(data)


def calculate(data) -> None:
    """Does the calculation: LEFT OPERATOR RIGHT"""

    try:
        if data["operator"] == "+":
            data["left"] += data["right"]

        elif data["operator"] == "-":
            data["left"] -= data["right"]

        elif data["operator"] == "÷":
            data["left"] /= data["right"]

        elif data["operator"] == "x":
            data["left"] *= data["right"]

        data["numbers"] = str(data["left"])
        data["value"] = ""

    except NotImplementedError:
        data["numbers"] = "Error"


# Channels #############################################################################


invent.subscribe(
    when_any_button_is_clicked, to_channel="calculator", when_subject=["press"]
)


# User Interface #######################################################################


invent.App(
    name="Calculator",
    pages=[
        Page(
            children=[
                Grid(
                    columns=4,
                    children=[
                        TextInput(
                            column_span=4,
                            value=from_datastore("numbers"),
                        ),
                        Button(
                            text="AC",
                            purpose="SECONDARY",
                            channel="calculator",
                        ),
                        Button(
                            text="C",
                            purpose="SECONDARY",
                            channel="calculator",
                        ),
                        Button(
                            text="+/-",
                            purpose="SECONDARY",
                            channel="calculator",
                        ),
                        Button(
                            text="÷", purpose="SUCCESS", channel="calculator"
                        ),
                        Button(
                            text="7", purpose="DEFAULT", channel="calculator"
                        ),
                        Button(
                            text="8", purpose="DEFAULT", channel="calculator"
                        ),
                        Button(
                            text="9", purpose="DEFAULT", channel="calculator"
                        ),
                        Button(
                            text="x", purpose="SUCCESS", channel="calculator"
                        ),
                        Button(
                            text="4", purpose="DEFAULT", channel="calculator"
                        ),
                        Button(
                            text="5", purpose="DEFAULT", channel="calculator"
                        ),
                        Button(
                            text="6", purpose="DEFAULT", channel="calculator"
                        ),
                        Button(
                            text="-", purpose="SUCCESS", channel="calculator"
                        ),
                        Button(
                            text="1", purpose="DEFAULT", channel="calculator"
                        ),
                        Button(
                            text="2", purpose="DEFAULT", channel="calculator"
                        ),
                        Button(
                            text="3", purpose="DEFAULT", channel="calculator"
                        ),
                        Button(
                            text="+", purpose="SUCCESS", channel="calculator"
                        ),
                        Button(
                            column_span=2,
                            text="0",
                            purpose="DEFAULT",
                            channel="calculator",
                        ),
                        Button(
                            text=".",
                            purpose="SECONDARY",
                            channel="calculator",
                        ),
                        Button(
                            text="=",
                            purpose="SECONDARY",
                            channel="calculator",
                        ),
                    ],
                ),
            ]
        )
    ],
)


# GO! ##################################################################################


invent.go()
