_D='keypress'
_C='No page with the id: {page_id}'
_B='keydown'
_A=None
from pyscript import document
from pyscript.ffi import create_proxy
from pyscript.web import page as dom
import invent
from.i18n import load_translations,_
__all__=['App']
__app__=_A
class App:
	def __init__(A,*B,name='',media_root='.',icon=_A,description=_A,author=_A,license=_A,pages=_A,native=False,theme='default.css'):
		C=pages;global __app__
		if not __app__:__app__=A
		if not name:raise ValueError(_('An app must have a name.'))
		A.name=name;A.icon=icon;A.description=description;A.author=author;A.license=license;A._pages=[];A._page_lookup_table={};A._current_page=_A
		if B:A.append(*B)
		if C:A.append(*C)
		if native:dom.body.classes.add('app-view')
		invent.set_media_root(media_root);invent.set_theme(theme);document.addEventListener(_B,create_proxy(A._on_keydown));document.addEventListener('keyup',create_proxy(A._on_keyup))
	@property
	def pages(self):return self._pages
	def append(B,*C):
		for A in C:
			if A.id in B._page_lookup_table:raise ValueError(_('A page with the id {name} already exists.').format(name=A.id))
			B._pages.append(A);B._page_lookup_table[A.id]=A
	def remove(A,*C):
		for B in C:
			if B in A._page_lookup_table:D=A._page_lookup_table[B];A._pages.remove(D);del A._page_lookup_table[B]
			else:raise KeyError(_(_C).format(page_id=B))
	def as_dict(A):return dict(name=A.name,icon=A.icon,description=A.description,author=A.author,license=A.license,pages=[A.as_dict()for A in A.pages])
	@classmethod
	def app(A):global __app__;return __app__
	def get_page(B,page_id):
		A=page_id
		if A in B._page_lookup_table:return B._page_lookup_table[A]
		else:raise KeyError(_(_C).format(page_id=A))
	def show_page(A,page_id):
		B=A.get_page(page_id);B.show()
		if A._current_page and A._current_page!=B:A._current_page.hide()
		A._current_page=B
	def _get_key_event_details(B,event):A=event;return{'key':A.key,'code':A.code,'shift':A.shiftKey,'ctrl':A.ctrlKey,'alt':A.altKey,'meta':A.metaKey,'repeat':A.repeat}
	def _on_keydown(A,event):invent.publish(invent.Message(subject=_B,key=A._get_key_event_details(event)),to_channel=_D)
	def _on_keyup(A,event):invent.publish(invent.Message(subject='keyup',key=A._get_key_event_details(event)),to_channel=_D)
	def go(A):
		dom.title=A.name;load_translations()
		if A.pages:
			for B in A.pages:dom.append(B.element._dom_element)
			A.show_page(A.pages[0].id)
		else:raise ValueError(_('No pages in the app!'))