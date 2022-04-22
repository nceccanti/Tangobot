import tkinter as tk
import serial, time, sys
from Move import *
from voiceinput import *
from speak import *

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
robot.stop()
Voice = VoiceInput()

#Event controller
class MouseMovement():
    def __init__(self, c):
        self.id = 0
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
        self.point = []

    #Adds Varibale object to be tracked
    def addVariable(self, x, y, text, fill, font):
        self.variables.append([x, y, text, fill, font])

    #Adds draggable object to be tracked
    def addDraggable(self, x, y, width, height, color, attribute, labels):
        self.draggables.append([x, y, width, height, color, attribute, labels])

    #Adds static interactable object to be tracked
    def addStatic(self, x, y, width, height, color):
        self.static.append([x, y, width, height, color, None, None, None])
        self.id += 1

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
            if event.x > self.static[i][0] and event.x < self.static[i][2] and event.y > self.static[i][1] and event.y < self.static[i][1] + self.static[i][3] and self.static[i][6] is not None:
                if self.selected[0] == False:
                    self.selected = [True, i]
                elif self.selected[0] == True:
                    self.selected = [False, None]
                    #print(self.static[i][6][0])
                    if len(self.static[i][7][0]) == 0:
                        self.SubWindowText(i)
                        print(i)
                    else:
                        self.SubWindow(i)
        if event.x > 900 and event.x < 950 and event.y > 400 and event.y < 450:
            self.reset()

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
                    self.static[i] = [self.static[i][0], self.static[i][1], self.static[i][2], self.static[i][3], self.static[i][4], self.draggables[self.track][4], self.draggables[self.track][5], self.draggables[self.track][6]]
                    print(self.static[i])
                    print(i)
            self.printElse()
            self.printDraggables()
            print(self.track)
            self.track=None
            self.trackId=None

    #Deletes attribute from static object
    def reset(self):
        for i in range(len(self.static)):
            self.static[i] = [self.static[i][0], self.static[i][1], self.static[i][2], self.static[i][3], self.static[i][4], None, None]
        self.printElse()

    def execute(self):
        wait = 0
        print(self.point)
        self.myCan.delete("all")
        for i in self.static:
            print(i[6])
            if i[6] is not None:
                if '!' == i[6][0]:
                    print("voice!")
                    print(i[6][1])
                    Voice.listen(i[6][1])
                elif '~' == i[6][0]:
                    print("speak!")
                    print(i[6][1])
                    s = Speaker()
                    s.TTS(i[6][1])
                else:
                    print(i[6][0], int(float(i[6][1])), float(i[6][2]))
                    robot.setTarget(0x01, 6000)
                    robot.setTarget(0x02, 6000)
                    if 0x01 == i[6][0]:
                        robot.setTarget(0x01, 6200)
                    if 0x02 == i[6][0]:
                        robot.setTarget(0x02, 6200)
                    print(self.static.index(i))
                    tar = self.point[self.static.index(i)][1]
                    robot.setTarget(i[6][0], tar)
                    wait = self.point[self.static.index(i)][2]
                win2 = self.myCan
                e = Eyes(win2)
                for i in range(wait):
                    e.blink()
                robot.setTarget(0x01, 6000)
                robot.setTarget(0x02, 6000)
                time.sleep(1)
                
        self.myCan.delete("all")
        self.printElse()
        self.printDraggables()

    def SubWindow(self, staticIndex):
        print("sub window")
        print(staticIndex)
        newWindow = tk.Toplevel(self.myCan)
        newWindow.title("Edit Instruction")
        newWindow.geometry("800x400")
        print(self.static[staticIndex][6])
        currentTarget = self.static[staticIndex][6][1] - 6000
        currentTime = self.static[staticIndex][6][2]
        newWindow.columnconfigure(0, weight=1)
        newWindow.columnconfigure(1, weight=3)
        targetLabelLeft = tk.Label(
            newWindow,
            text=self.static[staticIndex][7][0]
        )
        targetLabelLeft.grid(
            column=0,
            row=0,
            sticky='w'
        )
        self.target = tk.Scale(
            newWindow,
            from_= -2000,
            to=2000,
            orient='horizontal',
        )
        self.target.grid(
            column=1,
            row=0,
            sticky='we',
        )
        targetLabelRight = tk.Label(
            newWindow,
            text=self.static[staticIndex][7][1]
        )
        targetLabelRight.grid(
            column=2,
            row=0,
            sticky='w'
        )
        self.target.focus_set()
        print(str(currentTarget) + "curr")
        self.target.set(currentTarget)
        timeLabelLeft = tk.Label(
            newWindow,
            text="Time (seconds): "
        )
        timeLabelLeft.grid(
            columnspan=2,
            row=1,
            sticky='w'
        )
        self.time = tk.Scale(
            newWindow,
            from_=0,
            to=60,
            length=350,
            orient='horizontal',
        )
        self.time.grid(
            column=1,
            row=1,
            sticky='we',
        )
        self.time.focus_set()
        self.time.set(currentTime)

        self.staticIndexTarget = staticIndex
        self.window = newWindow
        sub = tk.Button(newWindow, text='Submit', width=20, command=self.SubmitText)
        sub.grid(
            column=1,
            row=3,
            sticky='we',
        )

    def SubmitText(self):
        target = self.target.get()
        time = self.time.get()
        print(self.staticIndexTarget)
        self.static[self.staticIndexTarget][6][1] = target + 6000
        self.static[self.staticIndexTarget][6][2] = time
        print(self.static[self.staticIndexTarget][6])
        self.point.append([self.staticIndexTarget, target + 6000, time])
        self.window.destroy()
        self.target = None
        self.time = None
        self.staticIndexTarget = None
        self.window = None

    def SubWindowText(self, staticIndex):
        print("sub window")
        newWindow = tk.Toplevel(self.myCan)
        newWindow.title("Edit Instruction")
        newWindow.geometry("800x400")
        currentTime = self.static[staticIndex][6][2]
        newWindow.columnconfigure(0, weight=1)
        newWindow.columnconfigure(1, weight=3)
        sub1 = tk.Button(newWindow, text='Hello', width=20, command=self.setHello)
        sub1.grid(
            column=1,
            row=1,
            sticky='we',
        )
        sub2 = tk.Button(newWindow, text='Howdy', width=20, command=self.setHowdy)
        sub2.grid(
            column=1,
            row=2,
            sticky='we',
        )
        sub3 = tk.Button(newWindow, text='Robot', width=20, command=self.setRobot)
        sub3.grid(
            column=1,
            row=3,
            sticky='we',
        )
        timeLabelLeft = tk.Label(
            newWindow,
            text="Time (seconds): "
        )
        timeLabelLeft.grid(
            columnspan=2,
            row=4,
            sticky='w'
        )
        self.time = tk.Scale(
            newWindow,
            from_=0,
            to=60,
            length=350,
            orient='horizontal',
        )
        self.time.grid(
            column=1,
            row=4,
            sticky='we',
        )
        self.time.focus_set()
        self.time.set(currentTime)
        self.staticIndexTarget = staticIndex
        self.window = newWindow
        sub = tk.Button(newWindow, text='Submit', width=20, command=self.SubmitTextStr)
        sub.grid(
            column=1,
            row=5,
            sticky='we',
        )

    def setHello(self):
        self.target = "hello"

    def setHowdy(self):
        self.target = "howdy"

    def setRobot(self):
        self.target = "robot"

    def SubmitTextStr(self):
        target = self.target
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
        self.win.attributes('-fullscreen',True)

    #Creates GUI window, create all objects here
    def createWindow(self):
        self.myCan = tk.Canvas(self.win, bg="#333333", width="1024", height="600")
        m1 = MouseMovement(self.myCan)
        self.myCan.bind('<B1-Motion>', m1.mouseDragged)
        self.myCan.bind('<ButtonPress-1>', m1.mousePressed)
        self.myCan.bind('<ButtonRelease-1>', m1.mouseRelease)
        self.myCan.bind('<space>', m1.execute())
        self.addBackground(0, 140, 8, 1024, '#222222', m1)
        self.addBackground(900, 500, 50, 50, '#000000', m1)
        self.addBackground(900, 400, 50, 50, '#FFFFFF', m1)
        self.addVariable(60, 480, "Move", "Black", 'Helvetica 13 bold', m1)
        self.addVariable(170, 480, "Turn", "Black", 'Helvetica 13 bold', m1)
        self.addVariable(280, 480, "Waist", "Black", 'Helvetica 13 bold', m1)
        self.addVariable(390, 480, "Neck Vertical", "Black", 'Helvetica 13 bold', m1)
        self.addVariable(500, 480, "Neck Lateral", "Black", 'Helvetica 13 bold', m1)
        self.addVariable(610, 480, "Speak", "Black", 'Helvetica 13 bold', m1)
        self.addVariable(720, 480, "Voice Command", "Black", 'Helvetica 13 bold', m1)
        self.addVariable(925, 380, "Reset", "Black", 'Helvetica 13 bold', m1)
        self.addVariable(925, 480, "Execute", "Black", 'Helvetica 13 bold', m1)
        self.addMoveable(40, 500, 40, 40, "#FFFF00", m1, [0x01, 6000, 1], ['Forward', 'Backward'])
        self.addMoveable(150, 500, 40, 40, "#FF0000", m1, [0x02, 6000, 1], ['Right', 'Left'])
        self.addMoveable(260, 500, 40, 40, "#008000", m1, [0x00, 6000, 1], ['Right', 'Left'])
        self.addMoveable(370, 500, 40, 40, "#800080", m1, [0x04, 6000, 1], ['Down', 'Up'])
        self.addMoveable(480, 500, 40, 40, "#0000FF", m1, [0x03, 6000, 1], ['Right', 'Left'])
        self.addMoveable(590, 500, 40, 40, "#FFA500", m1, ['~', "", 1], ['', ''])
        self.addMoveable(700, 500, 40, 40, "#FFC0CB", m1, ['!', "", 1], ['', ''])

        for i in range(8):
            x = i * 128
            self.addDestination(x+20, 100, 88, 88, "#B4E4F5", m1)
        self.myCan.pack()

    #Adds variable object
    def addVariable(self, x, y, text1, fill1, font1, controller):
        self.myCan.create_text(x, y, text=text1, fill=fill1, font=(font1))
        controller.addVariable(x, y, text1, fill1, font1)

    #Adds draggable object
    def addMoveable(self, x, y, height, width, color, controller, attribute, labels):
        xf = x + width
        yf = y + height
        self.myCan.create_rectangle(x, y, xf, yf, fill=color)
        controller.addDraggable(x, y, width, height, color, attribute, labels)

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

class Eyes():
    def __init__(self, win):
        self.myCan = win

    def eyeballs(self):
        print("eyes")
        self.myCan.create_oval(75, 75, 200, 300, fil="white")
        self.myCan.create_oval(225, 75, 350, 300, fil="white")
        self.myCan.create_oval(105, 180, 165, 270, fil="black")
        self.myCan.create_oval(255, 180, 310, 270, fil="black")
        self.myCan.create_oval(110, 230, 130, 250, fil="white")
        self.myCan.create_oval(260, 230, 280, 250, fil="white")
        self.myCan.pack()

    def eyelids(self):
        print("blink")
        self.myCan.create_oval(75, 75, 200, 300, fil="yellow")
        self.myCan.create_oval(225, 75, 350, 300, fil="yellow")
        self.myCan.pack()

    def blink(self):
        self.eyeballs()
        self.myCan.update()
        self.myCan.after(750, self.eyelids())
        self.myCan.update()
        self.myCan.after(250, self.eyeballs())

if __name__ == '__main__':
    win = tk.Tk()
    g = GUI(win)
    g.createWindow()
    win.mainloop()