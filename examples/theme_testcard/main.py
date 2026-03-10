"""
This app is a simple test card for the theme system. We ensure all the various
UI aspects of the Invent framework are shown in a page, and allow the user to
select different "themes" to see how they affect the appearance of the page.
"""

import random

import invent
from invent.ui import *

# Datastore ############################################################################

await invent.setup()  # Load default values for the datastore.

# Code #################################################################################

# Create some sample appointments for the calendar widget based upon today's month and
# year, so that the calendar will show some appointments when it is rendered. Needs to
# include both just plain dates, and datetimes with times, to show how both are rendered.
from datetime import date, datetime


def navigate(message):
    """
    Handle navigation between pages based on button clicks / names.
    """
    # Extract the page name from the button name. The button names are in the format
    # "pagename_button", so we split on "_button" and take the first part to get the page
    # name.
    page_name = message.button.name.split("_button")[0]
    invent.show_page(page_name)


invent.subscribe(navigate, to_channel="navigate", when_subject=["press"])


# Some random funky backgrounds for page 4. It's just boring CSS.
backgrounds = [
    "linear-gradient(to bottom, #ff7e5f, #feb47b)",  # Linear gradient.
    "#3498db",  # A solid single colour.
    f"url('{invent.media.images.repeat_image.png}') repeat",  # A repeated image.
    f"url('{invent.media.images.random.png}') center / cover no-repeat",  # A centered, cover image.
]


today = date.today()
appointments = {
    today.isoformat(): "Today's appointment",
    datetime(
        today.year, today.month, 10, 9, 0
    ).isoformat(): "Morning appointment",
    datetime(
        today.year, today.month, 10, 12, 0
    ).isoformat(): "Lunch appointment",
    datetime(
        today.year, today.month, 10, 15, 0
    ).isoformat(): "Afternoon appointment",
    datetime(
        today.year, today.month, 10, 18, 0
    ).isoformat(): "Evening appointment",
    datetime(
        today.year, today.month, 15, 14, 30
    ).isoformat(): "Meeting with Bob",
    datetime(
        today.year, today.month, 20, 19, 0
    ).isoformat(): "Dinner with Alice",
    datetime(
        today.year, today.month, 25, 9, 0
    ).isoformat(): "Dentist appointment",
}
invent.datastore["calendar_appointments"] = appointments

# User Interface #######################################################################

