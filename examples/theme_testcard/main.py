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
                                Label(text="# Test Card"),
                                Image(image=invent.media.images.invent_logo.png),
                            ]
                        ),  
                        Label(
                            text="## Textual styling"
                        ),
                        Label(
                            text="""This is a paragraph of text. I can have **strong** and *emphasised* text, as well as [links](https://inventframework.org/) to elsewhere. 
                            
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. 
                            
That should be long enough to wrap around to the next line.

Here's some code:"""
                        ),
                        Code(code="""def hello(name="world"):
    return f"Hello, {name}"
                             """),
                        Label(
                            text="# Heading 1\n\n## Heading2\n\n### Heading 3\n\n#### Heading 4\n\n##### Heading 5\n\n###### Heading 6"
                        ),
                        Label(text="## Form controls\n\n### Buttons\n\nHere's a row of Default buttons:"),
                        Row(
                            content=[
                                Button(
                                    text="Default Large",
                                    name="default_large",
                                    size="LARGE",
                                    purpose="DEFAULT",
                                ),
                                Button(
                                    text="Default Medium",
                                    name="default_medium",
                                    size="MEDIUM",
                                    purpose="DEFAULT",
                                ),
                                Button(
                                    text="Default Small",
                                    name="default_small",
                                    size="SMALL",
                                    purpose="DEFAULT",
                                ),
                            ],
                        ),
                        Label(text="Here's a row of Primary buttons:"),
                        Row(
                            content=[
                                Button(
                                    text="Primary Large",
                                    name="primary_large",
                                    size="LARGE",
                                    purpose="PRIMARY",
                                ),
                                Button(
                                    text="Primary Medium",
                                    name="primary_medium",
                                    size="MEDIUM",
                                    purpose="PRIMARY",
                                ),
                                Button(
                                    text="Primary Small",
                                    name="primary_small",
                                    size="SMALL",
                                    purpose="PRIMARY",
                                ),
                            ],
                        ),
                        Label(text="Here's a row of Secondary buttons:"),
                        Row(
                            content=[
                                Button(
                                    text="Secondary Large",
                                    name="secondary_large",
                                    size="LARGE",
                                    purpose="SECONDARY",
                                ),
                                Button(
                                    text="Secondary Medium",
                                    name="secondary_medium",
                                    size="MEDIUM",
                                    purpose="SECONDARY",
                                ),
                                Button(
                                    text="Secondary Small",
                                    name="secondary_small",
                                    size="SMALL",
                                    purpose="SECONDARY",
                                ),
                            ],
                        ),
                        Label(text="Here's a row of Success buttons:"),
                        Row(
                            content=[
                                Button(
                                    text="Success Large",
                                    name="success_large",
                                    size="LARGE",
                                    purpose="SUCCESS",
                                ),
                                Button(
                                    text="Success Medium",
                                    name="success_medium",
                                    size="MEDIUM",
                                    purpose="SUCCESS",
                                ),
                                Button(
                                    text="Success Small",
                                    name="success_small",
                                    size="SMALL",
                                    purpose="SUCCESS",
                                ),
                            ]
                        ),
                        Label(text="Here's a row of Warning buttons:"),
                        Row(
                            content=[
                                Button(
                                    text="Warning Large",
                                    name="warning_large",
                                    size="LARGE",
                                    purpose="WARNING",
                                ),
                                Button(
                                    text="Warning Medium",
                                    name="warning_medium",
                                    size="MEDIUM",
                                    purpose="WARNING",
                                ),
                                Button(
                                    text="Warning Small",
                                    name="warning_small",
                                    size="SMALL",
                                    purpose="WARNING",
                                ),
                            ],
                        ),
                        Label(text="Here's a row of Danger buttons:"),
                        Row(
                            content=[
                                Button(
                                    text="Danger Large",
                                    name="danger_large",
                                    size="LARGE",
                                    purpose="DANGER",
                                ),
                                Button(
                                    text="Danger Medium",
                                    name="danger_medium",
                                    size="MEDIUM",
                                    purpose="DANGER",
                                ),
                                Button(
                                    text="Danger Small",
                                    name="danger_small",
                                    size="SMALL",
                                    purpose="DANGER",
                                ),
                            ],
                        ),
                        Label(text="### Inputs"),
                        CheckBox(label="A checkbox!"),
                        Slider(),
                        FileUpload(),
                        Html(html="<hr>Some arbitrary HTML<hr>"),
                        Switch(label="A switch!"),
                        TextInput(input_type="text", placeholder="A text input"),
                        TextInput(input_type="email", placeholder="An email input"),
                        TextInput(input_type="password", placeholder="A password input"),
                        TextInput(input_type="tel", placeholder="A telephone input"),
                        TextInput(input_type="url", placeholder="A URL input"),
                        Label(text="## Multimedia"),
                        Label(text="A test image:"),
                        Image(image=invent.media.images.testcard_invent.png),
                        Label(text="A test audio player:"),
                        Audio(source=invent.media.sounds.left_bank_two.ogg),
                        Label(text="A test video player:"),
                        Video(source=invent.media.video.testcard_invent.webm),
                    ]
                )
            ],
        ),
    ],
)

# GO! ##################################################################################


invent.go()
