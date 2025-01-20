"""
This app is a simple test card for the theme system. We ensure all the various
UI aspects of the Invent framework are shown in a page, and allow the user to
select different "themes" to see how they affect the appearance of the page.
"""

import invent
from invent.ui import *

# Datastore ############################################################################

await invent.setup()  # Load default values for the datastore.

# Code #################################################################################

# User Interface #######################################################################

app = invent.App(
    name="Theme Testcard",
    pages=[
        Page(
            name="Testcard",
            children=[
                Column(
                    children=[
                        Row(
                            children=[
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
    return f"Hello, {name}" """
                        ),
                        Label(text="Some more extensive code:"),
                        Code(
                            code="""class Hello:  # Enterprise programmer 👔

  def __init__(self, name="world!"):
    self.name = name

  @property
  def greet(self):
    return f"{self.__class__.__name__} {name}"

print(Hello().greet)"""
                        ),
                        Label(
                            text="# Heading 1\n\n## Heading2\n\n### Heading 3\n\n#### Heading 4\n\n##### Heading 5\n\n###### Heading 6"
                        ),
                        Label(
                            text="## A table\n\nTakes a list of lists as data, with configurable options for headers and the caption. The style of the table depends upon the selected theme."
                        ),
                        Table(
                            data=[
                                [
                                    "",
                                    "Hamble",
                                    "Jemima",
                                    "Humpty",
                                    "Little Ted",
                                    "Big Ted",
                                ],
                                [
                                    "Toy-type",
                                    "Doll",
                                    "Rag doll",
                                    "Felt Egg",
                                    "Teddy",
                                    "Teddy",
                                ],
                                [
                                    "Dress",
                                    "Blue pinafore dress",
                                    "Woolly trousers and jumper",
                                    "Tartan trousers",
                                    "None (just fur)",
                                    "None (just fur)",
                                ],
                                [
                                    "Eyes",
                                    "Blue",
                                    "Blue",
                                    "Black",
                                    "Beady",
                                    "Beady",
                                ],
                                [
                                    "Nose",
                                    "Pink",
                                    "None",
                                    "White",
                                    "Black",
                                    "Black",
                                ],
                                [
                                    "Super power",
                                    "Sitting up",
                                    "Flopping over",
                                    "Rolling around",
                                    "Getting lost",
                                    "Falling off things",
                                ],
                            ],
                            label="The Play School toys",
                            row_headers=True,
                        ),
                        Label(text="## Form controls\n\n### Buttons"),
                        Row(
                            children=[
                                Column(
                                    children=[
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
                                    children=[
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
                                    children=[
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
                                    children=[
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
                                    children=[
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
                                    children=[
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
                            children=[
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
                        Meter(),
                        Progress(value=50),
                        Progress(),
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
                        Selector(choices=["One", "Two", "Three"]),
                        Label(text="## Multimedia"),
                        Label(text="A map:"),
                        Map(
                            markers=[
                                Map.Marker(
                                    popup_content="Hello, world! [A link](https://inventframework.org/)"
                                ),
                                Map.Marker(
                                    latitude=51.505,
                                    longitude=-0.09,
                                    popup_content=Label(text="# London"),
                                    icon=Map.MARKER_ICON_FLAG,
                                    icon_color="blue",
                                ),
                            ],
                        ),
                        Label(text="A default image:"),
                        Image(),
                        Label(text="A test image:"),
                        Image(image=invent.media.images.testcard_invent.png),
                        Label(text="A test audio player:"),
                        Audio(source=invent.media.sounds.left_bank_two.ogg),
                        Label(text="A test video player:"),
                        Video(source=invent.media.video.testcard_invent.webm),
                        Label(text="## Layouts"),
                        Html(
                            html="<p><span style='color: red;'>Rows are in red</span>, <span style='color: blue;'>columns in blue</span>,<br><span style='color: green;'>grids are in green</span>... (and this isn't a poem). 😉</p>"
                        ),
                        Label(text="Column with horizontally aligned rows."),
                        Column(
                            border_color="blue",
                            border_width="S",
                            border_style="Dotted",
                            children=[
                                Row(
                                    border_color="red",
                                    border_width="S",
                                    border_style="Dotted",
                                    children=[
                                        Label(text="25% default", flex="1"),
                                        Label(text="50% default", flex="2"),
                                        Label(text="25% default", flex="1"),
                                    ],
                                ),
                                Row(
                                    border_color="red",
                                    border_width="S",
                                    border_style="Dotted",
                                    horizontal_align="start",
                                    children=[
                                        Label(text="25% start", flex="1"),
                                        Label(
                                            text="50% start",
                                            flex="2",
                                        ),
                                        Label(
                                            text="25% start",
                                            flex="1",
                                        ),
                                    ],
                                ),
                                Row(
                                    border_color="red",
                                    border_width="S",
                                    border_style="Dotted",
                                    horizontal_align="center",
                                    children=[
                                        Label(
                                            text="25% center",
                                            flex="1",
                                        ),
                                        Label(
                                            text="50% center",
                                            flex="2",
                                        ),
                                        Label(
                                            text="25% center",
                                            flex="1",
                                        ),
                                    ],
                                ),
                                Row(
                                    border_color="red",
                                    border_width="S",
                                    border_style="Dotted",
                                    horizontal_align="end",
                                    children=[
                                        Label(text="25% end", flex="1"),
                                        Label(text="50% end", flex="2"),
                                        Label(text="25% end", flex="1"),
                                    ],
                                ),
                            ],
                        ),
                        Label(text="Row with vertically aligned columns."),
                        Row(
                            border_color="red",
                            border_width="S",
                            border_style="Dotted",
                            children=[
                                Column(
                                    border_color="blue",
                                    border_width="S",
                                    border_style="Dotted",
                                    children=[
                                        Label(text="Long cat is loooong..."),
                                        Image(
                                            image=invent.media.images.longcat.jpg
                                        ),
                                    ],
                                ),
                                Column(
                                    border_color="blue",
                                    border_width="S",
                                    border_style="Dotted",
                                    children=[
                                        Label(text="25% default", flex="1"),
                                        Label(text="50% default", flex="2"),
                                        Label(text="25% default", flex="1"),
                                    ],
                                ),
                                Column(
                                    border_color="blue",
                                    border_width="S",
                                    border_style="Dotted",
                                    vertical_align="start",
                                    children=[
                                        Label(text="25% start", flex="1"),
                                        Label(
                                            text="50% start",
                                            flex="2",
                                        ),
                                        Label(
                                            text="25% start",
                                            flex="1",
                                        ),
                                    ],
                                ),
                                Column(
                                    border_color="blue",
                                    border_width="S",
                                    border_style="Dotted",
                                    vertical_align="center",
                                    children=[
                                        Label(
                                            text="25% center",
                                            flex="1",
                                        ),
                                        Label(
                                            text="50% center",
                                            flex="2",
                                        ),
                                        Label(
                                            text="25% center",
                                            flex="1",
                                        ),
                                    ],
                                ),
                                Column(
                                    border_color="blue",
                                    border_width="S",
                                    border_style="Dotted",
                                    vertical_align="end",
                                    children=[
                                        Label(text="25% end", flex="1"),
                                        Label(text="50% end", flex="2"),
                                        Label(text="25% end", flex="1"),
                                    ],
                                ),
                                Column(
                                    border_color="blue",
                                    border_width="S",
                                    border_style="Dotted",
                                    flex=2,
                                    children=[Label(text="Flexed to fill.")],
                                ),
                            ],
                        ),
                        Label(text="Grid with row and column spans."),
                        Grid(
                            border_color="green",
                            border_width="S",
                            border_style="Dotted",
                            columns=3,
                            children=[
                                Label(
                                    text="Item 1 (colspan 2)",
                                    column_span=2,
                                    background_color="lightgrey",
                                ),
                                Label(
                                    text="Item 2", background_color="lightgrey"
                                ),
                                Label(
                                    text="Item 3", background_color="lightgrey"
                                ),
                                Label(
                                    text="Item 4 (rowspan 2), v/h align center",
                                    row_span=2,
                                    background_color="lightgrey",
                                    vertical_align="center",
                                    horizontal_align="center",
                                ),
                                Label(
                                    text="Item 5", background_color="lightgrey"
                                ),
                                Label(
                                    text="Item 6", background_color="lightgrey"
                                ),
                                Label(
                                    text="Item 7", background_color="lightgrey"
                                ),
                                Label(
                                    text="Item 8", background_color="lightgrey"
                                ),
                                Label(
                                    text="Item 9", background_color="lightgrey"
                                ),
                            ],
                        ),
                        Label(
                            text="A column with horizontally aligned widgets."
                        ),
                        Column(
                            border_color="blue",
                            border_width="S",
                            border_style="Dotted",
                            children=[
                                Button(text="Default"),
                                Button(text="Start", horizontal_align="start"),
                                Button(
                                    text="Center", horizontal_align="center"
                                ),
                                Button(text="End", horizontal_align="end"),
                                Button(
                                    text="Stretch", horizontal_align="stretch"
                                ),
                            ],
                        ),
                        Label(text="Row with vertically aligned widgets."),
                        Row(
                            border_color="red",
                            border_width="S",
                            border_style="Dotted",
                            children=[
                                Column(
                                    border_color="blue",
                                    border_width="S",
                                    border_style="Dotted",
                                    children=[
                                        Label(text="Long cat is loooong..."),
                                        Image(
                                            image=invent.media.images.longcat.jpg
                                        ),
                                    ],
                                ),
                                Button(text="Default"),
                                Button(text="Start", vertical_align="start"),
                                Button(text="Center", vertical_align="center"),
                                Button(text="End", vertical_align="end"),
                                Button(
                                    text="Stretch with fill",
                                    size="LARGE",
                                    vertical_align="stretch",
                                    flex="2",
                                ),
                            ],
                        ),
                    ]
                )
            ],
        ),
    ],
)

# GO! ##################################################################################

invent.go()
