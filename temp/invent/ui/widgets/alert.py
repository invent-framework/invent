_A='DEFAULT'
from invent.i18n import _
from invent.ui.core import Widget,TextProperty,ChoiceProperty,BooleanProperty,Event
from invent.ui.core.measures import PURPOSES
from invent.utils import from_markdown
from pyscript.web import button,div,p
class Alert(Widget):
	title=TextProperty(_('The title of the alert.'));text=TextProperty(_('The text to display in the alert.'));purpose=ChoiceProperty(_('The purpose of the alert.'),default_value=_A,choices=PURPOSES,group='style');dismissable=BooleanProperty(_('Whether the alert can be dismissed by the user.'),default_value=False);dismissed=Event(_('An event that is fired when the alert is dismissed.'),alert=_('The alert that was dismissed.'))
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 256 256"><path d="M236.8,188.09,149.35,36.22h0a24.76,24.76,0,0,0-42.7,0L19.2,188.09a23.51,23.51,0,0,0,0,23.72A24.35,24.35,0,0,0,40.55,224h174.9a24.35,24.35,0,0,0,21.33-12.19A23.51,23.51,0,0,0,236.8,188.09ZM222.93,203.8a8.5,8.5,0,0,1-7.48,4.2H40.55a8.5,8.5,0,0,1-7.48-4.2,7.59,7.59,0,0,1,0-7.72L120.52,44.21a8.75,8.75,0,0,1,15,0l87.45,151.87A7.59,7.59,0,0,1,222.93,203.8ZM120,144V104a8,8,0,0,1,16,0v40a8,8,0,0,1-16,0Zm20,36a12,12,0,1,1-12-12A12,12,0,0,1,140,180Z"></path></svg>'
	def on_dismissed(A):A.element.remove();A.publish('dismissed',alert=A)
	def on_purpose_changed(A):
		D='--alert-border-color';C='--alert-bg'
		if A.purpose==_A:A.element.style.pop(C,None);A.element.style[D]='var(--primary)'
		else:B=A.purpose.lower();A.element.style[C]=f"var(--{B}-light)";A.element.style[D]=f"var(--{B})"
	def on_text_changed(A):A._text_el.innerHTML=from_markdown(A.text)or'';A.element.style['display']='block'if A.text else'none'
	def on_title_changed(A):A._title_el.textContent=A.title or''
	def on_dismissable_changed(B):
		if B.dismissable:A=button('✕');A.setAttribute('aria-label',_('Dismiss'));A.addEventListener('click',lambda e:B.on_dismissed());B.element.append(A)
		else:
			for A in B.element.querySelectorAll('button'):A.remove()
	def render(A):A._title_el=p(classes=['alert-title']);A._text_el=p();B=div(A._title_el,A._text_el,classes=['invent-alert']);B.setAttribute('role','alert');return B