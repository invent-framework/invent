_O='DEFAULT'
_N='rounded'
_M='datetime'
_L='alt'
_K='src'
_J='banner-image'
_I='publish-end'
_H='--card-border-color'
_G='end'
_F='start'
_E='banner'
_D='avatar'
_C='style'
_B=None
_A='square'
from invent.i18n import _
from..containers.column import Column
from pyscript.ffi import create_proxy
from pyscript.web import article,header,img,h3,time,footer,div
from invent.ui.core import Widget,TextProperty,DatetimeProperty,ChoiceProperty,Event
from invent.ui.core.measures import PURPOSES
from invent.utils import humanise_timestamp
CARD_SHAPES=[_N,_A]
IMAGE_POSITIONS=[_D,_E]
PUBLISH_POSITIONS=[_F,_G]
class ContentCard(Widget):
	def __init__(B,**A):
		C='children';B.children=Column()
		if C in A:
			for D in A.pop(C):B.children.append(D)
		super().__init__(**A)
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><path fill="currentColor" d="M200 112a8 8 0 0 1-8 8h-40a8 8 0 0 1 0-16h40a8 8 0 0 1 8 8m-8 24h-40a8 8 0 0 0 0 16h40a8 8 0 0 0 0-16m40-80v144a16 16 0 0 1-16 16H40a16 16 0 0 1-16-16V56a16 16 0 0 1 16-16h176a16 16 0 0 1 16 16m-16 144V56H40v144zm-80.26-34a8 8 0 1 1-15.5 4c-2.63-10.26-13.06-18-24.25-18s-21.61 7.74-24.25 18a8 8 0 1 1-15.5-4a39.84 39.84 0 0 1 17.19-23.34a32 32 0 1 1 45.12 0a39.76 39.76 0 0 1 17.2 23.34ZM96 136a16 16 0 1 0-16-16a16 16 0 0 0 96 16"/></svg>'
	published_at=DatetimeProperty(_('The publication date and time relating to the content.'),default_value=_B);image=TextProperty(_('The image/icon associated with the content.'),default_value=_B);title=TextProperty(_('The title related to the content.'),default_value=_B);shape=ChoiceProperty(_('The shape of the content card.'),choices=CARD_SHAPES,default_value=_N,group=_C);image_position=ChoiceProperty(_('The position of the image on the content card.'),choices=IMAGE_POSITIONS,default_value=_D,group=_C);publish_position=ChoiceProperty(_('The position of the publication timestamp on the content card.'),choices=PUBLISH_POSITIONS,default_value=_F,group=_C);purpose=ChoiceProperty(_("The card's purpose."),default_value=_O,choices=PURPOSES,group=_C);pressed=Event(_('Sent when the card is pressed.'))
	def click(A,event):A.publish(A.pressed)
	def render(A):
		B=article(style={_H:f"var(--primary)"});B.classes.add('invent-card')
		if A.shape==_A:B.classes.add(_A)
		if A.publish_position==_G:B.classes.add(_I)
		if A.image_position==_E:B.classes.add(_J)
		A._banner=img();A._banner.setAttribute(_K,A.image or'');A._banner.setAttribute(_L,A.title or'');B.append(A._banner);A._header=header();A._avatar=img();A._avatar.setAttribute(_K,A.image or'');A._avatar.setAttribute(_L,A.title or'');A._header.append(A._avatar);C=div();A._h3=h3();A._h3.textContent=A.title or'';C.append(A._h3);D=A.published_at.isoformat()if A.published_at else'';E=humanise_timestamp(A.published_at)if A.published_at else'';A._header_time=time();A._header_time.setAttribute(_M,D);A._header_time.textContent=E;C.append(A._header_time);A._header.append(C);B.append(A._header);B.append(A.children.element);A._footer_time=time();A._footer_time.setAttribute(_M,D);A._footer_time.textContent=E;F=footer();F.append(A._footer_time);B.append(F);B.addEventListener('click',create_proxy(A.click));A._update_header_visibility();return B
	def _update_header_visibility(A):B=bool(A.image and A.image_position==_D)or bool(A.title)or bool(A.published_at and A.publish_position==_F);A._header.style.display=''if B else'none'
	def on_title_changed(A):
		A._h3.textContent=A.title or''
		for B in(A._banner,A._avatar):B.setAttribute(_L,A.title or'')
		A._update_header_visibility()
	def on_image_changed(A):
		for B in(A._banner,A._avatar):B.setAttribute(_K,A.image or'')
		A._update_header_visibility()
	def on_image_position_changed(A):
		if A.image_position==_E:A.element.classes.add(_J)
		else:A.element.classes.remove(_J)
		A._update_header_visibility()
	def on_published_at_changed(A):
		C=A.published_at.isoformat()if A.published_at else'';D=humanise_timestamp(A.published_at)if A.published_at else''
		for B in(A._header_time,A._footer_time):B.setAttribute(_M,C);B.textContent=D
		A._update_header_visibility()
	def on_publish_position_changed(A):
		if A.publish_position==_G:A.element.classes.add(_I)
		else:A.element.classes.remove(_I)
		A._update_header_visibility()
	def on_shape_changed(A):
		if A.shape==_A:A.element.classes.add(_A)
		else:A.element.classes.remove(_A)
	def on_purpose_changed(A):
		C='--card-bg'
		if A.purpose==_O:A.element.style.pop(C,_B);A.element.style[_H]='var(--primary)'
		else:B=A.purpose.lower();A.element.style[C]=f"var(--{B}-light)";A.element.style[_H]=f"var(--{B})"