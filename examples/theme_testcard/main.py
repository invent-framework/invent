"""
This app is a simple test card for the theme system. We ensure all the various
UI aspects of the Invent framework are shown in a page, and allow the user to
select different "themes" to see how they affect the appearance of the page.
"""

import invent
from invent.ui import *

# Datastore ############################################################################

await invent.load()  # Load default values for the datastore.

# Code #################################################################################

# User Interface #######################################################################

app = invent.App(
    name="Theme Testcard",
    content=[
        Page(
            name="Testcard",
            content=[
                Column(
                    content=[
                        Row(
                            content=[
                                Label(text="# Invent Test Card"),
                                Image(
                                    image=invent.media.images.invent_logo.png,
                                    width="64px",
                                ),
                            ]
                        ),
                        Label(text="## Textual styling"),
                        Label(
                            text="""This is a paragraph of text. I can have **strong** and *emphasised* text, as well as [links](https://inventframework.org/) to elsewhere. 
                            
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. 
                            
That should be long enough to wrap around to the next line.

Here's some code:"""
                        ),
                        Code(
                            code="""def hello(name="world"):
    return f"Hello, {name}"
                             """
                        ),
                        Label(
                            text="# Heading 1\n\n## Heading2\n\n### Heading 3\n\n#### Heading 4\n\n##### Heading 5\n\n###### Heading 6"
                        ),
                        Label(text="## Form controls\n\n### Buttons"),
                        Row(
                            content=[
                                Column(
                                    content=[
                                        Label(text="Default:"),
                                        Button(
                                            text="Large",
                                            name="default_large",
                                            size="LARGE",
                                            purpose="DEFAULT",
                                        ),
                                        Button(
                                            text="Medium",
                                            name="default_medium",
                                            size="MEDIUM",
                                            purpose="DEFAULT",
                                        ),
                                        Button(
                                            text="Small",
                                            name="default_small",
                                            size="SMALL",
                                            purpose="DEFAULT",
                                        ),
                                    ]
                                ),
                                Column(
                                    content=[
                                        Label(text="Primary:"),
                                        Button(
                                            text="Large",
                                            name="primary_large",
                                            size="LARGE",
                                            purpose="PRIMARY",
                                        ),
                                        Button(
                                            text="Medium",
                                            name="primary_medium",
                                            size="MEDIUM",
                                            purpose="PRIMARY",
                                        ),
                                        Button(
                                            text="Small",
                                            name="primary_small",
                                            size="SMALL",
                                            purpose="PRIMARY",
                                        ),
                                    ]
                                ),
                                Column(
                                    content=[
                                        Label(text="Secondary:"),
                                        Button(
                                            text="Large",
                                            name="secondary_large",
                                            size="LARGE",
                                            purpose="SECONDARY",
                                        ),
                                        Button(
                                            text="Medium",
                                            name="secondary_medium",
                                            size="MEDIUM",
                                            purpose="SECONDARY",
                                        ),
                                        Button(
                                            text="Small",
                                            name="secondary_small",
                                            size="SMALL",
                                            purpose="SECONDARY",
                                        ),
                                    ]
                                ),
                                Column(
                                    content=[
                                        Label(text="Success:"),
                                        Button(
                                            text="Large",
                                            name="success_large",
                                            size="LARGE",
                                            purpose="SUCCESS",
                                        ),
                                        Button(
                                            text="Medium",
                                            name="success_medium",
                                            size="MEDIUM",
                                            purpose="SUCCESS",
                                        ),
                                        Button(
                                            text="Small",
                                            name="success_small",
                                            size="SMALL",
                                            purpose="SUCCESS",
                                        ),
                                    ]
                                ),
                                Column(
                                    content=[
                                        Label(text="Warning:"),
                                        Button(
                                            text="Large",
                                            name="warning_large",
                                            size="LARGE",
                                            purpose="WARNING",
                                        ),
                                        Button(
                                            text="Medium",
                                            name="warning_medium",
                                            size="MEDIUM",
                                            purpose="WARNING",
                                        ),
                                        Button(
                                            text="Small",
                                            name="warning_small",
                                            size="SMALL",
                                            purpose="WARNING",
                                        ),
                                    ]
                                ),
                                Column(
                                    content=[
                                        Label(text="Danger:"),
                                        Button(
                                            text="Large",
                                            name="danger_large",
                                            size="LARGE",
                                            purpose="DANGER",
                                        ),
                                        Button(
                                            text="Medium",
                                            name="danger_medium",
                                            size="MEDIUM",
                                            purpose="DANGER",
                                        ),
                                        Button(
                                            text="Small",
                                            name="danger_small",
                                            size="SMALL",
                                            purpose="DANGER",
                                        ),
                                    ]
                                ),
                            ],
                        ),
                        Label(text="### Inputs"),
                        CheckBox(label="A checkbox!"),
                        Switch(label="A switch!"),
                        Row(
                            content=[
                                Label(text="Favourite colour radio buttons: "),
                                Radio(
                                    label="Red", group="colour", value="red"
                                ),
                                Radio(
                                    label="Green",
                                    group="colour",
                                    value="green",
                                ),
                                Radio(
                                    label="Blue", group="colour", value="blue"
                                ),
                            ],
                        ),
                        Slider(),
                        FileUpload(),
                        Html(html="<hr>Some arbitrary HTML<hr>"),
                        ColorPicker(),
                        TextInput(
                            input_type="text",
                            placeholder="A standard text input",
                        ),
                        TextInput(
                            input_type="email", placeholder="An email input"
                        ),
                        TextInput(
                            input_type="password",
                            placeholder="A password input",
                        ),
                        TextInput(
                            input_type="tel", placeholder="A telephone input"
                        ),
                        TextInput(input_type="url", placeholder="A URL input"),
                        TextInput(
                            input_type="number", placeholder="A numeric input"
                        ),
                        DateTimePicker(),
                        DatePicker(),
                        TimePicker(),
                        Label(text="## Multimedia"),
                        Label(text="A test image:"),
                        Image(image=invent.media.images.testcard_invent.png),
                        Label(text="A test audio player:"),
                        Audio(source=invent.media.sounds.left_bank_two.ogg),
                        Label(text="A test video player:"),
                        Video(source=invent.media.video.testcard_invent.webm),
                        Label(text="## Layouts"),
                        Html(html="<p><span style='color: blue;'>Columns in blue</span>, <span style='color: red;'>rows in red</span>.</p>"),
                        Column(
                            border_color="blue",
                            border_width="S",
                            border_style="Dashed",
                            content=[
                                Row(
                                    border_color="red",
                                    border_width="S",
                                    border_style="Dotted",
                                    content=[
                                        Label(text="25%", layout={"flex": "1"}),
                                        Label(text="50%", layout={"flex": "2"}),
                                        Label(text="25%", layout={"flex": "1"}),
                                    ],
                                ),
                            ],
                        )
                    ]
                )
            ],
        ),
    ],
)

# GO! ##################################################################################


invent.go()
