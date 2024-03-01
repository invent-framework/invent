"""Functions to export an Invent app in a variety of formats.

Where "variety" currently means "as python code" :)

"""


def as_python_code(app):
    """ Generate the *textual* Python code for the app."""

    chunks = []
    for page in app.content:
        chunks.append(_pretty_repr(page))

    return chunks


# Internal #############################################################################


def _pretty_repr(component):
    """Generate a pretty repr of a component (the code to construct it)."""

    return "\n".join(_pretty_repr_lines(component))


def _pretty_repr_lines(component, lines=None, indent=""):
    """Generate a pretty repr as a LIST of lines of code.

    Creating it line-by-line makes it easier to format it nicely (with commas only
    where necessary etc. :) ). Maybe we should just use a formatter :)

    """

    lines = lines or []

    component_properties = type(component).properties()
    component_is_container = "content" in component_properties

    if component_is_container:
        content_from_datastore = getattr(component, "_content_from_datastore", None)

    #### The component class e.g. "Page("
    lines.append(f"{indent}{type(component).__name__}(")

    indent += "    "

    #### The component's properties (other than it's content if it is a container.
    for i, (property_name, property_obj) in enumerate(component_properties.items()):
        # Put the content last in the list of properties...
        if property_name == "content":
            continue

        from_datastore = getattr(component, property_obj.private_name + "_from_datastore", None)
        if from_datastore:
            line = f"{indent}{property_name}=from_datastore('{from_datastore.key}'"
            if from_datastore.via_function:
                line += f", via_function={from_datastore.via_function.__name__}"
            line += ")"

        else:
            line = f"{indent}{property_name}={repr(getattr(component, property_name))}"

        if i < len(component_properties) + 1:
            line += ", "

        lines.append(line)

    if component_is_container:
        if not content_from_datastore:
            lines.append(f"{indent}content=[")

            for child in component.content:
                _pretty_repr_lines(child, lines, indent+"    ")
                #if child is not component.content[-1]:
                lines[-1] += ", "

            lines.append(f"{indent}]")

        else:
            line = f"{indent}content=from_datastore('{content_from_datastore.key}'"
            if content_from_datastore.via_function:
                line += f", via_function={content_from_datastore.via_function.__name__}"
            line += ")"
            lines.append(line)

    indent = indent[:-4]
    lines.append(f"{indent})")

    return lines
