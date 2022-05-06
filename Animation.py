import timeit
import tkinter as tk
import _thread, threading
#from Move import *
from fireworks import *
import time


class Screen:
    def __init__(self, win):
        self.myCan = win

    def CoffeeSteam(self):
        self.myCan.create_oval(372, 100, 664, 500, fill="#333333", outline='')
        self.myCan.create_oval(162, 0, 862, 300, fill="#222222", outline='')
        self.myCan.create_oval(376, 240, 664, 290, fill="#804000", outline='')
        self.myCan.create_line(375, 50, 415, 100, 375, 150, 415, 200, smooth=1, fill='white', width=5)
        self.myCan.create_line(475, 50, 515, 100, 475, 150, 515, 200, smooth=1, fill='white', width=5)
        self.myCan.create_line(575, 50, 615, 100, 575, 150, 615, 200, smooth=1, fill='white', width=5)
        self.myCan.pack()

    def CoffeeCup(self):
        self.myCan.create_oval(372, 100, 664, 500, fill="#333333", outline='')
        self.myCan.create_oval(162, 0, 862, 300, fill="#222222", outline='')
        self.myCan.create_oval(376, 240, 664, 290, fill="#804000", outline='')
        self.myCan.pack()

    def CoffeeScreen(self):
        print("test")
        self.CoffeeCup()
        self.myCan.update()
        self.myCan.after(500, self.CoffeeSteam())
        self.myCan.update()
        self.myCan.after(1000, self.CoffeeCup())

    def Lightning(self):
        self.myCan.create_polygon(512, 50, 225, 330, 475, 330, 400, 550, 675, 270, 425, 270, fill='yellow')
        self.myCan.pack()

    def WhiteLightning(self):
        self.myCan.create_polygon(512, 50, 225, 330, 475, 330, 400, 550, 675, 270, 425, 270, fill='white')
        self.myCan.pack()

    def RechargeScreen(self):
        #512, 50, 400, 325, 450, 325, 400, 500, 475, 275, 425, 275
        self.Lightning()
        self.myCan.update()
        self.myCan.after(250, self.WhiteLightning())
        self.myCan.update()
        self.myCan.after(750, self.Lightning())
        self.myCan.update()

    def WhiteRiddle(self):
        self.myCan.create_oval(312, 50, 712, 450, fill="green", outline='')
        self.myCan.create_polygon(319, 300, 705, 300, 812, 400, 212, 400, fill='purple')
        self.myCan.create_oval(112, 350, 912, 450, fill="green", outline='')
        self.myCan.create_oval(256, 335, 768, 385, fill="purple", outline='')
        self.myCan.pack()

    def Riddle(self):
        self.myCan.create_oval(312, 50, 712, 450, fill="white", outline='')
        self.myCan.create_polygon(319, 300, 705, 300, 812, 400, 212, 400, fill='#FFD700')
        self.myCan.create_oval(112, 350, 912, 450, fill="white", outline='')
        self.myCan.create_oval(256, 335, 768, 385, fill="#FFD700", outline='')
        #self.myCan.create_polygon(312, 300, 712, 300, 812, 400, 212, 400, fill='purple')
        self.myCan.pack()

    def TrickyScreen(self):
        self.Riddle()
        self.myCan.update()
        self.myCan.after(500, self.WhiteRiddle())
        self.myCan.update()
        self.myCan.after(1500, self.Riddle())
        self.myCan.update()

    def Circle(self, color, r):
        self.myCan.create_oval(512-r, 300-r, 512+r, 300+r, fill=color, outline='')
        self.myCan.pack()


    def FunScreen(self):
        colors = ["#28B463", "#641E16", "#1B4F72", "#512E5F", "#138D75", "#2ECC71", "#943126", "white"]
        self.Circle("black", 220)
        self.myCan.update()
        r = 200
        for color in colors:
            self.myCan.after(250, self.Circle(color, r))
            self.myCan.update()
            r -= 20

    def Battle(self, enemies):
        for i in range(enemies):
            if i < 3:
                y = 0 * 200
            else:
                y = 1 * 300
            print(i, y)
            x = (i % 3) * 350
            self.myCan.create_oval((25+x), (25+y), (225+x), (225+y), fill="green", outline='')
            self.myCan.create_oval((50+x), (95+y), (200+x), (155+y), fill="white", outline='')
            self.myCan.create_oval((100+x), (100+y), (150+x), (150+y), fill="black", outline='')
        self.myCan.pack()

    def BattleBlink(self, enemies):
        for i in range(enemies):
            if i < 3:
                y = 0 * 200
            else:
                y = 1 * 300
            print(i, y)
            x = (i % 3) * 350
            self.myCan.create_oval((25+x), (25+y), (225+x), (225+y), fill="green", outline='')
            self.myCan.create_oval((50+x), (95+y), (200+x), (155+y), fill="purple")
        self.myCan.pack()

    def BattleScreen(self, enemies):
        self.Battle(enemies)
        self.myCan.update()
        self.myCan.after(250, self.BattleBlink(enemies))
        self.myCan.update()
        self.myCan.after(750, self.Battle(enemies))
        self.myCan.update()

