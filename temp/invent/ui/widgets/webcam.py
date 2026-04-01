_K='_recorder'
_J='_mode_buttons'
_I='active'
_H='invent-webcam-mode-active'
_G='mode'
_F='element'
_E='recording'
_D='_shutter_btn'
_C=True
_B='photo'
_A='video'
from invent.i18n import _
import time
from invent.ui.core import Widget,ChoiceProperty,BooleanProperty,Event
from pyscript.web import div,video,button,canvas
from pyscript.ffi import create_proxy
class Webcam(Widget):
	mode=ChoiceProperty(_('The current webcam mode (photo or video).'),default_value=_B,choices=[_B,_A],group='style');show_mode_indicator=BooleanProperty(_('Whether to show the mode/status indicators.'),default_value=_C,group='style');photo_captured=Event(_('Sent when a photo is captured.'),webcam=_('The Webcam widget that captured the photo.'));video_recorded=Event(_('Sent when a video is recorded.'),webcam=_('The Webcam widget that recorded the video.'))
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><circle cx="128" cy="128" r="32" fill="currentColor" opacity="0.2"/><path fill="currentColor" d="M208 56H48a16 16 0 0 0-16 16v112a16 16 0 0 0 16 16h160a16 16 0 0 0 16-16V72a16 16 0 0 0-16-16m0 128H48V72h160zM128 96a32 32 0 1 0 32 32a32 32 0 0 0-32-32m0 48a16 16 0 1 1 16-16a16 16 0 0 1-16 16"/></svg>'
	def trigger(A):
		if hasattr(A,_D):A._shutter_btn.click()
	def set_mode(A,mode):
		if mode in[_B,_A]:
			A.mode=mode
			if hasattr(A,_J):A._update_mode_buttons()
	def capture_photo(A):
		if hasattr(A,'_canvas')and hasattr(A,'_video_elem'):B=A._video_elem._dom_element;C=A._canvas._dom_element;D=B.videoWidth or 1280;E=B.videoHeight or 720;C.width=D;C.height=E;F=C.getContext('2d');F.drawImage(B,0,0,D,E);A._download_canvas_as_image();A.publish(A.photo_captured,webcam=A)
	def _set_status(A,text):
		if not hasattr(A,'_status_elem'):return
		A._status_elem.textContent=text;A._status_elem._dom_element.textContent=text
	def _timestamp(A):return int(time.time()*1000)
	def start_recording(A):
		if hasattr(A,_K):
			if not A._recording and A._recorder.state=='inactive':A._recorded_chunks=[];A._recording=_C;A._recorder.start();A._shutter_btn.classes.add(_E);A._set_shutter_text();A._set_status('Recording...')
	def stop_recording(A):
		if hasattr(A,_K)and A._recording and A._recorder.state==_E:A._recording=False;A._recorder.stop();A._shutter_btn.classes.remove(_E);A._set_shutter_text();A._set_status('Saving video...')
	def on_mode_changed(A):
		if hasattr(A,_J):A._update_mode_buttons()
		if hasattr(A,'_mode_indicator'):A._mode_indicator.textContent=A._mode_label();A._mode_indicator._dom_element.textContent=A._mode_label()
		if hasattr(A,_D):A._set_shutter_text()
	def _mode_label(A):
		if A.mode==_A:return'Video Mode'
		return'Photo Mode'
	def _update_mode_buttons(B):
		for C in B._mode_buttons:
			A=C[_F];D=C[_G]
			if D==B.mode:A.classes.add(_H);A.classes.add(_I)
			else:A.classes.remove(_H);A.classes.remove(_I)
	def _set_shutter_text(A):
		if not hasattr(A,_D):return
		if A.mode==_A:B='Stop'if A._recording else'Record'
		else:B='Take'
		A._shutter_btn.textContent=B;A._shutter_btn._dom_element.textContent=B
	def _download_canvas_as_image(B):
		try:from pyscript import window as C;A=C.document.createElement('a');A.href=B._canvas._dom_element.toDataURL('image/jpeg');A.download=f"photo-{B._timestamp()}.jpg";A.click()
		except Exception as D:print(f"Error downloading photo: {D}")
	def _on_shutter_click(A,event):
		if A.mode==_B:A.capture_photo()
		elif A._recording:A.stop_recording()
		else:A.start_recording()
	def _setup_webcam_stream(A):
		E='ideal'
		try:
			from pyscript import window as B;C=B.navigator
			if not C.mediaDevices:print('Camera not supported in this browser');return
			D=max(320,min(int(B.innerWidth or 1280),1280));F=max(240,int(D*9/16));G={_A:{'width':{E:D},'height':{E:F},'facingMode':'user'},'audio':_C}
			async def H():
				try:B=await C.mediaDevices.getUserMedia(G);A._video_elem.srcObject=B;A._set_status('Webcam ready');A._setup_recorder(B)
				except Exception as D:print(f"Camera access denied or error: {D}");A._set_status('Camera access denied')
			import asyncio as I;I.create_task(H())
		except Exception as J:print(f"Error setting up webcam: {J}")
	def _setup_recorder(A,stream):
		try:
			from pyscript import window as B
			def D(event):
				B=event
				if B.data.size>0:A._recorded_chunks.append(B.data)
			def E(event):
				if not A._recorded_chunks:A._set_status('No video captured');return
				E=B.Blob.new(A._recorded_chunks,{'type':'video/webm'});C=B.document.createElement('a');D=B.URL.createObjectURL(E);C.href=D;C.download=f"video-{A._timestamp()}.webm";C.click();B.URL.revokeObjectURL(D);A.publish(A.video_recorded,webcam=A);A._set_status('Video saved')
			C=B.MediaRecorder.new(stream);C.addEventListener('dataavailable',create_proxy(D));C.addEventListener('stop',create_proxy(E));A._recorder=C;A._recording=False;A._recorded_chunks=[]
		except Exception as F:print(f"Error setting up recorder: {F}")
	def render(A):
		L='mode-btn';K='invent-webcam-mode-btn';J='click';A._canvas=canvas();A._canvas.width=1;A._canvas.height=1;A._canvas.style.display='none';A._video_elem=video();A._video_elem.id=f"{A.id}-video";A._video_elem.autoplay=_C;A._video_elem.muted=_C;A._video_elem.classes.add('invent-webcam-video')
		def M(event):B=A._video_elem._dom_element;C=A._canvas._dom_element;D=B.videoWidth or 1280;E=B.videoHeight or 720;C.width=D;C.height=E
		A._video_elem._dom_element.addEventListener('loadedmetadata',create_proxy(M));E=div(A._video_elem);E.classes.add('invent-webcam-box');E.classes.add('webcam-box');B=button('Photo');B.id=f"{A.id}-photo-btn";B.classes.add(K);B.classes.add(L);B.classes.add(_H);B.classes.add(_I);B._dom_element.addEventListener(J,create_proxy(lambda e:A.set_mode(_B)));C=button('Video');C.id=f"{A.id}-video-btn";C.classes.add(K);C.classes.add(L);C._dom_element.addEventListener(J,create_proxy(lambda e:A.set_mode(_A)));A._mode_buttons=[{_F:B,_G:_B},{_F:C,_G:_A}];F=div(B,C);F.classes.add('invent-webcam-modes');F.classes.add('modes');A._shutter_btn=button('Take');A._shutter_btn.id=f"{A.id}-shutter";A._shutter_btn.classes.add('invent-webcam-shutter');A._shutter_btn.classes.add('shutter');A._shutter_btn._dom_element.addEventListener(J,create_proxy(A._on_shutter_click));A._set_shutter_text();G=div(A._shutter_btn);G.classes.add('invent-webcam-shutter-container');G.classes.add('shutter-container');H=div(F,G);H.classes.add('invent-webcam-actions');H.classes.add('actions');A._status_elem=div('Initializing camera...');A._status_elem.id=f"{A.id}-status";A._status_elem.classes.add('invent-webcam-status');A._mode_indicator=div(A._mode_label());A._mode_indicator.id=f"{A.id}-mode-indicator";A._mode_indicator.classes.add('mode-selection');A._mode_indicator.classes.add('invent-webcam-mode-indicator');D=div(A._status_elem,A._mode_indicator);D.classes.add('invent-webcam-indicators');D.classes.add('indicators')
		if not A.show_mode_indicator:D.classes.add('hidden')
		I=div(A._canvas,E,H,D,id=A.id);I.classes.add('invent-webcam');I.classes.add('webcam-container');A._setup_webcam_stream();return I