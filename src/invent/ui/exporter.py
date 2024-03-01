"""Functions to export an Invent app in a variety of formats.

Where "variety" currently means "as python code" :)

"""

DATASTORE = """
# Datastore ############################################################################


invent.datastore.setdefault("number_of_honks", 0)
invent.datastore.setdefault("number_of_oinks", 0)
"""


BLOCKS = """
# Code #################################################################################


def make_honk(message):
    invent.datastore["number_of_honks"] = (
        invent.datastore["number_of_honks"] + 1
    )
    invent.play_sound(invent.media.sounds.honk.mp3)


def make_oink(message):
    invent.datastore["number_of_oinks"] = (
        invent.datastore["number_of_oinks"] + 1
    )
    invent.play_sound(invent.media.sounds.oink.mp3)


def move_page(message):
    if message.button == "to_goose":
        invent.show_page("Honk")
    elif message.button == "to_pig":
        invent.show_page("Oink")


def make_geese(value_from_datastore):
    return [
        invent.ui.TextBox(text="🪿")

        for _ in range(value_from_datastore)
    ]


def make_pigs(value_from_datastore):
    return [
        invent.ui.TextBox(text="🐖")

        for _ in range(value_from_datastore)
    ]


# Channels #############################################################################


invent.subscribe(make_honk, to_channel="honk", when_subject=["press", "touch"])
invent.subscribe(make_oink, to_channel="oink", when_subject=["press", "touch"])
invent.subscribe(
    move_page,
    to_channel="navigate",
    when_subject=[
        "press",
    ],
)


# User Interface #######################################################################

"""

########################################################################################

APP_TEMPLATE = """
import invent
from invent.ui import *

{datastore}
{blocks}
{ui}
"""

def as_python_code(app):
    """ Generate the *textual* Python code for the app."""

    lines = []

    # The first line of the component's constructor ####################################
    lines.append("App(")

    indent = "    "
    lines.append(f'{indent}name="{app.name}",')
    lines.append(f"{indent}content=[")

    for page in app.content:
        _pretty_repr_lines(page, lines, indent+"    ")

    lines.append(f"{indent}],")

    # The last line of the component's constructor e.g.")" :) ##########################

    lines.append(")")

    ui = "\n".join(lines)

    return APP_TEMPLATE.format(
        datastore=DATASTORE,
        blocks=BLOCKS,
        ui=ui
    )


# Internal #############################################################################


def _pretty_repr_lines(component, lines=None, indent=""):
    """Generate a pretty repr as a LIST of lines of code.

    Creating it line-by-line makes it easier to format it nicely (with commas only
    where necessary etc. :) ). Maybe we should just use a formatter :)

    """

    lines = lines or []

    # The first line of the component's constructor ####################################
    #
    # e.g. "Page("

    lines.append(f"{indent}{type(component).__name__}(")

    # The component's properties EXCEPT its content - we put that last #################

    indent += "    "

    component_properties = type(component).properties()
    for i, (property_name, property_obj) in enumerate(component_properties.items()):
        # Put the content last in the list of properties...
        if property_name == "content":
            continue

        from_datastore = getattr(
            component, property_obj.private_name + "_from_datastore", None
        )
        if from_datastore:
            line = _from_datastore_line(indent, from_datastore, property_name)

        else:
            line = f"{indent}{property_name}={repr(getattr(component, property_name))},"

        lines.append(line)

    # The component's CONTENT property (for Containers only) ###########################

    if "content" in component_properties:
        from_datastore = getattr(component, "_content_from_datastore", None)
        if from_datastore:
            lines.append(_from_datastore_line(indent, from_datastore, "content"))

        else:
            lines.append(f"{indent}content=[")

            for child in component.content:
                _pretty_repr_lines(child, lines, indent+"    ")

            lines.append(f"{indent}],")

    # The last line of the component's constructor e.g.")" :) ##########################

    lines.append(f"{indent[4:]}),")

    return lines


def _from_datastore_line(indent, from_datastore, property_name):
    """Create a line for a property that gets its value from the datastore."""

    line = f"{indent}{property_name}=from_datastore('{from_datastore.key}'"
    if from_datastore.via_function:
        line += f", via_function={from_datastore.via_function.__name__}"
    line += "),"

    return line
