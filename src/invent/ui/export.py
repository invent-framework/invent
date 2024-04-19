"""Functions to export an Invent app in a variety of formats.

Where "variety" currently means "as python code" :)

"""

from invent.ui import Container


# TODO: This will be passed in from the builder :)
IMPORTS = """
import invent
from invent.ui import *
from invent.ai import *
"""


# Contents/templates for index.html, main.py and pyscript.toml files ##########


INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{title}</title>

    <!-- Recommended meta tags -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">

    <!-- PyScript -->
    <link rel="stylesheet" href="https://pyscript.net/releases/2024.4.1/core.css">
    <script type="module" src="https://pyscript.net/releases/2024.4.1/core.js"></script>

    <!-- App CSS Styles -->
    <link rel="stylesheet" href="https://unpkg.com/papercss@1.9.2/dist/paper.min.css">
</head>
<body>
  <script type="py" src="./main.py" config="./pyscript.toml" async></script>
</body>
</html>
"""


MAIN_PY_TEMPLATE = """
{imports}

# Datastore ##################################################################

{datastore}

# Code #######################################################################

{code}

# User Interface #############################################################

{app}

# GO! ########################################################################

invent.go()

"""


PYSCRIPT_TOML_TEMPLATE = """
packages = [ "pyodide_http", "requests" ]
experimental_create_proxy = "auto"
[files]
#
# invent
#
"{{INVENT}}" = "{invent_src}"
"{{INVENT_TO}}" = "./invent"
"{{INVENT}}/__init__.py"="{{INVENT_TO}}/__init__.py"
"{{INVENT}}/__about__.py"="{{INVENT_TO}}/__about__.py"
"{{INVENT}}/ai.py"="{{INVENT_TO}}/ai.py"
"{{INVENT}}/channels.py"="{{INVENT_TO}}/channels.py"
"{{INVENT}}/compatability.py"="{{INVENT_TO}}/compatability.py"
"{{INVENT}}/datastore.py"="{{INVENT_TO}}/datastore.py"
"{{INVENT}}/i18n.py"="{{INVENT_TO}}/i18n.py"
"{{INVENT}}/media.py"="{{INVENT_TO}}/media.py"
"{{INVENT}}/speech.py"="{{INVENT_TO}}/speech.py"
"{{INVENT}}/utils.py"="{{INVENT_TO}}/utils.py"
#
# invent.ui
#
"{{INVENT}}/ui/__init__.py"="{{INVENT_TO}}/ui/__init__.py"
"{{INVENT}}/ui/app.py"="{{INVENT_TO}}/ui/app.py"
"{{INVENT}}/ui/core.py"="{{INVENT_TO}}/ui/core.py"
"{{INVENT}}/ui/export.py"="{{INVENT_TO}}/ui/export.py"
"{{INVENT}}/ui/page.py"="{{INVENT_TO}}/ui/page.py"
"{{INVENT}}/ui/utils.py"="{{INVENT_TO}}/ui/utils.py"
"{{INVENT}}/ui/widgets/__init__.py"="{{INVENT_TO}}/ui/widgets/__init__.py"
"{{INVENT}}/ui/widgets/audio.py"="{{INVENT_TO}}/ui/widgets/audio.py"
"{{INVENT}}/ui/widgets/button.py"="{{INVENT_TO}}/ui/widgets/button.py"
"{{INVENT}}/ui/widgets/checkbox.py"="{{INVENT_TO}}/ui/widgets/checkbox.py"
"{{INVENT}}/ui/widgets/code.py"="{{INVENT_TO}}/ui/widgets/code.py"
"{{INVENT}}/ui/widgets/html.py"="{{INVENT_TO}}/ui/widgets/html.py"
"{{INVENT}}/ui/widgets/image.py"="{{INVENT_TO}}/ui/widgets/image.py"
"{{INVENT}}/ui/widgets/slider.py"="{{INVENT_TO}}/ui/widgets/slider.py"
"{{INVENT}}/ui/widgets/switch.py"="{{INVENT_TO}}/ui/widgets/switch.py"
"{{INVENT}}/ui/widgets/textbox.py"="{{INVENT_TO}}/ui/widgets/textbox.py"
"{{INVENT}}/ui/widgets/textinput.py"="{{INVENT_TO}}/ui/widgets/textinput.py"
"{{INVENT}}/ui/widgets/fileupload.py"="{{INVENT_TO}}/ui/widgets/fileupload.py"
"""


def as_pyscript_app(app, imports=IMPORTS, datastore="", code="", to_psdc=True):
    """Generate the index.html, main.py and pyscript.toml files for an app."""

    # index.html
    index_html = INDEX_HTML.format(
        title=app.name
    )

    # main.py
    main_py = MAIN_PY_TEMPLATE.format(
        imports=imports,
        datastore=datastore,
        code=code,
        app=_pretty_repr_app(app),
    )

    # pyscript.toml
    pyscript_toml = PYSCRIPT_TOML_TEMPLATE.format(
        invent_src=(
            "https://mchilvers.pyscriptapps.com/invent/latest/invent"
            if to_psdc
            else "../../src/invent"
        )
    )

    return index_html, main_py, pyscript_toml


def as_dict(app, imports=IMPORTS, datastore="", code="", to_psdc=True):
    """Export an app as a dictionary."""

    return dict(
        imports={},
        datastore={},
        blocks={},
        app=app.as_dict()
    )


def from_dict(bundle_dict):
    """Rehydrate an app from the dictionary representation."""

    app = _app_from_dict(bundle_dict["app"])

    return app


def _app_from_dict(app_dict):
    """Create an App from the specified dictionary representation."""

    from invent.ui.app import App

    content = [
        _component_from_dict(component_dict) for component_dict in app_dict["content"]
    ]

    app_dict["content"] = content

    return App(**app_dict)


def _component_from_dict(component_dict):
    """Create a component from the specified dictionary representation."""

    from invent import ui

    cls = getattr(ui, component_dict["type"])

    if issubclass(cls, Container):
        content = [
            _component_from_dict(component_dict)

            for component_dict in component_dict["properties"]["content"]
        ]

    else:
        content = None

    component_dict["properties"]["content"] = content

    return cls(**component_dict["properties"])


# Internal ###################################################################


# The {pages} indentation looks weird in this template, but the actual
# indentation is handled in the pretty repr functions :)
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

    Creating it line-by-line makes it easier to format it nicely (with commas
    only where necessary etc. :) ). Maybe we should just use a formatter :)

    """

    # The first line of the component's constructor e.g. "Page(".
    lines.append(f"{indent}{type(component).__name__}(")

    # The component's properties.
    _pretty_repr_component_properties(component, lines, indent + "    ")

    # If the component is a Container, its "content" property.
    if isinstance(component, Container):
        _pretty_repr_container_content_property(
            component, lines, indent + "    "
        )

    # The last line of the component's constructor e.g.")" :).
    lines.append(f"{indent}),")

    return lines


def _pretty_repr_component_properties(component, lines, indent):
    """Generate a pretty repr of a Component's properties."""

    for property_name, property_obj in type(component).properties().items():
        # If the component is a Container, we deal with its content separately
        # (for the recursive case). A Widget may well define its own custom
        # "content" property though, so we handle that just like any other
        # property.
        if isinstance(component, Container) and property_name == "content":
            continue

        from_datastore = _get_from_datastore(component, property_name)
        property_value = (
            from_datastore
            if from_datastore
            else getattr(component, property_name)
        )

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
    """
    Return the "from_datastore" instance for a property or None if it is a
    simple/literal property.
    """

    return getattr(component, f"_{property_name}_from_datastore", None)
