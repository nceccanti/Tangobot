import speech_recognition as sr

class VoiceInput:
    def listen(self, input):
        isWord = False
        while isWord == False
            with sr.Microphone() as source:
                r = sr.Recognizer()
                r.adjust_for_ambient_noise(source)
                r.dynamic_energythreshold = 3000
                try:
                    print("listening")
                    audio = r.listen(source)
                    print("got audio")
                    word = r.recognize_google(audio)
                    if word == input:
                        isWord = True
                except sr.UnknownValueError:
                    print("unknown words")
        return isWord