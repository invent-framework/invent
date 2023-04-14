"""
The simplest possible app. It says, "Hello, World!".
"""
from pypercard import App, Card

temp_app = App(
    name="Temperature conversion tool.",
    cards=[Card("input_card"), Card("result_card"), Card("error_card")],
)


@temp_app.transition("input_card", "click", "to_c")
def to_c(app, card):
    try:
        temp = float(card.get_by_id("temperature").value)
        app.datastore["result"] = str(round((temp - 32) * (5 / 9), 2)) + "°c"
        return "result_card"
    except Exception:
        return "error_card"


@temp_app.transition("input_card", "click", "to_f")
def to_f(app, card):
    try:
        temp = float(card.get_by_id("temperature").value)
        app.datastore["result"] = str(round((temp * (9 / 5)) + 32, 2)) + "°f"
        return "result_card"
    except Exception:
        return "error_card"


@temp_app.transition("result_card", "click", "again")
def again(app, card):
    return "input_card"


@temp_app.transition("error_card", "click", "reset")
def reset(app, card):
    return "input_card"


temp_app.start("input_card")
