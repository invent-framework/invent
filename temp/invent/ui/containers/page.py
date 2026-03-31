_G='--page-transition-duration'
_F='style'
_E='MEDIUM'
_D='None'
_C='NONE'
_B=None
_A='display'
from pyscript.ffi import create_proxy
from pyscript.web import page as document
from.column import Column
from invent.i18n import _
from invent.ui.core import ChoiceProperty,TextProperty
from invent.utils import is_micropython
_SPEED_VARS={'SLOW':'--transition-speed-slow',_E:'--transition-speed','FAST':'--transition-speed-fast'}
class Page(Column):
	background=TextProperty(_("The page's background (colour, image or gradient)."),default_value=_B,group=_F);transition=ChoiceProperty(_('The transition effect when showing or hiding the page.'),default_value=_C,choices=[_C,'FADE','SLIDE','ZOOM','CONVEX','CONCAVE'],group=_F);transition_speed=ChoiceProperty(_('The speed of the page transition.'),default_value=_E,choices=['SLOW',_E,'FAST'],group=_F)
	def _apply_background(A):
		B='background'
		if A.background:document.body.style[B]=A.background
		else:document.body.style[B]=_B
	def _apply_transition_speed(A):B=_SPEED_VARS[A.transition_speed];A.element.style[_G]=f"var({B})"
	def _animate(A,cls,on_done):
		B='animationend';A.element.classes.add(cls)
		def C(event):
			A.element.classes.remove(cls);A.element.removeEventListener(B,A._animation_handler)
			if not is_micropython:A._animation_handler.destroy()
			A._animation_handler=_B;on_done()
		A._animation_handler=create_proxy(C);A.element.addEventListener(B,A._animation_handler)
	def on_background_changed(A):
		if A.element.style[_A]!=_D:A._apply_background()
	def on_transition_speed_changed(A):A._apply_transition_speed()
	def render(B):A=super().render();A.classList.add('container');A.style[_A]=_D;C=_SPEED_VARS[B.transition_speed];A.style[_G]=f"var({C})";return A
	def show(A):
		A._apply_background();A.element.style[_A]='flex'
		if A.transition!=_C:B=f"invent-page--entering-{A.transition.lower()}";A._animate(B,lambda:_B)
	def hide(A):
		if A.transition==_C:A.element.style[_A]=_D;return
		B=f"invent-page--leaving-{A.transition.lower()}"
		def C():A.element.style[_A]=_D
		A._animate(B,C)