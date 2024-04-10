import invent
from invent.ui import *


# Datastore ############################################################################


invent.datastore.update(
    {
        "numbers": "0",
        "value": "",
        "left": 0,  # Decimal(0),
        "right": 0,  # Decimal(0),
        "operator": "+",
    }
)


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

App(
    name="Calculator",
    content=[
        Page(
            children=[
                TextInput(value=from_datastore("numbers")),
                Row(
                    children=[
                        Button(text="AC", purpose="SECONDARY", on_press=to_channel("calculator"), style=Pack(flex=1)),
                        Button(text="C", purpose="SECONDARY", on_press=to_channel("calculator"), style=Pack(flex=1)),
                        Button(text="+/-", purpose="SECONDARY", on_press=to_channel("calculator"), style=Pack(flex=1)),
                        Button(text="÷", purpose="SUCCESS", on_press=to_channel("calculator"), style=Pack(flex=1)),
                    ]
                ),
                Row(
                    children=[
                        Button(text="7", purpose="DEFAULT", on_press=to_channel("calculator"), style=Pack(flex=1)),
                        Button(text="8", purpose="DEFAULT", on_press=to_channel("calculator"), style=Pack(flex=1)),
                        Button(text="9", purpose="DEFAULT", on_press=to_channel("calculator"), style=Pack(flex=1)),
                        Button(text="x", purpose="SUCCESS", on_press=to_channel("calculator"), style=Pack(flex=1)),
                    ]
                ),
                Row(
                    children=[
                        Button(text="4", purpose="DEFAULT", on_press=to_channel("calculator"), style=Pack(flex=1)),
                        Button(text="5", purpose="DEFAULT", on_press=to_channel("calculator"), style=Pack(flex=1)),
                        Button(text="6", purpose="DEFAULT", on_press=to_channel("calculator"), style=Pack(flex=1)),
                        Button(text="-", purpose="SUCCESS", on_press=to_channel("calculator"), style=Pack(flex=1)),
                    ]
                ),
                Row(
                    children=[
                        Button(text="1", purpose="DEFAULT", on_press=to_channel("calculator"), style=Pack(flex=1)),
                        Button(text="2", purpose="DEFAULT", on_press=to_channel("calculator"), style=Pack(flex=1)),
                        Button(text="3", purpose="DEFAULT", on_press=to_channel("calculator"), style=Pack(flex=1)),
                        Button(text="+", purpose="SUCCESS", on_press=to_channel("calculator"), style=Pack(flex=1)),
                    ]
                ),
                Row(
                    children=[
                        Button(text="0", purpose="DEFAULT", on_press=to_channel("calculator"), style=Pack(flex=2)),
                        Button(text=".", purpose="SECONDARY", on_press=to_channel("calculator"), style=Pack(flex=1)),
                        Button(text="=", purpose="SECONDARY", on_press=to_channel("calculator"), style=Pack(flex=1)),
                    ],
                ),
            ]
        )
    ],
)

# GO! ##################################################################################


invent.go()
