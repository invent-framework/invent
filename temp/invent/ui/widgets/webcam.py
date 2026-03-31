_L='_recorder'
_K='_mode_buttons'
_J='active'
_I='invent-webcam-mode-active'
_H='mode'
_G='element'
_F='recording'
_E='_shutter_btn'
_D='style'
_C=True
_B='photo'
_A='video'
from invent.i18n import _
import time
from invent.ui.core import Widget,ChoiceProperty,BooleanProperty,Event
from pyscript.web import div,video,button,canvas
from pyscript.ffi import create_proxy
class Webcam(Widget):
	mode=ChoiceProperty(_('The current webcam mode (photo or video).'),default_value=_B,choices=[_B,_A],group=_D);show_gallery=BooleanProperty(_('Whether to show the gallery button.'),default_value=_C,group=_D);show_mode_indicator=BooleanProperty(_('Whether to show the mode/status indicators.'),default_value=_C,group=_D);photo_captured=Event(_('Sent when a photo is captured.'),webcam=_('The Webcam widget that captured the photo.'));video_recorded=Event(_('Sent when a video is recorded.'),webcam=_('The Webcam widget that recorded the video.'))
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><circle cx="128" cy="128" r="32" fill="currentColor" opacity="0.2"/><path fill="currentColor" d="M208 56H48a16 16 0 0 0-16 16v112a16 16 0 0 0 16 16h160a16 16 0 0 0 16-16V72a16 16 0 0 0-16-16m0 128H48V72h160zM128 96a32 32 0 1 0 32 32a32 32 0 0 0-32-32m0 48a16 16 0 1 1 16-16a16 16 0 0 1-16 16"/></svg>'
	def trigger(A):
		if hasattr(A,_E):A._shutter_btn.click()
	def set_mode(A,mode):
		if mode in[_B,_A]:
			A.mode=mode
			if hasattr(A,_K):A._update_mode_buttons()
	def capture_photo(A):
		if hasattr(A,'_canvas')and hasattr(A,'_video_elem'):B=A._video_elem._dom_element;C=A._canvas._dom_element;D=B.videoWidth or 1280;E=B.videoHeight or 720;C.width=D;C.height=E;F=C.getContext('2d');F.drawImage(B,0,0,D,E);A._download_canvas_as_image();A.publish('photo_captured',webcam=A)
	def _set_status(A,text):
		if not hasattr(A,'_status_elem'):return
		A._status_elem.textContent=text;A._status_elem._dom_element.textContent=text
	def _timestamp(A):return int(time.time()*1000)
	def start_recording(A):
		if hasattr(A,_L):
			if not A._recording and A._recorder.state=='inactive':A._recorded_chunks=[];A._recording=_C;A._recorder.start();A._shutter_btn.classes.add(_F);A._set_shutter_text();A._set_status('Recording...')
	def stop_recording(A):
		if hasattr(A,_L)and A._recording and A._recorder.state==_F:A._recording=False;A._recorder.stop();A._shutter_btn.classes.remove(_F);A._set_shutter_text();A._set_status('Saving video...')
	def on_mode_changed(A):
		if hasattr(A,_K):A._update_mode_buttons()
		if hasattr(A,'_mode_indicator'):A._mode_indicator.textContent=A._mode_label();A._mode_indicator._dom_element.textContent=A._mode_label()
		if hasattr(A,_E):A._set_shutter_text()
	def _mode_label(A):
		if A.mode==_A:return'Video Mode'
		return'Photo Mode'
	def _update_mode_buttons(B):
		for C in B._mode_buttons:
			A=C[_G];D=C[_H]
			if D==B.mode:A.classes.add(_I);A.classes.add(_J)
			else:A.classes.remove(_I);A.classes.remove(_J)
	def _set_shutter_text(A):
		if not hasattr(A,_E):return
		if A.mode==_A:B='Stop'if A._recording else'Record'
		else:B='Take'
		A._shutter_btn.textContent=B;A._shutter_btn._dom_element.textContent=B
	def _download_canvas_as_image(C):
		try:from pyscript import window as B;A=B.document.createElement('a');A.href=C._canvas._dom_element.toDataURL('image/jpeg');A.download=f"photo-{C._timestamp()}.jpg";B.document.body.appendChild(A);A.click();B.document.body.removeChild(A)
		except Exception as D:print(f"Error downloading photo: {D}")
	def _on_shutter_click(A,event):
		if A.mode==_B:A.capture_photo()
		elif A._recording:A.stop_recording()
		else:A.start_recording()
	def _setup_webcam_stream(A):
		C='ideal'
		try:
			from pyscript import window as D;B=D.navigator
			if not B.mediaDevices:print('Camera not supported in this browser');return
			E={_A:{'width':{C:1280},'height':{C:720},'facingMode':'user'},'audio':_C}
			async def F():
				try:C=await B.mediaDevices.getUserMedia(E);A._video_elem.srcObject=C;A._set_status('Webcam ready');A._setup_recorder(C)
				except Exception as D:print(f"Camera access denied or error: {D}");A._set_status('Camera access denied')
			import asyncio as G;G.create_task(F())
		except Exception as H:print(f"Error setting up webcam: {H}")
	def _setup_recorder(A,stream):
		try:
			from pyscript import window as B
			def D(event):
				B=event
				if B.data.size>0:A._recorded_chunks.append(B.data)
			def E(event):
				if not A._recorded_chunks:A._set_status('No video captured');return
				E=B.Blob.new(A._recorded_chunks,{'type':'video/webm'});C=B.document.createElement('a');D=B.URL.createObjectURL(E);C.href=D;C.download=f"video-{A._timestamp()}.webm";B.document.body.appendChild(C);C.click();B.document.body.removeChild(C);B.URL.revokeObjectURL(D);A.publish('video_recorded',webcam=A);A._set_status('Video saved')
			C=B.MediaRecorder.new(stream);C.addEventListener('dataavailable',create_proxy(D));C.addEventListener('stop',create_proxy(E));A._recorder=C;A._recording=False;A._recorded_chunks=[]
		except Exception as F:print(f"Error setting up recorder: {F}")
	def render(A):
		N='mode-btn';M='invent-webcam-mode-btn';L='click';A._canvas=canvas();A._canvas.width=1280;A._canvas.height=720;A._canvas.style.display='none';A._video_elem=video();A._video_elem.id=f"{A.id}-video";A._video_elem.autoplay=_C;A._video_elem.muted=_C;A._video_elem.classes.add('invent-webcam-video');F=div(A._video_elem);F.classes.add('invent-webcam-box');F.classes.add('webcam-box');B=button('Photo');B.id=f"{A.id}-photo-btn";B.classes.add(M);B.classes.add(N);B.classes.add(_I);B.classes.add(_J);B._dom_element.addEventListener(L,create_proxy(lambda e:A.set_mode(_B)));C=button('Video');C.id=f"{A.id}-video-btn";C.classes.add(M);C.classes.add(N);C._dom_element.addEventListener(L,create_proxy(lambda e:A.set_mode(_A)));A._mode_buttons=[{_G:B,_H:_B},{_G:C,_H:_A}];G=div(B,C);G.classes.add('invent-webcam-modes');G.classes.add('modes');A._shutter_btn=button('Take');A._shutter_btn.id=f"{A.id}-shutter";A._shutter_btn.classes.add('invent-webcam-shutter');A._shutter_btn.classes.add('shutter');A._shutter_btn._dom_element.addEventListener(L,create_proxy(A._on_shutter_click));A._set_shutter_text();H=div(A._shutter_btn);H.classes.add('invent-webcam-shutter-container');H.classes.add('shutter-container');D=button('Gallery');D.id=f"{A.id}-gallery-btn";D.classes.add('invent-webcam-gallery-btn');D.classes.add('small-btn');I=div(D)if A.show_gallery else div();I.classes.add('invent-webcam-gallery');I.classes.add('gallery');J=div(G,H,I);J.classes.add('invent-webcam-actions');J.classes.add('actions');A._status_elem=div('Initializing camera...');A._status_elem.id=f"{A.id}-status";A._status_elem.classes.add('invent-webcam-status');A._mode_indicator=div(A._mode_label());A._mode_indicator.id=f"{A.id}-mode-indicator";A._mode_indicator.classes.add('mode-selection');A._mode_indicator.classes.add('invent-webcam-mode-indicator');E=div(A._status_elem,A._mode_indicator);E.classes.add('invent-webcam-indicators');E.classes.add('indicators')
		if not A.show_mode_indicator:E.classes.add('hidden')
		K=div(A._canvas,F,J,E,id=A.id);K.classes.add('invent-webcam');K.classes.add('webcam-container');A._setup_webcam_stream();return K