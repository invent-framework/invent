"""Functions to export an Invent app in a variety of formats.

Where "variety" currently means "as python code" :)

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

    return "\n".join(lines)


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
