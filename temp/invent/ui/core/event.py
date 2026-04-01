import invent
from invent.i18n import _
class Event:
	def __init__(A,description=None,**B):A.description=description;A.content=B;A._event_name=None
	def __set_name__(A,owner,name):A._event_name=name
	def create_message(A,source,**C):
		for B in C:
			if B not in A.content:raise ValueError(_('Unknown field in event {event}: ').format(event=A._event_name)+B)
		for B in A.content:
			if B not in C:raise ValueError(_('Field missing from event {event}:').format(event=A._event_name)+B)
		C['source']=source;return invent.Message(A._event_name,**C)
	def as_dict(A):return{'description':A.description,'content':A.content}