_J='element'
_I='_recorder'
_H='_mode_indicator'
_G=False
_F='recording'
_E='_shutter_btn'
_D=True
_C='video'
_B='photo'
_A='both'
from invent.i18n import _
import time
from invent.ui.core import Widget,ChoiceProperty,BooleanProperty,Event
from pyscript.web import div,video,button,canvas
from pyscript.ffi import create_proxy
class Webcam(Widget):
	mode=ChoiceProperty(_('Webcam mode: photo, video, or both.'),default_value=_A,choices=[_B,_C,_A],group='style');show_mode_indicator=BooleanProperty(_('Whether to show the mode/status indicators.'),default_value=_D,group='style');photo_captured=Event(_('Sent when a photo is captured.'),webcam=_('The Webcam widget that captured the photo.'));video_recorded=Event(_('Sent when a video is recorded.'),webcam=_('The Webcam widget that recorded the video.'))
	@classmethod
	def icon(A):return'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 256 256"><circle cx="128" cy="128" r="32" fill="currentColor" opacity="0.2"/><path fill="currentColor" d="M208 56H48a16 16 0 0 0-16 16v112a16 16 0 0 0 16 16h160a16 16 0 0 0 16-16V72a16 16 0 0 0-16-16m0 128H48V72h160zM128 96a32 32 0 1 0 32 32a32 32 0 0 0-32-32m0 48a16 16 0 1 1 16-16a16 16 0 0 1-16 16"/></svg>'
	def trigger(A):
		if hasattr(A,_E):A._shutter_btn.click()
	def set_mode(A,mode):
		if A.mode!=_A:return
		if mode in[_B,_C]:
			A._active_mode=mode
			if hasattr(A,'_mode_buttons'):A._update_mode_buttons()
			if hasattr(A,_H):A._mode_indicator._dom_element.textContent=A._mode_label()
			if hasattr(A,_E):A._set_shutter_text()
	def _current_mode(A):
		if A.mode==_A:return getattr(A,'_active_mode',_B)
		return A.mode
	def capture_photo(A):
		if hasattr(A,'_canvas')and hasattr(A,'_video_elem'):B=A._video_elem._dom_element;C=A._canvas._dom_element;D=B.videoWidth or 1280;E=B.videoHeight or 720;C.width=D;C.height=E;F=C.getContext('2d');F.drawImage(B,0,0,D,E);A._download_canvas_as_image();A.publish(A.photo_captured,webcam=A)
	def _set_status(A,text):
		if not hasattr(A,'_status_elem'):return
		A._status_elem._dom_element.textContent=text
	def _timestamp(A):return int(time.time()*1000)
	def start_recording(A):
		if hasattr(A,_I):
			if not A._recording and A._recorder.state=='inactive':A._recorded_chunks=[];A._recording=_D;A._recorder.start();A._shutter_btn.classes.add(_F);A._set_shutter_text();A._set_status('Recording...')
	def stop_recording(A):
		if hasattr(A,_I)and A._recording and A._recorder.state==_F:A._recording=_G;A._recorder.stop();A._shutter_btn.classes.remove(_F);A._set_shutter_text();A._set_status('Saving video...')
	def on_mode_changed(A):
		C='hidden'
		if not hasattr(A,'_controls'):return
		A._active_mode=_B if A.mode==_A else A.mode;B=A._controls._dom_element
		if hasattr(A,'_modes_container'):
			try:B.removeChild(A._modes_container._dom_element)
			except Exception:pass
			A._modes_container=None;A._mode_buttons=[]
		if A.mode==_A:A._modes_container=A._build_mode_buttons();B.insertBefore(A._modes_container._dom_element,A._shutter_container._dom_element)
		else:A._mode_buttons=[]
		A._set_shutter_text()
		if hasattr(A,_H):A._mode_indicator._dom_element.textContent=A._mode_label()
		if hasattr(A,'_indicators'):
			if A.show_mode_indicator:A._indicators.classes.remove(C)
			else:A._indicators.classes.add(C)
	def _mode_label(A):
		if A._current_mode()==_C:return'Video Mode'
		return'Photo Mode'
	def _update_mode_buttons(B):
		E='active';D='invent-webcam-mode-active'
		for C in B._mode_buttons:
			A=C[_J];F=C['mode']
			if F==B._current_mode():A.classes.add(D);A.classes.add(E)
			else:A.classes.remove(D);A.classes.remove(E)
	def _set_shutter_text(A):
		if not hasattr(A,_E):return
		C=getattr(A,'_recording',_G)
		if A._current_mode()==_C:B='Stop'if C else'Record'
		else:B='Take'
		A._shutter_btn._dom_element.textContent=B
	def _download_canvas_as_image(B):
		try:from pyscript import window as C;A=C.document.createElement('a');A.href=B._canvas._dom_element.toDataURL('image/jpeg');A.download=f"photo-{B._timestamp()}.jpg";A.click()
		except Exception as D:print(f"Error downloading photo: {D}")
	def _on_shutter_click(A,event):
		if A._current_mode()==_B:A.capture_photo()
		elif A._recording:A.stop_recording()
		else:A.start_recording()
	def _setup_webcam_stream(A):
		E='ideal'
		try:
			from pyscript import window as B;C=B.navigator
			if not C.mediaDevices:print('Camera not supported in this browser');return
			D=max(320,min(int(B.innerWidth or 1280),1280));F=max(240,int(D*9/16));G={_C:{'width':{E:D},'height':{E:F},'facingMode':'user'},'audio':_D}
			async def H():
				try:
					B=await C.mediaDevices.getUserMedia(G);A._video_elem.srcObject=B;A._set_status('Webcam ready')
					if A.mode in(_C,_A):A._setup_recorder(B)
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
			C=B.MediaRecorder.new(stream);C.addEventListener('dataavailable',create_proxy(D));C.addEventListener('stop',create_proxy(E));A._recorder=C;A._recording=_G;A._recorded_chunks=[]
		except Exception as F:print(f"Error setting up recorder: {F}")
	def _build_mode_buttons(A):
		A._mode_buttons=[]
		def F(mode_name):C=mode_name;D='Photo'if C==_B else'Video';B=button(D);B.id=f"{A.id}-{C}-btn";B.classes.add('invent-webcam-mode-btn');B.classes.add('mode-btn');B._dom_element.addEventListener('click',create_proxy(lambda e,m=C:A.set_mode(m)));return B
		C=[]
		for D in[_B,_C]:E=F(D);C.append(E);A._mode_buttons.append({_J:E,'mode':D})
		B=div(*C);B.classes.add('invent-webcam-modes');B.classes.add('modes');A._update_mode_buttons();return B
	def render(A):
		A._canvas=canvas();A._canvas.classes.add('invent-webcam-canvas-hidden');A._video_elem=video();A._video_elem.id=f"{A.id}-video";A._video_elem.autoplay=_D;A._video_elem.muted=_D;A._video_elem.classes.add('invent-webcam-video')
		def E(event):B=A._video_elem._dom_element;C=A._canvas._dom_element;D=B.videoWidth or 1280;E=B.videoHeight or 720;C.width=D;C.height=E
		A._video_elem._dom_element.addEventListener('loadedmetadata',create_proxy(E));C=div(A._video_elem);C.classes.add('invent-webcam-box');C.classes.add('webcam-box');A._shutter_btn=button('Take');A._shutter_btn.id=f"{A.id}-shutter";A._shutter_btn.classes.add('invent-webcam-shutter');A._shutter_btn.classes.add('shutter');A._shutter_btn._dom_element.addEventListener('click',create_proxy(A._on_shutter_click));B=div(A._shutter_btn);B.classes.add('invent-webcam-shutter-container');B.classes.add('shutter-container');A._controls=div(B);A._controls.classes.add('invent-webcam-actions');A._controls.classes.add('actions');A._shutter_container=B;A._status_elem=div('Initializing camera...');A._status_elem.id=f"{A.id}-status";A._status_elem.classes.add('invent-webcam-status');A._mode_indicator=div('');A._mode_indicator.id=f"{A.id}-mode-indicator";A._mode_indicator.classes.add('mode-selection');A._mode_indicator.classes.add('invent-webcam-mode-indicator');A._indicators=div(A._status_elem,A._mode_indicator);A._indicators.classes.add('invent-webcam-indicators');A._indicators.classes.add('indicators');D=div(A._canvas,C,A._controls,A._indicators,id=A.id);D.classes.add('invent-webcam');D.classes.add('webcam-container');A._setup_webcam_stream();return D