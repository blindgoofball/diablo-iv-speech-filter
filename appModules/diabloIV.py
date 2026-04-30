import appModuleHandler
import speech
from logHandler import log
import html

class AppModule(appModuleHandler.AppModule):
	def __init__(self, processID, appName=None):
		super().__init__(processID, appName)
		self.originalSpeak=speech.speech.speak
		speech.speech.speak=self.newSpeak
	def terminate(self):
		super().terminate()
		speech.speech.speak=self.originalSpeak
	def newSpeak(self, sequence, *args, **kwargs):
		newSeq=[]
		for item in sequence:
			if isinstance(item, str):
				if item == 'blank':
					item=''
				item=html.unescape(item)
			newSeq.append(item)
		return self.originalSpeak(newSeq, *args, **kwargs)
	def event_loseFocus(self, obj, nextHandler):
		speech.speech.speak=self.originalSpeak
		nextHandler()
	def event_gainFocus(self, obj, nextHandler):
		speech.speech.speak=self.newSpeak
		nextHandler()