import tkinter as tk
import serial, time, sys
from Move import *

usb = ""
try:
    usb = serial.Serial('/dev/ttyACM0')
except:
    try:
        usb = serial.Serial('/dev/ttyACM1')
    except:
        print("No serial ports")
        #sys.exit(0)

robot = Move(500, usb)

#Event controller
class MouseMovement():
    def __init__(self, c):
        self.selected = [False, None]
        self.flag = False
        self.myCan = c
        self.draggables = []
        self.static = []
        self.background = []
        self.variables = []
        self.track = None
        self.trackId = None
        self.target = None
        self.time = None
        self.staticIndexTarget = None
        self.window = None

    #Adds Varibale object to be tracked
    def addVariable(self, x, y, text, fill, font):
        self.variables.append([x, y, text, fill, font])

    #Adds draggable object to be tracked
    def addDraggable(self, x, y, width, height, color, attribute):
        self.draggables.append([x, y, width, height, color, attribute])

    #Adds static interactable object to be tracked
    def addStatic(self, x, y, width, height, color):
        self.static.append([x, y, width, height, color, None, None])

    #Adds static background object, these objects are intended to have no interaction with the user
    def addBackgroundObject(self, x, y, width, height, color):
        self.background.append([x, y, width, height, color])

    #What happens when mouse is pressed down
    def mousePressed(self, event):
        if event.x > 900 and event.x < 950 and event.y > 500 and event.y < 550:
            self.execute()
        for i in range(len(self.draggables)):
            if event.x > self.draggables[i][0] and event.x < self.draggables[i][0] + self.draggables[i][2] and event.y > self.draggables[i][1] and event.y < self.draggables[i][1] + self.draggables[i][3]:
                self.flag = True
                self.track = i
        for i in range(len(self.static)):
            if event.x > self.static[i][0] and event.x < self.static[i][2] and event.y > self.static[i][1] and event.y < self.static[i][1] + self.static[i][3]:
                if self.selected[0] == False:
                    self.selected = [True, i]
                elif self.selected[0] == True:
                    self.SubWindow(i)
                    self.selected = [False, None]

    #What happens when you drag the mouse
    def mouseDragged(self, event):
        if self.flag == True:
            self.myCan.delete('all')
            self.printElse()
            for i in range(len(self.draggables)):
                if i == self.track:
                    self.myCan.create_rectangle(event.x, event.y, event.x + self.draggables[self.track][2], event.y + self.draggables[self.track][3], fill=self.draggables[self.track][4])
                else:
                    self.myCan.create_rectangle(self.draggables[i][0], self.draggables[i][1], self.draggables[i][0] + self.draggables[i][2], self.draggables[i][1] + self.draggables[i][3], fill=self.draggables[i][4])

    #Re-prints all static objects
    def printElse(self):
        for i in self.background:
            self.myCan.create_rectangle(i[0], i[1], i[2], i[3], fill=i[4])
        for i in self.variables:
            self.myCan.create_text(i[0], i[1], text=i[2], fill=i[3], font=i[4])
        for i in self.static:
            #print(i[0], i[1], i[2], i[3], i[4])
            if i[5] is None:
                self.myCan.create_rectangle(i[0], i[1], i[2], i[3], fill=i[4])
            else:
                self.myCan.create_rectangle(i[0], i[1], i[2], i[3], fill=i[5])

    #Returns all draggable objects to original position
    def printDraggables(self):
        for i in self.draggables:
            #print(i[0], i[1], i[2], i[3], i[4])
            self.myCan.create_rectangle(i[0], i[1], i[0] + i[2], i[1] + i[3], fill=i[4])
 
    #What happens when mouse press is released
    def mouseRelease(self, event):
        if self.flag == True:
            self.flag = False
            self.myCan.delete('all')
            for i in range(len(self.static)):
                if event.x > self.static[i][0] and event.x < self.static[i][2] and event.y > self.static[i][1] and event.y < self.static[i][3]:
                    self.static[i] = [self.static[i][0], self.static[i][1], self.static[i][2], self.static[i][3], self.static[i][4], self.draggables[self.track][4], self.draggables[self.track][5]]
            self.printElse()
            self.printDraggables()
            self.track=None
            self.trackId=None

    #Deletes attribute from static object
    def rightClick(self, event):
        for i in range(len(self.static)):
            if event.x > self.static[i][0] and event.x < self.static[i][2] and event.y > self.static[i][1] and event.y < self.static[i][3]:
                self.static[i] = [self.static[i][0], self.static[i][1], self.static[i][2], self.static[i][3], self.static[i][4], None, None]
        self.printElse()

    def execute(self):
        #print("execute instructions")
        for i in self.static:
            if i[6] is not None:
                print(i[6][0], int(float(i[6][1])), float(i[6][2]))
                robot.setTarget(0x01, 6000)
                robot.setTarget(0x02, 6000)
                robot.setTarget(i[6][0], int(float(i[6][1])))
                time.sleep(float(i[6][2]))

    def SubWindow(self, staticIndex):
        print("sub window")
        newWindow = tk.Toplevel(self.myCan)
        newWindow.title("Edit Instruction")
        newWindow.geometry("400x400")
        self.target = tk.Entry(newWindow, width=40)
        self.target.focus_set()
        self.target.pack()
        self.time = tk.Entry(newWindow, width=40)
        self.time.focus_set()
        self.time.pack()
        self.staticIndexTarget = staticIndex
        self.window = newWindow
        tk.Button(newWindow, text='Submit', width=20, command=self.SubmitText).pack(pady=20)


    def SubmitText(self):
        target = self.target.get()
        time = self.time.get()
        self.static[self.staticIndexTarget][6][1] = target
        self.static[self.staticIndexTarget][6][2] = time
        self.window.destroy()
        self.target = None
        self.time = None
        self.staticIndexTarget = None
        self.window = None

