_A='invent-bubble'
from datetime import datetime
from invent.i18n import _
from invent.utils import from_markdown,contrast_colours,humanise_timestamp
from invent.ui.core import Widget,TextProperty,Event,DatetimeProperty,ChoiceProperty
from pyscript import web
_DEFAULT_AUTHOR_IMAGE="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='%23585858' viewBox='0 0 256 256'%3E%3Cpath d='M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216ZM80,108a12,12,0,1,1,12,12A12,12,0,0,1,80,108Zm96,0a12,12,0,1,1-12-12A12,12,0,0,1,176,108Zm-1.07,48c-10.29,17.79-27.4,28-46.93,28s-36.63-10.2-46.92-28a8,8,0,1,1,13.84-8c7.47,12.91,19.21,20,33.08,20s25.61-7.1,33.07-20a8,8,0,0,1,13.86,8Z'%3E%3C/path%3E%3C/svg%3E%0A"
class ChatBubble(Widget):
	author_name=TextProperty(_('The name of the author of the message.'),default_value=None);author_image=TextProperty(_("The URL of the author's image."),default_value=_DEFAULT_AUTHOR_IMAGE);timestamp=DatetimeProperty(_('The time when the message was sent.'),default_value=None);shade=TextProperty(_('The colour of the chat bubble as a CSS colour string.'),default_value=None);content=TextProperty(_('The content of the message.'),min_length=1);direction=ChoiceProperty(_('The direction of broadcast. Sent or received. Determines the alignment of the chat bubble.'),choices=['sent','received'],default_value='sent');pressed=Event(_('An event that is fired when the chat bubble is pressed.'),author_name=str,author_image=str,timestamp=datetime,content=str)
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="#currentColor" viewBox="0 0 256 256"><path d="M216,48H40A16,16,0,0,0,24,64V224a15.85,15.85,0,0,0,9.24,14.5A16.13,16.13,0,0,0,40,240a15.89,15.89,0,0,0,10.25-3.78l.09-.07L83,208H216a16,16,0,0,0,16-16V64A16,16,0,0,0,216,48ZM40,224h0ZM216,192H80a8,8,0,0,0-5.23,1.95L40,224V64H216ZM88,112a8,8,0,0,1,8-8h64a8,8,0,0,1,0,16H96A8,8,0,0,1,88,112Zm0,32a8,8,0,0,1,8-8h64a8,8,0,1,1,0,16H96A8,8,0,0,1,88,144Z"></path></svg>'
	def update_bubble(A):
		if not A.content:return
		A.element.replaceChildren();A.element.classes.clear();A.element.classes.add(_A);A.element.classes.add(A.direction)
		if A.shade:C=contrast_colours(A.shade);A.element.style['--bubble-bg']=A.shade;A.element.style['--bubble-text']=C['text'];A.element.style['--bubble-link']=C['link']
		if A.author_image:G=web.img(src=A.author_image,alt=A.author_name,width='40',height='40');A.element.append(G)
		B=web.div(classes=['invent-bubble-body'])
		if A.author_name:H=web.header(web.strong(A.author_name));B.append(H)
		D=web.div();D.innerHTML=from_markdown(A.content);B.append(D)
		if A.timestamp:E=web.footer();F=web.time(humanise_timestamp(A.timestamp));F.setAttribute('datetime',A.timestamp.isoformat());E.append(F);B.append(E)
		A.element.append(B)
	on_author_name_changed=update_bubble;on_author_image_changed=update_bubble;on_timestamp_changed=update_bubble;on_content_changed=update_bubble;on_direction_changed=update_bubble;on_shade_changed=update_bubble
	def render(A):B=web.div(classes=[_A]);B.addEventListener('click',lambda event:A.publish(A.pressed,author_name=A.author_name,author_image=A.author_image,timestamp=A.timestamp,content=A.content));return B