import os.path
import tkinter as tk
import serial, time, sys
import speech_recognition as sr
from Move import *
# class FileControl:
#     def readFile(self):
#         if os.path.isfile('data.txt'):
#             with open('data.txt', 'r') as file:
#                 f = file.read()
#

class VoiceControl:
    def controller(self, s):
        ind = []
        if s.find("girl") != -1 or s.find("stop") != -1:
            print("command stop")
            robot.stop()
        elif s.find("giddyup") != -1 or s.find("giddy up") != -1:
            print("command forward")
            robot.forwardWheel()
        elif s.find("reverse") != -1:
            print("command backward")
            robot.backwardWheel()
        elif s.find("turn left") != -1:
            print("command left")
            robot.pivotLeft()
        elif s.find("turn right") != -1:
            print("command right")
            robot.pivotRight()
        elif s.find("neck left") != -1:
            print("command neck left")
            robot.neckLeft()
        elif s.find("neck right") != -1:
            print("command neck right")
            robot.neckRight()
        elif s.find("neck up") != -1:
            print("command neckup")
            robot.neckUp()
        elif s.find("neck down") != -1:
            print("command neckdown")
            robot.neckDown()
        elif s.find("waist left") != -1:
            print("command waist left")
            robot.waistLeft()
        elif s.find("waist right") != -1:
            print("command stop")
            robot.waistRight()



class KeyControl:
    def lateral(self, key):
        if key.keycode == 111:
            robot.forwardWheel()
        elif key.keycode == 116:
            robot.backwardWheel()

    def turn(self, key):
        if key.keycode == 114:
            robot.pivotRight()
        elif key.keycode == 113:
            robot.pivotLeft()


    def waist(self, key):
        if key.keycode == 38:
            robot.waistLeft()
        elif key.keycode == 40:
            robot.waistRight()

    def head(self, key):
        if key.keycode == 31:
            robot.neckUp()
        elif key.keycode == 45:
            robot.neckDown()
        elif key.keycode == 44:
            robot.neckLeft()
        elif key.keycode == 46:
            robot.neckRight()
    def reset(self, key):
        print(key.keycode)
        robot.stop()
    
usb = ""
try:
    usb = serial.Serial('/dev/ttyACM0')
except:
    try:
        usb = serial.Serial('/dev/ttyACM1')
    except:
        print("No serial ports")
        sys.exit(0)

robot = Move(500, usb)
robot.stop()

listening = True
while listening:
    with sr.Microphone() as source:
        r = sr.Recognizer()
        r.adjust_for_ambient_noise(source)
        r.dynamic_energythreshold = 3000
        try:
            print(listening)
            audio = r.listen(source)
            print("got audio")
            word = r.recognize_google(audio)
            print(word)
            v = VoiceControl()
            v.controller(word)

        except sr.UnknownValueError:
            print("unknown words")





# win = tk.Tk()
# keys = KeyControl()

# win.bind('<Up>', keys.lateral)
# win.bind('<Down>', keys.lateral)
# win.bind('<Left>', keys.turn)
# win.bind('<Right>', keys.turn)
# win.bind('<a>', keys.waist)
# win.bind('<d>', keys.waist)
# win.bind('<i>', keys.head)
# win.bind('<k>', keys.head)
# win.bind('<j>', keys.head)
# win.bind('<l>', keys.head)
# win.bind('<space>', keys.reset)
# win.mainloop()















