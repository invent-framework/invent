"""
The core classes for user interface things in the Invent framework.

Based on original pre-COVID work by [Nicholas H.Tollervey.](https://ntoll.org/)

Copyright (c) 2019-present Invent contributors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from ..i18n import _
from .core import Widget, Container, from_datastore
from .containers import (
    Accordion,
    Carousel,
    Column,
    Footer,
    Grid,
    Header,
    Page,
    Row,
    Tabs,
    Timeline,
    Tree,
)
from .widgets.alert import Alert
from .widgets.audio import Audio
from .widgets.avatar import Avatar
from .widgets.button import Button
from .widgets.buttongroup import ButtonGroup
from .widgets.calendar import Calendar
from .widgets.chart import Chart
from .widgets.chatbubble import ChatBubble
from .widgets.checkbox import CheckBox
from .widgets.code import Code
from .widgets.color import ColorPicker
from .widgets.contentcard import ContentCard
from .widgets.date import DatePicker
from .widgets.datetime import DateTimePicker
from .widgets.divider import Divider
from .widgets.fileupload import FileUpload
from .widgets.html import Html
from .widgets.image import Image
from .widgets.label import Label
from .widgets.map import Map
from .widgets.menu import Menu
from .widgets.meter import Meter
from .widgets.modal import Modal
from .widgets.progress import Progress
from .widgets.radio import Radio
from .widgets.rating import Rating
from .widgets.selector import Selector
from .widgets.slider import Slider
from .widgets.switch import Switch
from .widgets.table import Table
from .widgets.textinput import TextInput
from .widgets.time import TimePicker
from .widgets.video import Video

__all__ = [
    "Code",
    "Page",
    "Widget",
    "Accordion",
    "Carousel",
    "Container",
    "Column",
    "Footer",
    "Grid",
    "Header",
    "Row",
    "Tabs",
    "from_datastore",
    "Alert",
    "Audio",
    "Avatar",
    "Button",
    "ButtonGroup",
    "Calendar",
    "Chart",
    "ChatBubble",
    "CheckBox",
    "Code",
    "ColorPicker",
    "ContentCard",
    "DatePicker",
    "DateTimePicker",
    "Divider",
    "FileUpload",
    "Html",
    "Image",
    "Label",
    "Map",
    "Menu",
    "Meter",
    "Modal",
    "Progress",
    "Radio",
    "Rating",
    "Selector",
    "Slider",
    "Switch",
    "Table",
    "TextInput",
    "Timeline",
    "TimePicker",
    "Tree",
    "Video",
]


AVAILABLE_COMPONENTS = {
    # Containers...
    _("Accordion"): Accordion,
    _("Avatar"): Avatar,
    _("Column"): Column,
    _("Footer"): Footer,
    _("Grid"): Grid,
    _("Header"): Header,
    _("Popup"): Modal,
    _("Row"): Row,
    _("Tabs"): Tabs,
    _("Timeline"): Timeline,
    _("Tree"): Tree,
    # Widgets...
    _("Alert"): Alert,
    _("Audio"): Audio,
    _("Button"): Button,
    _("Calendar"): Calendar,
    _("Chart"): Chart,
    _("CheckBox"): CheckBox,
    _("Code"): Code,
    _("ColorPicker"): ColorPicker,
    _("ContentCard"): ContentCard,
    _("DatePicker"): DatePicker,
    _("DateTimePicker"): DateTimePicker,
    _("Divider"): Divider,
    _("FileUpload"): FileUpload,
    _("Html"): Html,
    _("Image"): Image,
    _("Radio"): Radio,
    _("Rating"): Rating,
    _("Slider"): Slider,
    _("Switch"): Switch,
    _("Label"): Label,
    _("Table"): Table,
    _("TextInput"): TextInput,
    _("TimePicker"): TimePicker,
    _("Video"): Video,
}
