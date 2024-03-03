"""Functions to export an Invent app in a variety of formats.

Where "variety" currently means "as python code" :)

"""

from invent.ui import Container


# TODO: This will be passed in from the builder :)
IMPORTS = """
import invent
from invent.ui import *
"""


# TODO: This will be passed in from the builder :)
DATASTORE = """
invent.datastore.setdefault("number_of_honks", 0)
invent.datastore.setdefault("number_of_oinks", 0)
"""


# TODO: This will be passed in from the builder :)
CODE = """
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


invent.subscribe(make_honk, to_channel="honk", when_subject=["press", "touch"])
invent.subscribe(make_oink, to_channel="oink", when_subject=["press", "touch"])
invent.subscribe(
    move_page,
    to_channel="navigate",
    when_subject=[
        "press",
    ],
)
"""


# Contents/templates for index.html, main.py and pyscript.toml files ###################


INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Invent</title>

    <!-- Recommended meta tags -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">

    <!-- PyScript -->
    <link rel="stylesheet" href="https://pyscript.net/releases/2024.1.1/core.css">
    <script type="module" src="https://pyscript.net/releases/2024.1.1/core.js"></script>

    <!-- App CSS Styles -->
    <link rel="stylesheet" href="https://unpkg.com/papercss@1.9.2/dist/paper.min.css">
</head>
<body>
  <script type="mpy" src="./main.py" config="./pyscript.toml"></script>
</body>
</html>
"""


MAIN_PY_TEMPLATE = """
{imports}

# Datastore ############################################################################

{datastore}

# Code #################################################################################

{code}

# User Interface #######################################################################

{app}

# GO! ##################################################################################

invent.go()

"""


PYSCRIPT_TOML_TEMPLATE = """
[files]
#
# Invent.
#
"{{INVENT}}" = "{invent_src}"
"{{INVENT_TO}}" = "./invent"
"{{INVENT}}/__init__.py"="{{INVENT_TO}}/__init__.py"
"{{INVENT}}/__about__.py"="{{INVENT_TO}}/__about__.py"
"{{INVENT}}/channels.py"="{{INVENT_TO}}/channels.py"
"{{INVENT}}/datastore.py"="{{INVENT_TO}}/datastore.py"
"{{INVENT}}/i18n.py"="{{INVENT_TO}}/i18n.py"
"{{INVENT}}/media.py"="{{INVENT_TO}}/media.py"
"{{INVENT}}/utils.py"="{{INVENT_TO}}/utils.py"
"{{INVENT}}/ui/__init__.py"="{{INVENT_TO}}/ui/__init__.py"
"{{INVENT}}/ui/app.py"="{{INVENT_TO}}/ui/app.py"
"{{INVENT}}/ui/core.py"="{{INVENT_TO}}/ui/core.py"
"{{INVENT}}/ui/export.py"="{{INVENT_TO}}/ui/export.py"
"{{INVENT}}/ui/page.py"="{{INVENT_TO}}/ui/page.py"
"{{INVENT}}/ui/utils.py"="{{INVENT_TO}}/ui/utils.py"
"{{INVENT}}/ui/widgets/__init__.py"="{{INVENT_TO}}/ui/widgets/__init__.py"
"{{INVENT}}/ui/widgets/button.py"="{{INVENT_TO}}/ui/widgets/button.py"
"{{INVENT}}/ui/widgets/code.py"="{{INVENT_TO}}/ui/widgets/code.py"
"{{INVENT}}/ui/widgets/image.py"="{{INVENT_TO}}/ui/widgets/image.py"
"{{INVENT}}/ui/widgets/textbox.py"="{{INVENT_TO}}/ui/widgets/textbox.py"
"{{INVENT}}/ui/widgets/textinput.py"="{{INVENT_TO}}/ui/widgets/textinput.py"
"""


def as_pyscript_app(app, imports=IMPORTS, datastore=DATASTORE, code=CODE, to_psdc=True):
    """Generate the index.html, main.py and pyscript.toml files for an app."""

    # index.html
    index_html = INDEX_HTML

    # main.py
    main_py = MAIN_PY_TEMPLATE.format(
        imports=imports, datastore=datastore, code=code, app=_pretty_repr_app(app)
    )

    # pyscript.toml
    pyscript_toml = PYSCRIPT_TOML_TEMPLATE.format(
        invent_src="https://mchilvers.pyscriptapps.com/invent/latest/invent" if to_psdc else "../../src/invent"
    )

    return index_html, main_py, pyscript_toml


# Internal #############################################################################


# The {pages} indentation looks weird in this template, but the actual indentation is
# handled in the pretty repr functions :)
APP_TEMPLATE = """
App(
    name='{name}',
    content=[
{pages}
    ],
)
"""


def _pretty_repr_app(app):
    """Generate a pretty repr of the App's UI."""

    return APP_TEMPLATE.format(
        name=app.name, pages=_pretty_repr_pages(app.content)
    )


def _pretty_repr_pages(pages):
    """Generate a pretty repr of the pages in an App."""

    lines = []
    for page in pages:
        _pretty_repr_component(page, lines=lines, indent=" " * 8)

    return "\n".join(lines)


def _pretty_repr_component(component, lines, indent=""):
    """Generate a pretty repr of a Component.

    Creating it line-by-line makes it easier to format it nicely (with commas only
    where necessary etc. :) ). Maybe we should just use a formatter :)

    """

    # The first line of the component's constructor e.g. "Page(".
    lines.append(f"{indent}{type(component).__name__}(")

    # The component's properties.
    _pretty_repr_component_properties(component, lines, indent+"    ")

    # If the component is a Container, its "content" property.
    if isinstance(component, Container):
        _pretty_repr_container_content_property(component, lines, indent+"    ")

    # The last line of the component's constructor e.g.")" :).
    lines.append(f"{indent}),")

    return lines


def _pretty_repr_component_properties(component, lines, indent):
    """Generate a pretty repr of a Component's properties."""

    for property_name, property_obj in type(component).properties().items():
        # If the component is a Container, we deal with its content separately (for the
        # recursive case). A Widget may well define its own custom "content" property
        # though, so we handle that just like any other property.
        if isinstance(component, Container) and property_name == "content":
            continue

        from_datastore = _get_from_datastore(component, property_name)
        property_value = from_datastore if from_datastore else getattr(component, property_name)

        lines.append(f"{indent}{property_name}={repr(property_value)},")


def _pretty_repr_container_content_property(component, lines, indent):
    """
    Generate a pretty repr of a Container's "content" property.
    """

    from_datastore = _get_from_datastore(component, "content")
    if from_datastore:
        lines.append(f"{indent}content={repr(from_datastore)},")

    else:
        lines.append(f"{indent}content=[")
        for child in component.content:
            _pretty_repr_component(child, lines=lines, indent=indent + "    ")
        lines.append(f"{indent}],")


def _get_from_datastore(component, property_name):
    """Return the "from_datastore" instance for a property or None if it is a simple/literal property."""

    return getattr(component, f"_{property_name}_from_datastore", None)
