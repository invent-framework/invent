_A='video'
import re
from invent.i18n import _
from invent.ui.core import Widget,TextProperty,Event
from pyscript.web import div,video
from pyscript.ffi import create_proxy
_YOUTUBE_ID_RE=re.compile('v=([a-zA-Z0-9_-]+)')
_VIMEO_ID_RE=re.compile('vimeo\\.com/(\\d+)')
_IFRAME_ALLOW='accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture'
def _hosted_embed_url(source):
	A=source
	if'youtube'in A or'youtu.be'in A:B=_YOUTUBE_ID_RE.search(A);return'https://www.youtube.com/embed/{}'.format(B.group(1))if B else None
	if'vimeo'in A:B=_VIMEO_ID_RE.search(A);return'https://player.vimeo.com/video/{}'.format(B.group(1))if B else None
class Video(Widget):
	source=TextProperty(_('The video source file to play.'));playing=Event(_('Sent when the video starts to play.'),video=_('The video source playing.'));paused=Event(_('Sent when the video is paused.'),video=_('The video source paused.'),position=_('The pause position in seconds.'));position_changed=Event(_('Sent when the position in the video is changed.'),video=_('The video source that has been affected.'),position=_('The new position in seconds.'))
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="m164.44 105.34l-48-32A8 8 0 0 0 104 80v64a8 8 0 0 0 12.44 6.66l48-32a8 8 0 0 0 0-13.32M120 129.05V95l25.58 17ZM216 40H40a16 16 0 0 0-16 16v112a16 16 0 0 0 16 16h176a16 16 0 0 0 16-16V56a16 16 0 0 0-16-16m0 128H40V56h176zm16 40a8 8 0 0 1-8 8H32a8 8 0 0 1 0-16h192a8 8 0 0 1 8 8"/></svg>'
	def play(A):A.element.querySelector(_A).play()
	def pause(A):A.element.querySelector(_A).pause()
	def reset(A):A.set_position(0)
	def stop(A):A.pause();A.reset()
	def set_position(A,position):B=position;C=A.element.querySelector(_A);C.currentTime=B;A.publish(A.position_changed,video=A.source,position=B)
	def on_play(A,event):A.publish(A.playing,video=A.source)
	def on_pause(A,event):A.publish(A.paused,video=A.source,position=event.target.currentTime)
	def _build_native(B):
		C='controls';A=video();A.setAttribute(C,C)
		if B.source:A.setAttribute('src',B.source)
		A.addEventListener('play',create_proxy(B.on_play));A.addEventListener('pause',create_proxy(B.on_pause));return A
	def _build_hosted(B,embed_url):A=div();A.setAttribute('style','position:relative;padding-bottom:56.25%;height:0;overflow:hidden;');A.innerHTML=f'<iframe src="{embed_url}" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" allowfullscreen allow="{_IFRAME_ALLOW}"></iframe>';return A
	def _inject(A):A.element.innerHTML='';B=_hosted_embed_url(A.source)if A.source else None;C=A._build_hosted(B)if B else A._build_native();A.element.append(C)
	def on_source_changed(A):A._inject()
	def render(A):B=div(id=A.id);return B