class Animation:
    def __init__(self, win):
        self.win = win
        self.win.geometry("1024x600")
        # self.win.attributes('-fullscreen',True)
        self.myCan = tk.Canvas(self.win, bg="#222222", width="1024", height="600")

    def initial(self):
        self.myCan.create_oval(462, 150, 562, 250, fill="black", outline='')
        self.myCan.create_oval(462, 300, 562, 400, fill="black", outline='')
        self.myCan.create_rectangle(462, 200, 562, 350, fill="black")
        self.myCan.create_line(422, 350, 512, 500, 602, 350, smooth=1, fill='black', width=15)
        self.myCan.create_line(512, 430, 512, 520, smooth=1, fill='black', width=15)
        self.myCan.create_line(412, 520, 612, 520, smooth=1, fill='black', width=15)
        self.myCan.pack()
        self.myCan.update()

    def screenControl(self, wait, type, enemies):
        self.move.setTarget(0x05, 4000)
        self.move.setTarget(0x06, 6000)
        self.move.setTarget(0x08, 6000)
        self.move.setTarget(0x09, 4000)
        self.move.setTarget(0x0a, 6000)
        self.move.setTarget(0x0b, 6000)
        self.myCan.delete('all')
        s = Screen(self.myCan)
        if type == 'B':
            iter = int(wait / 2)
            for i in range(iter):
                self.move.setTarget(0x05, 8000)
                time.sleep(0.2)
                self.move.setTarget(0x0b, 3000)
                s.BattleScreen(enemies)
                self.move.setTarget(0x0b, 6000)
                s.BattleScreen(enemies)
                self.move.setTarget(0x05, 4000)
                self.move.setTarget(0x00, 6000)
        if type == 'CO':
            self.move.setTarget(0x05, 8000)
            time.sleep(0.1)
            self.move.setTarget(0x0b, 4000)
            time.sleep(0.1)
            self.move.setTarget(0x08, 4000)
            iter = int(wait / 1.5)
            for i in range(iter):
                s.CoffeeScreen()
            self.move.setTarget(0x05, 4000)
            time.sleep(0.1)
            self.move.setTarget(0x0b, 6000)
            time.sleep(0.1)
            self.move.setTarget(0x08, 6000)
            self.move.setTarget(0x00, 6000)
        elif type == 'CH':
            self.move.setTarget(0x05, 6000)
            time.sleep(0.1)
            self.move.setTarget(0x0b, 6000)
            time.sleep(0.1)
            iter = int(wait / 2)
            for i in range(iter):
                self.move.setTarget(0x06, 4000)
                s.RechargeScreen()
                self.move.setTarget(0x06, 8000)
                s.RechargeScreen()
                self.move.setTarget(0x05, 4000)
                time.sleep(0.1)
                self.move.setTarget(0x06, 6000)
                time.sleep(0.1)
                self.move.setTarget(0x00, 6000)
        elif type == 'T':
            self.move.setTarget(0x05, 9000)
            iter = int(wait / 2)
            for i in range(iter):
                s.TrickyScreen()
            self.move.setTarget(0x05, 4000)
        elif type == 'F':
            self.move.setTarget(0x05, 11000)
            time.sleep(0.1)
            iter = int(wait / 2)
            for i in range(iter):
                s.FunScreen()
            self.move.setTarget(0x0a, 1000)
            time.sleep(1)
            self.move.setTarget(0x0a, 7000)
            time.sleep(1)
            self.move.setTarget(0x05, 4000)
        self.myCan.delete('all')
        self.myCan.create_oval(462, 150, 562, 250, fill="black", outline='')
        self.myCan.create_oval(462, 300, 562, 400, fill="black", outline='')
        self.myCan.create_rectangle(462, 200, 562, 350, fill="black")
        self.myCan.create_line(422, 350, 512, 500, 602, 350, smooth=1, fill='black', width=15)
        self.myCan.create_line(512, 430, 512, 520, smooth=1, fill='black', width=15)
        self.myCan.create_line(412, 520, 612, 520, smooth=1, fill='black', width=15)


    # def BatteArm(self, wait):
    #     self.move.setTarget(0x05, 8000)
    #     time.sleep(0.2)
    #     iter = int(wait / 2)
    #     for i in range(iter):
    #         self.move.setTarget(0x0b, 3000)
    #         time.sleep(1)
    #         self.move.setTarget(0x0b, 6000)
    #         time.sleep(1)
    #     self.move.setTarget(0x05, 4000)
    #     self.move.setTarget(0x00, 6000)
    #
    # def CoffeeArm(self, wait):
    #     self.move.setTarget(0x05, 8000)
    #     time.sleep(0.1)
    #     self.move.setTarget(0x0b, 4000)
    #     time.sleep(0.1)
    #     self.move.setTarget(0x08, 4000)
    #     time.sleep(wait)
    #     self.move.setTarget(0x05, 4000)
    #     time.sleep(0.1)
    #     self.move.setTarget(0x0b, 6000)
    #     time.sleep(0.1)
    #     self.move.setTarget(0x08, 6000)
    #     self.move.setTarget(0x00, 6000)
    #
    # def RechargeArm(self, wait):
    #     self.move.setTarget(0x05, 6000)
    #     time.sleep(0.1)
    #     self.move.setTarget(0x0b, 6000)
    #     time.sleep(0.1)
    #     iter = int(wait / 2)
    #     for i in range(iter):
    #         self.move.setTarget(0x06, 4000)
    #         time.sleep(1)
    #         self.move.setTarget(0x06, 8000)
    #         time.sleep(1)
    #     self.move.setTarget(0x05, 4000)
    #     time.sleep(0.1)
    #     self.move.setTarget(0x06, 6000)
    #     time.sleep(0.1)
    #     self.move.setTarget(0x00, 6000)
    #
    # def TrickyArm(self, wait):
    #     self.move.setTarget(0x05, 9000)
    #     time.sleep(wait)
    #     self.move.setTarget(0x05, 4000)
    #
    # def FunArm(self, wait):
        # self.move.setTarget(0x05, 11000)
        # time.sleep(0.1)
        # iter = int(wait / 2)
        # for i in range(iter):
        #     self.move.setTarget(0x0a, 1000)
        #     time.sleep(1)
        #     self.move.setTarget(0x0a, 7000)
        #     time.sleep(1)
        # self.move.setTarget(0x05, 4000)




