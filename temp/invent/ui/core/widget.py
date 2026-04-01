import invent
from invent.i18n import _
from.component import Component
from.property import TextProperty
class Widget(Component):
	channel=TextProperty(_('A comma separated list of channels to which the widgetbroadcasts.'),default_value=None)
	def __init__(A,*F,**D):
		super().__init__(*F,**D)
		if A.channel is None:A.channel=A.id
		G=type(A).events()
		for B in D:
			if B in G:
				C=D[B]
				if callable(C):invent.subscribe(handler=C,to_channel=A.channel,when_subject=B)
				elif isinstance(C,list):
					for E in C:
						if callable(E):invent.subscribe(handler=E,to_channel=A.channel,when_subject=B)
	def publish(A,event_instance,**B):
		if A.channel is not None:C=[A.strip()for A in A.channel.split(',')if A.strip()];D=event_instance.create_message(source=A,**B);invent.publish(D,to_channel=C)