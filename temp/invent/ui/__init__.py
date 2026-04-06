_X='Webcam'
_W='TimePicker'
_V='Timeline'
_U='TextEditor'
_T='TextInput'
_S='Terminal'
_R='Switch'
_Q='Slider'
_P='Rating'
_O='FileUpload'
_N='Divider'
_M='DateTimePicker'
_L='DatePicker'
_K='ContentCard'
_J='ColorPicker'
_I='CheckBox'
_H='Calendar'
_G='Button'
_F='Avatar'
_E='Header'
_D='Footer'
_C='Column'
_B='Accordion'
_A='Code'
from..i18n import _
from.core import Widget,Container,from_datastore
from.containers import Accordion,Carousel,Column,Footer,Grid,Header,Page,Row,Tabs,Timeline,Tree
from.widgets.alert import Alert
from.widgets.audio import Audio
from.widgets.avatar import Avatar
from.widgets.button import Button
from.widgets.buttongroup import ButtonGroup
from.widgets.calendar import Calendar
from.widgets.chart import Chart
from.widgets.chatbubble import ChatBubble
from.widgets.checkbox import CheckBox
from.widgets.code import Code
from.widgets.codeeditor import CodeEditor
from.widgets.color import ColorPicker
from.widgets.contentcard import ContentCard
from.widgets.date import DatePicker
from.widgets.datetime import DateTimePicker
from.widgets.divider import Divider
from.widgets.fileupload import FileUpload
from.widgets.html import Html
from.widgets.image import Image
from.widgets.label import Label
from.widgets.map import Map
from.widgets.menu import Menu
from.widgets.meter import Meter
from.widgets.modal import Modal
from.widgets.progress import Progress
from.widgets.radio import Radio
from.widgets.rating import Rating
from.widgets.selector import Selector
from.widgets.slider import Slider
from.widgets.switch import Switch
from.widgets.table import Table
from.widgets.terminal import Terminal
from.widgets.textinput import TextInput
from.widgets.texteditor import TextEditor
from.widgets.time import TimePicker
from.widgets.video import Video
from.widgets.webcam import Webcam
__all__=[_A,'Page','Widget',_B,'Carousel','Container',_C,_D,'Grid',_E,'Row','Tabs','from_datastore','Alert','Audio',_F,_G,'ButtonGroup',_H,'Chart','ChatBubble',_I,_A,'CodeEditor',_J,_K,_L,_M,_N,_O,'Html','Image','Label','Map','Menu','Meter','Modal','Progress','Radio',_P,'Selector',_Q,_R,'Table',_S,_T,_U,_V,_W,'Tree','Video',_X]
AVAILABLE_COMPONENTS={_(_B):Accordion,_(_F):Avatar,_(_C):Column,_(_D):Footer,_('Grid'):Grid,_(_E):Header,_('Popup'):Modal,_('Row'):Row,_('Tabs'):Tabs,_(_V):Timeline,_('Tree'):Tree,_('Alert'):Alert,_('Audio'):Audio,_(_G):Button,_(_H):Calendar,_('Chart'):Chart,_(_I):CheckBox,_(_A):Code,_(_J):ColorPicker,_(_K):ContentCard,_(_L):DatePicker,_(_M):DateTimePicker,_(_N):Divider,_(_O):FileUpload,_('Html'):Html,_('Image'):Image,_('Radio'):Radio,_(_P):Rating,_(_Q):Slider,_(_R):Switch,_('Label'):Label,_('Table'):Table,_(_S):Terminal,_(_T):TextInput,_(_U):TextEditor,_(_W):TimePicker,_('Video'):Video,_(_X):Webcam}