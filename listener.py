import tkinter as tk
import serial, time, sys
from Move import *

class KeyControl:

    def arrow(self, key):
        if key.keycode == 2113992448:
            robot.forwardWheel()
        elif key.keycode == 2097215233:
            robot.backwardWheel()
        elif key.keycode == 2080438019:
            robot.pivotRight()
        elif key.keycode == 2063660802:
            robot.pivotLeft()

    def waist(self, key):
        if key.keycode == 97:
            robot.waistLeft()
        elif key.keycode == 33554532:
            robot.waistRight()

    def head(self, key):
        if key.keycode == 570425449:
            robot.neckUp()
        elif key.keycode == 671088747:
            robot.neckDown()
        elif key.keycode == 637534314:
            robot.neckLeft()
        elif key.keycode == 620757100:
            robot.neckRight()
    

win = tk.Tk()
keys = KeyControl()

win.bind('<Up>', keys.arrow)
win.bind('<Down>', keys.arrow)
win.bind('<Left>', keys.arrow)
win.bind('<Right>', keys.arrow)
win.bind('<a>', keys.waist)
win.bind('<d>', keys.waist)
win.bind('<i>', keys.head)
win.bind('<k>', keys.head)
win.bind('<j>', keys.head)
win.bind('<l>', keys.head)
win.mainloop()

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
















