_A='CIRCLE'
from pyscript import web
from invent.i18n import _
from invent.ui.core.measures import TSHIRT_SIZES,MEDIUM
from invent.ui.core import Widget,TextProperty,ChoiceProperty,Event
from pyscript.web import figure,img
from pyscript.ffi import create_proxy
_DEFAULT_AVATAR_IMAGE="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23585858' viewBox='0 0 256 256'%3E%3Cpath d='M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216ZM80,108a12,12,0,1,1,12,12A12,12,0,0,1,80,108Zm96,0a12,12,0,1,1-12-12A12,12,0,0,1,176,108Zm-1.07,48c-10.29,17.79-27.4,28-46.93,28s-36.63-10.2-46.92-28a8,8,0,1,1,13.84-8c7.47,12.91,19.21,20,33.08,20s25.61-7.1,33.07-20a8,8,0,0,1,13.86,8Z'%3E%3C/path%3E%3C/svg%3E%0A"
class Avatar(Widget):
	image=TextProperty(_('The URL of the avatar image.'),default_value=_DEFAULT_AVATAR_IMAGE);shape=ChoiceProperty(_('The shape of the avatar.'),default_value=_A,choices=[_A,'ROUNDED','SQUARE'],group='style');size=ChoiceProperty(_('The size of the avatar.'),default_value=MEDIUM,choices=TSHIRT_SIZES,group='style');name=TextProperty(_('The name of the person or entity represented by the avatar.'),default_value=None);press=Event(_('Sent when the avatar is pressed.'),avatar=_('The avatar that was clicked.'))
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256"><path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216ZM80,108a12,12,0,1,1,12,12A12,12,0,0,1,80,108Zm96,0a12,12,0,1,1-12-12A12,12,0,0,1,176,108Zm-1.07,48c-10.29,17.79-27.4,28-46.93,28s-36.63-10.2-46.92-28a8,8,0,1,1,13.84-8c7.47,12.91,19.21,20,33.08,20s25.61-7.1,33.07-20a8,8,0,0,1,13.86,8Z"></path></svg>'
	def click(A,event):A.publish('press',avatar=A)
	def render(A):C=img();C.src=A.image if A.image else'';C.alt=A.name if A.name else'';C.title=A.name if A.name else'';B=figure(C);B.classes.add('invent-avatar');B.classes.add(f"invent-avatar--{A.shape.lower()}");B.classes.add(f"invent-avatar--{A.size.lower()}");B.addEventListener('click',create_proxy(A.click));return B
	def on_image_changed(A):A.element.find('img')[0].src=A.image if A.image else''
	def on_name_changed(A):B=A.element.find('img')[0];C=A.name if A.name else'';B.alt=C;B.title=C
	def on_shape_changed(A):
		for B in('circle','rounded','square'):A.element.classes.remove(f"invent-avatar--{B}")
		A.element.classes.add(f"invent-avatar--{A.shape.lower()}")
	def on_size_changed(A):
		for B in(A.lower()for A in TSHIRT_SIZES if A is not None):A.element.classes.remove(f"invent-avatar--{B}")
		A.element.classes.add(f"invent-avatar--{A.size.lower()}")