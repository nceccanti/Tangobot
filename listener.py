import tkinter as tk
import serial, time, sys
from Move import *

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
    def reset(self):
        robot.resetMovement()
    
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

win = tk.Tk()
keys = KeyControl()

win.bind('<Up>', keys.lateral)
win.bind('<Down>', keys.lateral)
win.bind('<Left>', keys.turn)
win.bind('<Right>', keys.turn)
win.bind('<a>', keys.waist)
win.bind('<d>', keys.waist)
win.bind('<i>', keys.head)
win.bind('<k>', keys.head)
win.bind('<j>', keys.head)
win.bind('<l>', keys.head)
win.bind('<Space>', keys.reset)
win.mainloop()















