from invent.i18n import _
from invent.ui.core import Widget,TextProperty,Event
from pyscript.web import audio
from pyscript.ffi import create_proxy
class Audio(Widget):
	source=TextProperty(_('The audio source file to play.'));playing=Event(_('Sent when the audio starts to play.'));paused=Event(_('Sent when the audio is paused.'),position=_('The pause position in seconds.'));position_changed=Event(_('Sent when the position in the audio is changed.'),position=_('The new position in seconds.'))
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><path fill="currentColor" d="M155.51 24.81a8 8 0 0 0-8.42.88L77.25 80H32a16 16 0 0 0-16 16v64a16 16 0 0 0 16 16h45.25l69.84 54.31A8 8 0 0 0 160 224V32a8 8 0 0 0-4.49-7.19M32 96h40v64H32Zm112 111.64l-56-43.55V91.91l56-43.55Zm54-106.08a40 40 0 0 1 0 52.88a8 8 0 0 1-12-10.58a24 24 0 0 0 0-31.72a8 8 0 0 1 12-10.58M248 128a79.9 79.9 0 0 1-20.37 53.34a8 8 0 0 1-11.92-10.67a64 64 0 0 0 0-85.33a8 8 0 1 1 11.92-10.67A79.83 79.83 0 0 1 248 128"/></svg>'
	def play(A):A.element.play()
	def pause(A):A.element.pause()
	def reset(A):A.set_position(0)
	def stop(A):A.pause();A.reset()
	def set_position(A,position):B=position;A.element.currentTime=B;A.publish(A.position_changed,position=B)
	def on_play(A,event):A.publish(A.playing)
	def on_pause(A,event):A.publish(A.paused,position=event.target.currentTime)
	def on_source_changed(A):A.element.setAttribute('src',A.source)
	def render(B):C='controls';A=audio(id=B.id);A.setAttribute(C,C);A.addEventListener('play',create_proxy(B.on_play));A.addEventListener('pause',create_proxy(B.on_pause));return A