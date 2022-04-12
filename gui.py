import tkinter as tk

class MouseMovement():
    def __init__(self, c):
        self.flag = False
        self.myCan = c
        self.objects = []
        self.track = None
        self.trackId = None

    def addObject(self, x, y, width, height, color, id):
        self.objects.append([x,y,width,height,color,id])

    def mousePressed(self, event):
        for i in range(len(self.objects)):
            if event.x > self.objects[i][0] and event.x < self.objects[i][0] + self.objects[i][2] and event.y > self.objects[i][1] and event.y < self.objects[i][1] + self.objects[i][3]:
                self.flag = True
                self.track = i
                self.trackId = self.objects[i][5]

    def mouseDragged(self, event):
        if self.flag == True:
            self.myCan.delete(self.trackId)
            self.myCan.create_rectangle(event.x, event.y, event.x + self.objects[self.track][2], event.y + self.objects[self.track][3], fill=self.objects[self.track][4])

    def mouseRelease(self, event):
        if self.flag == True:
            self.flag = False
            self.myCan.delete(self.trackId)
            self.myCan.create_rectangle(self.objects[self.track][0], self.objects[self.track][1], self.objects[self.track][0] + self.objects[self.track][2], self.objects[self.track][1] + self.objects[self.track][3], fill=self.objects[self.track][4])
            self.track=None
            self.trackId=None


class GUI:
    def __init__(self, win):
        self.win = win
        self.win.geometry("800x480")

    def createWindow(self):
        self.myCan = tk.Canvas(self.win, bg="#333333", width="500", height="500")
        m1 = MouseMovement(self.myCan)
        self.myCan.bind('<B1-Motion>', m1.mouseDragged)
        self.myCan.bind('<ButtonPress-1>', m1.mousePressed)
        self.myCan.bind('<ButtonRelease-1>', m1.mouseRelease)
        self.addInteractive(5, 5, 40, 40, "#FFFF00", m1)
        self.addInteractive(200, 5, 40, 40, "#FF0000", m1)
        #self.myCan.create_rectangle(5, 5, 45, 45, fill="#FFFF00")
        self.myCan.pack()

    def addInteractive(self, x, y, height, width, color, controller):
        xf = x + width
        yf = y + height
        temp = self.myCan.create_rectangle(x, y, xf, yf, fill=color)
        print(temp)
        controller.addObject(x, y, width, height, color, temp)

if __name__ == '__main__':
    win = tk.Tk()
    g = GUI(win)
    g.createWindow()
    win.mainloop()