_E='invent-rating-readonly'
_D='invent-rating-interactive'
_C='_stars_element'
_B='style'
_A='0.5'
from invent.i18n import _
from invent.ui.core import Widget,FloatProperty,ChoiceProperty,BooleanProperty,Event
from pyscript.web import div,span
from pyscript.ffi import create_proxy
class Rating(Widget):
	value=FloatProperty(_('The current rating value (multiples of 0.5).'),default_value=.0);max_value=ChoiceProperty(_('The number of stars to display.'),default_value='5',choices=['1','3','5','10'],group=_B);step=ChoiceProperty(_('The rating step size.'),default_value=_A,choices=[_A,'1'],group=_B);read_only=BooleanProperty(_('Prevent the user from changing the rating.'),default_value=False);show_label=BooleanProperty(_('Whether to show the numeric rating value next to the stars.'),default_value=True,group=_B);changed=Event(_('Sent when the rating value is changed by the user.'),rating=_('The Rating widget whose value changed.'),value=_('The new rating value.'))
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256"><path d="M239.18,97.26A16.38,16.38,0,0,0,224.92,86l-59-4.76L143.14,26.15a16.36,16.36,0,0,0-30.27,0L90.11,81.23,31.08,86a16.46,16.46,0,0,0-9.37,28.86l45,38.83L53,211.75a16.38,16.38,0,0,0,24.5,17.82L128,198.49l50.53,31.08A16.4,16.4,0,0,0,203,211.75l-13.76-58.07,45-38.83A16.43,16.43,0,0,0,239.18,97.26Zm-15.34,5.47-48.7,42a8,8,0,0,0-2.56,7.91l14.88,62.8a.37.37,0,0,1-.17.48c-.18.14-.23.11-.38,0l-54.72-33.65a8,8,0,0,0-8.38,0L69.09,215.94c-.15.09-.19.12-.38,0a.37.37,0,0,1-.17-.48l14.88-62.8a8,8,0,0,0-2.56-7.91l-48.7-42c-.12-.1-.23-.19-.13-.5s.18-.27.33-.29l63.92-5.16A8,8,0,0,0,103,91.86l24.62-59.61c.08-.17.11-.25.35-.25s.27.08.35.25L153,91.86a8,8,0,0,0,6.75,4.92l63.92,5.16c.15,0,.24,0,.33.29S224,102.63,223.84,102.73Z"></path></svg>'
	def _click(A,value):
		B=value
		def C(event):
			event.stopPropagation()
			if not A.read_only:
				C=float(A.step)
				if A.value==B or B==C and A.value==C:A.value=.0
				else:A.value=B
				A.publish(A.changed,rating=A,value=A.value)
		return create_proxy(C)
	def _rebuild_stars(A):
		H='invent-rating-half';F='click';A._stars_element._dom_element.replaceChildren();I=int(A.max_value)
		for C in range(1,I+1):
			B=span();B.classes.add('invent-rating-star')
			if A.value>=C:B.classes.add('invent-rating-star-full')
			elif A.value>=C-.5 and A.step==_A:B.classes.add('invent-rating-star-half')
			else:B.classes.add('invent-rating-star-empty')
			G=span('★');G.classes.add('invent-rating-star-glyph');B.append(G)
			if not A.read_only:
				if A.step==_A:D=span();D.classes.add(H);D.classes.add('invent-rating-half-left');D._dom_element.addEventListener(F,A._click(C-.5));E=span();E.classes.add(H);E.classes.add('invent-rating-half-right');E._dom_element.addEventListener(F,A._click(float(C)));B.append(D);B.append(E)
				else:B._dom_element.addEventListener(F,A._click(float(C)))
			A._stars_element.append(B)
		if A.show_label:J=f"{A.value}".replace('.0','');A._value_element.textContent=f"{J}/{A.max_value}"
		else:A._value_element.textContent=''
	def on_value_changed(A):
		if hasattr(A,_C):A._rebuild_stars()
	def on_max_value_changed(A):
		if A.value>int(A.max_value):A.value=float(int(A.max_value))
		if hasattr(A,_C):A._rebuild_stars()
	def on_read_only_changed(A):
		if hasattr(A,_C):
			if A.read_only:A.element.classes.remove(_D);A.element.classes.add(_E)
			else:A.element.classes.remove(_E);A.element.classes.add(_D)
			A._rebuild_stars()
	def render(A):
		A._stars_element=span();A._stars_element.classes.add('invent-rating-stars');A._value_element=span(f"{A.value}/{A.max_value}");A._value_element.classes.add('invent-rating-value');A._message_element=span('');A._message_element.classes.add('invent-rating-message');B=div(A._stars_element,A._value_element,A._message_element,id=A.id);B.classes.add('invent-rating')
		if A.read_only:B.classes.add(_E)
		else:B.classes.add(_D)
		A._rebuild_stars();return B