"""
A mysterious Myst like game to demonstrate some of the more creative uses of
PyperCard.
"""
from pypercard import App
import random


app = App()

if "open" not in app.datastore:
    app.datastore.update(
        {
            # Default game state flags.
            "open": False,
            "inscription": False,
            "encounter": False,
            "locked": True,
            "red_book": False,
            "instructions": False,
            "name": "Pilgrim",
        }.items()
    )


@app.transition("hello", "click", "submit")
def hello(app, card):
    name = card.get_by_id("name").value.strip()
    if name:
        app.datastore["name"] = name
        return "intro1"
    return "nameerror"


@app.transition("landed", "click", "continue")
def to_patio_landing(app, card):
    return which_patio(app, card)


@app.transition("beach", "click", "right")
def to_patio_landing(app, card):
    return which_patio(app, card)


def which_patio(app, card):
    if app.datastore["open"]:
        return "patio_open"
    return "patio_closed"


@app.transition("patio_closed", "click", "to_front_door")
def to_front_door(app, card):
    return which_front_door(app, card)


@app.transition("patio_open", "click", "to_front_door")
def to_front_door(app, card):
    return which_front_door(app, card)


@app.transition("stone", "click", "to_front_door")
def to_front_door(app, card):
    return which_front_door(app, card)


@app.transition("lake_reeds", "click", "to_front_door")
def to_front_door(app, card):
    return which_front_door(app, card)


@app.transition("undergrowth", "click", "to_front_door")
def to_front_door(app, card):
    return which_front_door(app, card)


@app.transition("front_courtyard", "click", "to_front_door")
def to_front_door(app, card):
    return which_front_door(app, card)


def which_front_door(app, card):
    if app.datastore["open"]:
        return "front_door_open"
    else:
        return "front_door_closed"


@app.transition("back_garden", "click", "to_back_door")
def to_back_door(app, card):
    if app.datastore["open"]:
        return "back_door_open"
    else:
        return "back_door_closed"


@app.transition("stone", "click", "to_inscription")
def to_inscription(app, card):
    if app.datastore["inscription"]:
        return "inscription2b"
    else:
        app.datastore["inscription"] = True
        return "inscription1"


@app.transition("woods", "click", "to_encounter")
def to_encounter(app, card):
    if app.datastore["encounter"]:
        if app.datastore["open"]:
            return "forest_path"
        else:
            return "interview"
    else:
        app.datastore["encounter"] = True
        return "encounter1"


@app.transition("interview", "click", "to_answer")
def to_answer(app, card):
    wrong = [
        "interview_no1",
        "interview_no2",
        "interview_no3",
        "interview_no4",
        "interview_no5",
    ]
    answer = card.get_by_id("answer").value.strip()
    if answer:
        if answer == "telesphoros":
            app.datastore["open"] = True
            return "interview_end"
        else:
            return random.choice(wrong)
    else:
        return random.choice(wrong)


@app.transition("window_view", "click", "to_red_book")
def to_red_book(app, card):
    if app.datastore["red_book"]:
        if app.datastore["locked"]:
            return "book_lock"
        else:
            return "red_book"
    else:
        app.datastore["red_book"] = True
        return "unlock1"


@app.transition("book_lock", "click", "to_unlock")
def to_unlock(app, card):
    app.datastore["message"] = "You must enter a four digit number."
    answer = card.get_by_id("answer").value.strip()
    if answer:
        try:
            code = int(answer)
            if code < 10000 and code >= 0:
                if code == 1943:
                    app.datastore["locked"] = False
                    return "red1"
                else:
                    app.datastore["message"] = "Wrong combination, try again."
            else:
                app.datastore[
                    "message"
                ] = "The number should be between 0000 and 9999."
        except Exception:
            app.datastore["message"] = "Please enter four valid digits."
    return "locked"


@app.transition("large_tower_door", "click", "to_dining_room")
def to_dining_room(app, card):
    if not app.datastore["locked"]:
        return "finale"
    if app.datastore["instructions"]:
        return "waiting"
    app.datastore["instructions"] = True
    return "instruct"


app.start()
