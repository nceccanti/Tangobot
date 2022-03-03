import tkinter as tk
import serial, time, sys
from Move import *

class KeyControl:

    def arrow(self, key):
        if key.keycode == 111:
            robot.forwardWheel()
        elif key.keycode == 116:
            robot.backwardWheel()
        elif key.keycode == 114:
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
for i in range(0,10000, 50):
    # inp = int(input("Enter target: "))
    print(i)
    robot.pivotTest(i)


# win = tk.Tk()
# keys = KeyControl()
#
# win.bind('<Up>', keys.arrow)
# win.bind('<Down>', keys.arrow)
# win.bind('<Left>', keys.arrow)
# win.bind('<Right>', keys.arrow)
# win.bind('<a>', keys.waist)
# win.bind('<d>', keys.waist)
# win.bind('<i>', keys.head)
# win.bind('<k>', keys.head)
# win.bind('<j>', keys.head)
# win.bind('<l>', keys.head)
# win.mainloop()

