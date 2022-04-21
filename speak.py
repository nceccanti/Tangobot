import pyttsx3

class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[10].id)

    def TTS(self, text):
        self.engine.say(text)
        self.engine.runAndWait()