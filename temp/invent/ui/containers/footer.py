from invent.i18n import _
from.row import Row
from..core.property import BooleanProperty
class Footer(Row):
	sticky=BooleanProperty(_('Whether the footer should be sticky (i.e. stay at the bottom of the page even when the user scrolls up).'),default_value=False)
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="currentColor" viewBox="0 0 256 256"><path transform="scale(1,-1) translate(0,-256)" d="M216,40H40A16,16,0,0,0,24,56V200a16,16,0,0,0,16,16H216a16,16,0,0,0,16-16V56A16,16,0,0,0,216,40Zm0,16V88H40V56Zm0,144H40V104H216v96Z"></path></svg>'
	def on_sticky_changed(A):
		B='invent-footer--sticky'
		if A.sticky:A.element.classes.add(B)
		else:A.element.classes.remove(B)