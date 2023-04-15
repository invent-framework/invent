"""
Cowculator 🐮🧮

Very very simple implementation.

Notice how the transition never returns a next-card string. When this happens
the current card remains visible, and only state has changed.
"""
from pypercard import App, DataStore

ds = DataStore()
ds["calculation"] = []  # Holds the calculation specification.

calc_app = App(datastore=ds)
calc_app.start()


# A set of valid arithmetic operations.
OPERANDS = {"%", "/", "*", "-", "+"}


@calc_app.transition("*", "click", query="button")
def handle_button(app, card, click_event):
    """
    Recipe: get the display, the value of the button and a flag to discern if
    the button is for a digit. Then handle each sort of button press.

    The calculation is appended to the "calculation" list in the app's
    datastore.

    When "=" is clicked, the calculation is evaluated by Python.

    Various state related checks happend to make sure the calculation is
    always valid Python and/or the display is always showing something
    sensible.
    """
    # Get the display element in the card.
    display = card.get_by_id("display")
    # Get the value associated with the button that's been clicked.
    val = click_event.target.value
    # Flag if the button also has a "digit" class (it's a valid digit).
    is_digit = "digit" in click_event.target.classList
    # Now handle the different situations caused by a button click.
    if is_digit:
        # The button represents "." or a digit (e.g. "8").
        if val == "." and "." in display.value:
            # Don't append a decimal point if one already exists.
            return
        elif display.value in OPERANDS:
            # Clear the display after having clicked an operand.
            display.value = ""
        # Just add the digit to the display.
        display.value += val
    elif val == "plus-minus" and display.value:
        # If the value in the display is a number, toggle between a positive
        # or negative number.
        if display.value not in OPERANDS:
            if display.value.startswith("-"):
                display.value = display.value[1:]
            else:
                display.value = "-" + display.value
    elif val == "cancel":
        # Cancel means reset everything to a clean state.
        display.value = ""
        app.datastore["calculation"] = []
    elif val == "=":
        # Use the calculation list to create a fragment of valid Python code
        # from which to evaluate the answer.
        calculation = app.datastore["calculation"]
        if display.value in OPERANDS:
            # Cannot get a result with a dangling operand.
            return
        calculation.append(display.value)
        to_eval = "".join(calculation)
        if to_eval.strip():
            # Evaluate the calculation then reset the calculation to empty,
            # in order to start again.
            display.value = str(eval(to_eval))
            app.datastore["calculation"] = []
    elif val in OPERANDS and display.value:
        # Handle operands in valid cases (there should be a number in the
        # display, upon which to operate) and update the calculation list.
        if display.value in OPERANDS:
            # Cannot have adjacent operands.
            return
        calculation = app.datastore["calculation"]
        calculation.append(display.value)
        calculation.append(val)
        display.value = val
        app.datastore["calculation"] = calculation