app = invent.App(
    name="Theme Testcard",
    pages=[
        Page(
            id="testcard",
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
                        Label(
                            text="This is a test card for the Invent framework. It includes all the different widgets and components in the framework, so that we can see how they look with different themes applied."
                        ),
                        Row(
                            children=[
                                Button(
                                    text="Visit page 2",
                                    name="page2_button",
                                    purpose="PRIMARY",
                                    channel="navigate",
                                ),
                                Button(
                                    text="Random transition to page 3",
                                    name="page3_button",
                                    purpose="PRIMARY",
                                    channel="navigate",
                                ),
                                Button(
                                    text="Random background on page 4",
                                    name="page4_button",
                                    purpose="PRIMARY",
                                    channel="navigate",
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
                        Code(code="""def hello(name="world"):
    return f"Hello, {name}" """),
                        Label(text="Some more extensive code:"),
                        Code(code="""class Hello:  # Enterprise programmer 👔

  def __init__(self, name="world!"):
    self.name = name

  @property
  def greet(self):
    return f"{self.__class__.__name__} {name}"

print(Hello().greet)"""),
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
                        Label(text="Avatars:"),
                        Row(
                            children=[
                                Label(text="Extra small avatars:"),
                                Avatar(
                                    name="Default avatar",
                                    size="XS",
                                ),
                                Avatar(
                                    name="Circle avatar",
                                    image="https://i.pravatar.cc/40?img=49",
                                    shape="CIRCLE",
                                    size="XS",
                                ),
                                Avatar(
                                    name="Rounded avatar",
                                    image="https://i.pravatar.cc/40?img=50",
                                    shape="ROUNDED",
                                    size="XS",
                                ),
                                Avatar(
                                    name="Square avatar",
                                    image="https://i.pravatar.cc/40?img=51",
                                    shape="SQUARE",
                                    size="XS",
                                ),
                            ]
                        ),
                        Row(
                            children=[
                                Label(text="Small avatars:"),
                                Avatar(
                                    name="Default avatar",
                                    size="S",
                                ),
                                Avatar(
                                    name="Circle avatar",
                                    image="https://i.pravatar.cc/40?img=49",
                                    shape="CIRCLE",
                                    size="S",
                                ),
                                Avatar(
                                    name="Rounded avatar",
                                    image="https://i.pravatar.cc/40?img=50",
                                    shape="ROUNDED",
                                    size="S",
                                ),
                                Avatar(
                                    name="Square avatar",
                                    image="https://i.pravatar.cc/40?img=51",
                                    shape="SQUARE",
                                    size="S",
                                ),
                            ]
                        ),
                        Row(
                            children=[
                                Label(text="Medium avatars:"),
                                Avatar(
                                    name="Default avatar",
                                ),
                                Avatar(
                                    name="Circle avatar",
                                    image="https://i.pravatar.cc/60?img=49",
                                    shape="CIRCLE",
                                ),
                                Avatar(
                                    name="Rounded avatar",
                                    image="https://i.pravatar.cc/60?img=50",
                                    shape="ROUNDED",
                                ),
                                Avatar(
                                    name="Square avatar",
                                    image="https://i.pravatar.cc/60?img=51",
                                    shape="SQUARE",
                                ),
                            ]
                        ),
                        Row(
                            children=[
                                Label(text="Large avatars:"),
                                Avatar(
                                    name="Default avatar",
                                    size="L",
                                ),
                                Avatar(
                                    name="Circle avatar",
                                    image="https://i.pravatar.cc/80?img=49",
                                    shape="CIRCLE",
                                    size="L",
                                ),
                                Avatar(
                                    name="Rounded avatar",
                                    image="https://i.pravatar.cc/80?img=50",
                                    shape="ROUNDED",
                                    size="L",
                                ),
                                Avatar(
                                    name="Square avatar",
                                    image="https://i.pravatar.cc/80?img=51",
                                    shape="SQUARE",
                                    size="L",
                                ),
                            ]
                        ),
                        Row(
                            children=[
                                Label(text="Extra large avatars:"),
                                Avatar(
                                    name="Default avatar",
                                    size="XL",
                                ),
                                Avatar(
                                    name="Circle avatar",
                                    image="https://i.pravatar.cc/100?img=49",
                                    shape="CIRCLE",
                                    size="XL",
                                ),
                                Avatar(
                                    name="Rounded avatar",
                                    image="https://i.pravatar.cc/100?img=50",
                                    shape="ROUNDED",
                                    size="XL",
                                ),
                                Avatar(
                                    name="Square avatar",
                                    image="https://i.pravatar.cc/100?img=51",
                                    shape="SQUARE",
                                    size="XL",
                                ),
                            ]
                        ),
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
                            tile_set=Map.TILES_SATELLITE,
                        ),
                        Label(text="A bar chart:"),
                        Chart(
                            chart_type="bar",
                            data={
                                "labels": [
                                    "Italy",
                                    "France",
                                    "Spain",
                                    "USA",
                                    "Argentina",
                                ],
                                "datasets": [
                                    {
                                        "label": "Volume of wine produced (in hectolitres)",
                                        "backgroundColor": [
                                            "red",
                                            "green",
                                            "blue",
                                            "orange",
                                            "brown",
                                        ],
                                        "data": [55, 49, 44, 24, 15],
                                    }
                                ],
                            },
                            options={
                                "plugins": {
                                    "title": {
                                        "display": True,
                                        "text": "World Wide Wine Production",
                                    },
                                },
                            },
                        ),
                        Label(text="A default image:"),
                        Image(),
                        Label(text="A test image:"),
                        Image(image=invent.media.images.testcard_invent.png),
                        Label(text="A test audio player:"),
                        Audio(source=invent.media.sounds.left_bank_two.ogg),
                        Label(text="A test video player (local source):"),
                        Video(source=invent.media.video.testcard_invent.webm),
                        Label(text="A test video player (Youtube):"),
                        Video(
                            source="https://www.youtube.com/watch?v=Rq9Zbz_IJSc"
                        ),
                        Label(text="A test video player (Vimeo):"),
                        Video(source="https://vimeo.com/347119375"),
                        Label(text="## Layouts"),
                        Label(text="A modal triggered by a button:"),
                        Modal(
                            text="Open modal",
                            children=[
                                Label(
                                    text="This is the content of the modal. It can contain any widgets, and is displayed in a layer above the main content when the trigger button is pressed."
                                ),
                                Button(text="A button in a modal"),
                                Video(
                                    source=invent.media.video.testcard_invent.webm
                                ),
                                CheckBox(label="A checkbox!"),
                                Switch(label="A switch!"),
                                Row(
                                    children=[
                                        Label(
                                            text="Favourite colour radio buttons: "
                                        ),
                                        Radio(
                                            label="Red",
                                            group="colour",
                                            value="red",
                                        ),
                                        Radio(
                                            label="Green",
                                            group="colour",
                                            value="green",
                                        ),
                                        Radio(
                                            label="Blue",
                                            group="colour",
                                            value="blue",
                                        ),
                                    ],
                                ),
                                Slider(),
                                Meter(),
                                Progress(value=50),
                                Progress(),
                            ],
                        ),
                        Label(text="Alerts:"),
                        Alert(
                            title="🚨 This is an alert",
                            text="This is an alert with the default purpose. It has a title and some text to show how the alert looks with both of those things. It also has a dismiss button (X).\n\n We can write Markdown in the text of the alert, so we can have **strong** and *emphasised* text, as well as [links](https://inventframework.org/) in the alert too!",
                            dismissable=True,
                        ),
                        Alert(
                            title="ℹ️ This is an informational (primary) alert",
                            text="This is an alert with the informational purpose. It has a title and some text to show how the alert looks with both of those things. It also has a dismiss button.",
                            purpose="PRIMARY",
                            dismissable=True,
                        ),
                        Alert(
                            title="💡 This is a secondary alert",
                            text="This is an alert with the secondary purpose. It has a title and some text to show how the alert looks with both of those things. It also has a dismiss button.",
                            purpose="SECONDARY",
                            dismissable=True,
                        ),
                        Alert(
                            title="⚠️ This is a warning alert",
                            text="This is an alert with the warning purpose. It has a title and some text to show how the alert looks with both of those things. It also has a dismiss button.",
                            purpose="WARNING",
                            dismissable=True,
                        ),
                        Alert(
                            title="❌ This is a danger alert",
                            text="This is an alert with the danger purpose. It has a title and some text to show how the alert looks with both of those things. **BY DEFAULT** alerts don't have a dismiss button (like here).",
                            purpose="DANGER",
                        ),
                        Alert(
                            title="✅ This is a success alert",
                            text="This is an alert with the success purpose. It has a title and some text to show how the alert looks with both of those things. It is not dismissable by default (but could be).",
                            purpose="SUCCESS",
                        ),
                        Label(text="Content cards:"),
                        ContentCard(
                            children=[
                                Label(
                                    text="This is a default content card. It can be used to display content that is related to a specific topic or theme. The content can include text, images, and other widgets."
                                ),
                                Button(
                                    text="A button in a content card",
                                    purpose="PRIMARY",
                                ),
                            ]
                        ),
                        ContentCard(
                            title="Content card with image, timestamp and primary purpose",
                            image=invent.media.images.testcard_invent.png,
                            published_at=datetime(2025, 12, 31, 23, 59),
                            children=[
                                Label(
                                    text="This is a content card with an image and a timestamp. The image is displayed as an avatar in the header of the card, and the timestamp is displayed at the top of the card."
                                ),
                                Button(
                                    text="Another button in a content card",
                                    purpose="PRIMARY",
                                ),
                            ],
                            purpose="PRIMARY",
                        ),
                        ContentCard(
                            title="Rounded content card with avatar image, end timestamp and success purpose",
                            image=invent.media.images.testcard_invent.png,
                            published_at=datetime(2025, 12, 31, 23, 59),
                            publish_position="end",
                            children=[
                                Label(
                                    text="This is a rounded content card with an avatar image and the publication timestamp at the end."
                                ),
                            ],
                            purpose="SUCCESS",
                        ),
                        ContentCard(
                            title="A Content card with a banner image, timestamp and secondary purpose",
                            image=invent.media.images.testcard_invent.png,
                            image_position="banner",
                            published_at=datetime(2025, 12, 31, 23, 59),
                            children=[
                                Label(
                                    text="This is a content card with a banner image. The image is displayed at the top of the card, and spans the full width of the card."
                                ),
                            ],
                            purpose="SECONDARY",
                        ),
                        ContentCard(
                            shape="square",
                            title="Square content card with banner image and end timestamp",
                            image_position="banner",
                            publish_position="end",
                            children=[
                                Label(
                                    text="This is a square content card with a banner image and the publication timestamp at the end."
                                ),
                                Label(
                                    text="The content card can contain any content, including other widgets. In this case, it contains another label and a button."
                                ),
                                Audio(
                                    source=invent.media.sounds.left_bank_two.ogg
                                ),
                                Label(
                                    text="Remember, that labels can also contain Markdown, so you can have **strong** and *emphasised* text, as well as [links](https://inventframework.org/) in the content of the card too!"
                                ),
                            ],
                            image=invent.media.images.testcard_invent.png,
                            published_at=datetime(2025, 12, 31, 23, 59),
                        ),
                        ContentCard(
                            title="Rounded content card with avatar image, end timestamp and warning purpose",
                            image=invent.media.images.testcard_invent.png,
                            published_at=datetime(2025, 12, 31, 23, 59),
                            publish_position="end",
                            children=[
                                Label(
                                    text="This is a rounded content card with an avatar image and the publication timestamp at the end."
                                ),
                            ],
                            purpose="WARNING",
                        ),
                        ContentCard(
                            title="A content card with the 'danger' purpose",
                            purpose="DANGER",
                            image_position="banner",
                            children=[
                                Label(
                                    text="This is a content card with the 'danger' purpose. The purpose of a content card affects the background and border colours of the card, and can be used to visually indicate the importance or urgency of the content."
                                ),
                            ],
                            image=invent.media.images.testcard_invent.png,
                            published_at=datetime(2025, 12, 31, 23, 59),
                        ),
                        Label(text="Conversational UI with chat bubbles:"),
                        Timeline(
                            children=[
                                ChatBubble(
                                    author_name="Alice",
                                    author_image="https://i.pravatar.cc/40?img=49",
                                    timestamp=datetime(2026, 1, 1, 10, 0),
                                    direction="sent",
                                    content="Happy New Year! 🎉",
                                ),
                                ChatBubble(
                                    author_name="Bob",
                                    author_image="https://i.pravatar.cc/40?img=66",
                                    timestamp=datetime(2026, 1, 1, 10, 1),
                                    content="Happy New Year to you too, Alice! 🥳",
                                    direction="received",
                                ),
                                ChatBubble(
                                    author_name="Eve",
                                    direction="received",
                                    content="Happy new year folks. How are you celebrating? (I don't have an avatar because I prefer to remain mysterious 👻)",
                                    timestamp=datetime(2026, 1, 1, 10, 2),
                                ),
                                ChatBubble(
                                    author_name="Alice",
                                    author_image="https://i.pravatar.cc/40?img=49",
                                    timestamp=datetime(2026, 1, 1, 10, 3),
                                    direction="sent",
                                    content="I'm having a party with some friends. We're playing board games and eating snacks. What about you, Bob?",
                                ),
                                ChatBubble(
                                    author_name="Bob",
                                    author_image="https://i.pravatar.cc/40?img=66",
                                    timestamp=datetime(2026, 1, 1, 10, 4),
                                    content="I'm having a quiet night in with my family. We're watching a movie and eating popcorn. 📽️🍿 What about you, Eve?",
                                    direction="received",
                                ),
                                ChatBubble(
                                    author_name="Eve",
                                    direction="received",
                                    content="I'm at a fancy restaurant with my partner. We're enjoying a delicious meal and some champagne. Cheers! 🥂",
                                    timestamp=datetime(2026, 1, 1, 10, 5),
                                ),
                                ChatBubble(
                                    author_name="Fred",
                                    author_image="https://i.pravatar.cc/40?img=51",
                                    direction="received",
                                    content="Hey folks, I'm having a blast at the beach with some friends.\n\nWe're playing volleyball and swimming in the ocean. 🌊🏐",
                                    timestamp=datetime(2026, 1, 1, 10, 6),
                                ),
                                ChatBubble(
                                    author_name="Mary",
                                    author_image="https://i.pravatar.cc/40?img=22",
                                    direction="received",
                                    content="Hi everyone, I'm having a relaxing night at home. I'm reading a book and sipping on some hot chocolate. 📚☕",
                                    timestamp=datetime(2026, 1, 1, 10, 7),
                                ),
                                ChatBubble(
                                    author_name="Alice",
                                    author_image="https://i.pravatar.cc/40?img=49",
                                    timestamp=datetime(2026, 1, 1, 10, 8),
                                    direction="sent",
                                    content="""That sounds lovely, Mary. Enjoy your book and hot chocolate! 📖☕
                                    
And Fred, the beach sounds like so much fun! Don't forget to put on some sunscreen! 🏖️🧴

Did I mention these messages all render _Markdown_? **Markdown** is supported in chat bubbles, 
so you can have _emphasis_, **strong text**, and [links](https://inventframework.org/) in your messages too!
                                    """,
                                ),
                                ChatBubble(
                                    author_name="Bob",
                                    author_image="https://i.pravatar.cc/40?img=66",
                                    timestamp=datetime(2026, 1, 1, 10, 9),
                                    direction="received",
                                    content="""You can have [links in messages](https://inventframework.org/)? That's amazing! I had no idea. I thought chat bubbles were just for plain text.""",
                                ),
                                ChatBubble(
                                    author_name="Fred",
                                    author_image="https://i.pravatar.cc/40?img=51",
                                    direction="received",
                                    content="""I know about the Markdown support, Alice! Bob, this will blow your mind... 🤯
                                    
I was just about to say how great it is that we can have _emphasis_ and **strong text** in our messages. 

It makes chatting so much more fun and expressive! 😄

Did I ever mention we can also include [links](https://inventframework.org/) in our messages? It's fantastic for sharing cool stuff with each other! 🌐

Also, it's possible to include emojis in the messages, as you can see! 🎉🥳😊

Finally, for extra fun, we can even define a custom background colour for each chat bubble, and the text and link
colours will automatically adjust to ensure they are readable against the background. How cool is that? 😎""",
                                    timestamp=datetime(2026, 1, 1, 10, 9),
                                    shade="#e0f712",
                                ),
                                ChatBubble(
                                    author_name="Alice",
                                    author_image="https://i.pravatar.cc/40?img=49",
                                    timestamp=datetime(2026, 1, 1, 10, 10),
                                    direction="sent",
                                    shade="#e0a9db",
                                    content="""Fred... you are showing off now. 😆
But I have to admit, the custom background colour with automatic contrast text and [link colours](https://inventframework.org/) is pretty neat.

Those Invent developers are really trying to think of everything to help make our lives easier, aren't they?

🎨🎨🎨🎨🎨🎨
""",
                                ),
                            ],
                        ),
                        Label(text="An accordion:"),
                        Accordion(
                            children=[
                                Label(
                                    name="Item 1",
                                    text="This is an accordion item.",
                                ),
                                Label(
                                    name="Item 2",
                                    text="It can contain other components.",
                                ),
                                Column(
                                    name="Item 3",
                                    children=[
                                        Label(
                                            text="This is a column inside an accordion item."
                                        ),
                                        Button(
                                            text="A button in a column",
                                            purpose="PRIMARY",
                                        ),
                                        TextInput(
                                            input_type="text",
                                            placeholder="A text input in a column",
                                        ),
                                    ],
                                ),
                                Label(
                                    name="Item 4",
                                    text="You can add as many items as you like, and they will be hidden until you click on the header.",
                                ),
                            ],
                        ),
                        Label(text="Tabs:"),
                        Tabs(
                            children=[
                                Label(
                                    name="Item 1",
                                    text="This is a tab item.",
                                ),
                                Label(
                                    name="Item 2",
                                    text="It can contain other components.",
                                ),
                                Column(
                                    name="Item 3",
                                    children=[
                                        Label(
                                            text="This is a column inside a tab item."
                                        ),
                                        Button(
                                            text="A button in a column",
                                            purpose="PRIMARY",
                                        ),
                                        TextInput(
                                            input_type="text",
                                            placeholder="A text input in a column",
                                        ),
                                    ],
                                ),
                                Label(
                                    name="Item 4",
                                    text="You can add as many items as you like, and they will be hidden until you click on the tab.",
                                ),
                            ],
                        ),
                        Label(text="A tree container:"),
                        Tree(
                            data=(
                                (
                                    "Item 1",
                                    (
                                        (
                                            "Subitem 1",
                                            "This is a sub-leaf node.",
                                        ),
                                        (
                                            "Subitem 2",
                                            Label(
                                                text="This is a widget leaf node."
                                            ),
                                        ),
                                        (
                                            "Subitem 3",
                                            (
                                                (
                                                    "Subsubitem 1",
                                                    "This is a sub-sub-leaf node.",
                                                ),
                                                (
                                                    "Subsubitem 2",
                                                    "This is another sub-sub-leaf node.",
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                                (
                                    "Item 2",
                                    (
                                        (
                                            "Subitem 1",
                                            "This is a sub-leaf node.",
                                        ),
                                        (
                                            "Subitem 2",
                                            Label(
                                                text="This is a widget leaf node."
                                            ),
                                        ),
                                        (
                                            "Subitem 3",
                                            (
                                                (
                                                    "Subsubitem 1",
                                                    "This is a sub-sub-leaf node.",
                                                ),
                                                (
                                                    "Subsubitem 2",
                                                    "This is another sub-sub-leaf node.",
                                                ),
                                            ),
                                        ),
                                    ),
                                ),
                                ("Item 3", "This is a leaf node."),
                            )
                        ),
                        Label(text="A calendar:"),
                        Calendar(
                            appointments=from_datastore(
                                "calendar_appointments"
                            )
                        ),
                        Label(text="A header:"),
                        Header(
                            children=[
                                Label(text="This is a non sticky header."),
                                Button(
                                    text="A button in the header",
                                    purpose="PRIMARY",
                                ),
                            ],
                        ),
                        Label(text="A footer:"),
                        Footer(
                            children=[
                                Label(text="This is a sticky footer."),
                                Button(
                                    text="A button in the footer",
                                    purpose="PRIMARY",
                                ),
                            ],
                            sticky=True,
                        ),
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
                                    vertical_align_content="center",
                                    children=[
                                        Label(
                                            text="Flexed to fill, v align content center"
                                        )
                                    ],
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
                                Row(
                                    border_color="red",
                                    border_width="S",
                                    border_style="Dotted",
                                    horizontal_align_content="center",
                                    children=[
                                        Label(
                                            text="Item 9a, h align content center",
                                            background_color="lightgrey",
                                        ),
                                        Label(
                                            text="Item 9b",
                                            background_color="lightgrey",
                                        ),
                                    ],
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
                ),
            ],
        ),
        Page(
            id="page2",
            children=[
                Label(
                    text="# This is page 2.\n\nThe content cards below are all examples of different configurations of the content card component, which is a versatile component for displaying content in a visually appealing way. The content card can be configured with different shapes, image positions, publication timestamp positions, and purposes to suit a wide variety of use cases."
                ),
                ContentCard(
                    title="Default content card with banner image and start timestamp",
                    children=[
                        Label(
                            text="This is a default content card with the image positioned as a banner at the top, and the publication timestamp positioned at the start (below the title)."
                        ),
                    ],
                    image=invent.media.images.testcard_invent.png,
                    published_at=datetime(2025, 12, 31, 23, 59),
                ),
                Button(
                    text="Back to Testcard page",
                    name="testcard_button",
                    channel="navigate",
                ),
            ],
        ),
        Page(
            id="page3",
            transition=random.choice(
                ["FADE", "SLIDE", "ZOOM", "CONVEX", "CONCAVE"]
            ),
            transition_speed=random.choice(["SLOW", "MEDIUM", "FAST"]),
            children=[
                Label(
                    text="# This is page 3.\n\nThe content cards below are all examples of different configurations of the content card component, which is a versatile component for displaying content in a visually appealing way. The content card can be configured with different shapes, image positions, publication timestamp positions, and purposes to suit a wide variety of use cases."
                ),
                ContentCard(
                    title="Default content card with banner image and start timestamp",
                    children=[
                        Label(
                            text="This is a default content card with the image positioned as a banner at the top, and the publication timestamp positioned at the start (below the title)."
                        ),
                    ],
                    image=invent.media.images.testcard_invent.png,
                    published_at=datetime(2025, 12, 31, 23, 59),
                ),
                Button(
                    text="Back to Testcard page",
                    name="testcard_button",
                    channel="navigate",
                ),
            ],
        ),
        Page(
            id="page4",
            background=random.choice(backgrounds),
            children=[
                Label(
                    text="# This is page 4.\n\nThe content cards below are all examples of different configurations of the content card component, which is a versatile component for displaying content in a visually appealing way. The content card can be configured with different shapes, image positions, publication timestamp positions, and purposes to suit a wide variety of use cases."
                ),
                ContentCard(
                    title="Default content card with banner image and start timestamp",
                    children=[
                        Label(
                            text="This is a default content card with the image positioned as a banner at the top, and the publication timestamp positioned at the start (below the title)."
                        ),
                    ],
                    image=invent.media.images.testcard_invent.png,
                    published_at=datetime(2025, 12, 31, 23, 59),
                ),
                Button(
                    text="Back to Testcard page",
                    name="testcard_button",
                    channel="navigate",
                ),
            ],
        ),
    ],
)

# GO! ##################################################################################

invent.go()
