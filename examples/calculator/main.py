import invent
from invent.ui import export


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

    if button.label in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
        data["numbers"] = data["value"] = (
            data["value"].lstrip("0") + button.label
        )

    elif button.label == "+/-":
        data["numbers"] = data["value"] = str(float(data["value"] or "0") * -1)

    elif button.label == "%":
        data["numbers"] = data["value"] = str(
            float(data["value"] or "0") / float(100)
        )

    elif button.label == ".":
        if "." not in data["value"]:
            data["numbers"] = data["value"] = (data["value"] or "0") + "."

    elif button.label == "AC":
        data["value"] = ""
        data["left"] = data["right"] = 0  # Decimal(0)
        data["operator"] = "+"
        data["numbers"] = "0"

    elif button.label == "C":
        data["value"] = ""
        data["numbers"] = "0"

    elif button.label in ("+", "-", "÷", "x"):
        data["right"] = float(
            data["value"] or "0"
        )  # Decimal(data["value"] or "0")
        calculate(data)
        data["operator"] = button.label

    elif button.label == "=":
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

invent.ui.App(
    name="Calculator",
    content=[
        invent.ui.Page(
            content=[
                invent.ui.Grid(
                    columns=4,
                    content=[
                        invent.ui.TextInput(
                            column_span=4,
                            value=invent.ui.from_datastore("numbers"),
                        ),
                        invent.ui.Button(
                            label="AC",
                            purpose="SECONDARY",
                            channel="calculator",
                        ),
                        invent.ui.Button(
                            label="C",
                            purpose="SECONDARY",
                            channel="calculator",
                        ),
                        invent.ui.Button(
                            label="+/-",
                            purpose="SECONDARY",
                            channel="calculator",
                        ),
                        invent.ui.Button(
                            label="÷", purpose="SUCCESS", channel="calculator"
                        ),
                        invent.ui.Button(
                            label="7", purpose="DEFAULT", channel="calculator"
                        ),
                        invent.ui.Button(
                            label="8", purpose="DEFAULT", channel="calculator"
                        ),
                        invent.ui.Button(
                            label="9", purpose="DEFAULT", channel="calculator"
                        ),
                        invent.ui.Button(
                            label="x", purpose="SUCCESS", channel="calculator"
                        ),
                        invent.ui.Button(
                            label="4", purpose="DEFAULT", channel="calculator"
                        ),
                        invent.ui.Button(
                            label="5", purpose="DEFAULT", channel="calculator"
                        ),
                        invent.ui.Button(
                            label="6", purpose="DEFAULT", channel="calculator"
                        ),
                        invent.ui.Button(
                            label="-", purpose="SUCCESS", channel="calculator"
                        ),
                        invent.ui.Button(
                            label="1", purpose="DEFAULT", channel="calculator"
                        ),
                        invent.ui.Button(
                            label="2", purpose="DEFAULT", channel="calculator"
                        ),
                        invent.ui.Button(
                            label="3", purpose="DEFAULT", channel="calculator"
                        ),
                        invent.ui.Button(
                            label="+", purpose="SUCCESS", channel="calculator"
                        ),
                        invent.ui.Button(
                            column_span=2,
                            label="0",
                            purpose="DEFAULT",
                            channel="calculator",
                        ),
                        invent.ui.Button(
                            label=".",
                            purpose="SECONDARY",
                            channel="calculator",
                        ),
                        invent.ui.Button(
                            label="=",
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
