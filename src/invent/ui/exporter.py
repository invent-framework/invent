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

    #### e.g. "Page("
    line = f"{indent}{type(component).__name__}("

    component_properties = type(component).properties()
    component_is_container = "content" in component_properties

    if component_is_container:
        content_from_datastore = getattr(component, "_content_from_datastore", None)

    for i, (property_name, property_obj) in enumerate(component_properties.items()):
        if property_name == "content" and not content_from_datastore:
            continue

        if property_name in ["id", "name"] and not property_obj:
            continue

        # if type(value) is str and not value:
        #     continue

        from_datastore = getattr(component, property_obj.private_name + "_from_datastore", None)
        if from_datastore:
            line += f"{property_name}=from_datastore('{from_datastore.key}'"
            if from_datastore.via_function:
                line += f", via_function={from_datastore.via_function.__name__}"
            line += ")"

        else:
            line += f"{property_name}={repr(getattr(component, property_name))}"

        if i < len(component_properties) + 1:
            line += ", "

    if component_is_container and not content_from_datastore:
        line += "content=["
        lines.append(line)

        for child in component.content:
            _pretty_repr_lines(child, lines, indent+"    ")
            if child is not component.content[-1]:
                lines[-1] += ", "

        lines.append("])")

    else:
        line = line + ")"
        lines.append(line)

    return lines
