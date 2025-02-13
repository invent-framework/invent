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
from .containers import Column, Grid, Page, Row
from .widgets.audio import Audio
from .widgets.button import Button
from .widgets.chart import Chart
from .widgets.checkbox import CheckBox
from .widgets.code import Code
from .widgets.color import ColorPicker
from .widgets.date import DatePicker
from .widgets.datetime import DateTimePicker
from .widgets.fileupload import FileUpload
from .widgets.html import Html
from .widgets.image import Image
from .widgets.map import Map
from .widgets.meter import Meter
from .widgets.progress import Progress
from .widgets.radio import Radio
from .widgets.selector import Selector
from .widgets.slider import Slider
from .widgets.switch import Switch
from .widgets.label import Label
from .widgets.table import Table
from .widgets.textinput import TextInput
from .widgets.time import TimePicker
from .widgets.video import Video


__all__ = [
    "Code",
    "Page",
    "Widget",
    "Container",
    "Column",
    "Grid",
    "Row",
    "from_datastore",
    "Audio",
    "Button",
    "Chart",
    "CheckBox",
    "Code",
    "ColorPicker",
    "DatePicker",
    "DateTimePicker",
    "FileUpload",
    "Html",
    "Image",
    "Map",
    "Meter",
    "Progress",
    "Radio",
    "Selector",
    "Slider",
    "Switch",
    "Label",
    "Table",
    "TextInput",
    "TimePicker",
    "Video",
]


AVAILABLE_COMPONENTS = {
    # Containers...
    _("Column"): Column,
    _("Row"): Row,
    _("Grid"): Grid,
    # Widgets...
    _("Audio"): Audio,
    _("Button"): Button,
    _("CheckBox"): CheckBox,
    _("Code"): Code,
    _("ColorPicker"): Code,
    _("DatePicker"): DatePicker,
    _("DateTimePicker"): DateTimePicker,
    _("FileUpload"): FileUpload,
    _("Html"): Html,
    _("Image"): Image,
    _("Radio"): Radio,
    _("Slider"): Slider,
    _("Switch"): Switch,
    _("Label"): Label,
    _("Table"): Table,
    _("TextInput"): TextInput,
    _("TimePicker"): TimePicker,
    _("Video"): Video,
}