class GUI:
    def __init__(self, win):
        self.win = win
        self.win.geometry("1024x600")

    #Creates GUI window, create all objects here
    def createWindow(self):
        self.myCan = tk.Canvas(self.win, bg="#333333", width="1024", height="600")
        m1 = MouseMovement(self.myCan)
        self.myCan.bind('<B1-Motion>', m1.mouseDragged)
        self.myCan.bind('<ButtonPress-1>', m1.mousePressed)
        self.myCan.bind('<ButtonRelease-1>', m1.mouseRelease)
        self.myCan.bind('<ButtonPress-3>', m1.rightClick)
        self.myCan.bind('<space>', m1.execute())
        self.addBackground(0, 140, 8, 1024, '#222222', m1)
        self.addBackground(900, 500, 50, 50, '#000000', m1)
        self.addVariable(120, 480, "Move", "Black", 'Helvetica 13 bold', m1)
        self.addVariable(220, 480, "Turn", "Black", 'Helvetica 13 bold', m1)
        self.addVariable(320, 480, "Waist", "Black", 'Helvetica 13 bold', m1)
        self.addVariable(420, 480, "Neck Vertical", "Black", 'Helvetica 13 bold', m1)
        self.addVariable(520, 480, "Neck Lateral", "Black", 'Helvetica 13 bold', m1)
        self.addMoveable(100, 500, 40, 40, "#FFFF00", m1, [0x01, 6000, 1])
        self.addMoveable(200, 500, 40, 40, "#FF0000", m1, [0x02, 6000, 1])
        self.addMoveable(300, 500, 40, 40, "#008000", m1, [0x00, 6000, 1])
        self.addMoveable(400, 500, 40, 40, "#800080", m1, [0x04, 6000, 1])
        self.addMoveable(500, 500, 40, 40, "#0000FF", m1, [0x03, 6000, 1])


        for i in range(8):
            x = i * 128
            self.addDestination(x+20, 100, 88, 88, "#B4E4F5", m1)
        self.myCan.pack()

    #Adds variable object
    def addVariable(self, x, y, text1, fill1, font1, controller):
        self.myCan.create_text(x, y, text=text1, fill=fill1, font=(font1))
        controller.addVariable(x, y, text1, fill1, font1)

    #Adds draggable object
    def addMoveable(self, x, y, height, width, color, controller, attribute):
        xf = x + width
        yf = y + height
        self.myCan.create_rectangle(x, y, xf, yf, fill=color)
        controller.addDraggable(x, y, width, height, color, attribute)

    #Adds box for draggable object to be "dropped" into
    def addDestination(self, x, y, height, width, color, controller):
        xf = x + width
        yf = y + height
        self.myCan.create_rectangle(x, y, xf, yf , fill=color)
        controller.addStatic(x, y, xf, yf, color)

    def addBackground(self, x, y, height, width, color, controller):
        xf = x + width
        yf = y + height
        self.myCan.create_rectangle(x, y, xf, yf, fill=color)
        controller.addBackgroundObject(x, y, xf, yf, color)

if __name__ == '__main__':
    win = tk.Tk()
    g = GUI(win)
    g.createWindow()
    win.mainloop()