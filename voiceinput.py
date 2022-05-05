import speech_recognition as sr

class VoiceInput:
    def listen(self, input):
        valid = ''
        isWord = False
        while isWord == False:
            with sr.Microphone() as source:
                r = sr.Recognizer()
                r.adjust_for_ambient_noise(source)
                try:
                    print("listening")
                    audio = r.listen(source)
                    print("got audio")
                    word = r.recognize_google(audio)
                    print(word)
                    for i in len(input):
                        if word.find(input[i]) != -1:
                            isWord = True
                            valid = word
                except sr.UnknownValueError:
                    print("unknown words")
        return valid
