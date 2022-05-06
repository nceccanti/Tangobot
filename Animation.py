import timeit
import tkinter as tk
import _thread, threading
import time
#from Move import *

class Screen:
    def __init__(self, win):
        self.win = win
        self.win.geometry("1024x600")
        # self.win.attributes('-fullscreen',True)
        self.myCan = tk.Canvas(self.win, bg="#222222", width="1024", height="600")

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
        self.CoffeeCup()
        self.myCan.update()
        self.myCan.after(500, self.CoffeeSteam())
        self.myCan.update()
        self.myCan.after(1000, self.CoffeeCup())
        self.myCan.delete('all')

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
        self.myCan.delete('all')

class Animation:
    def __init__(self, win):
        self.win = win

    def arm(self, wait, type):
        print("arm")
        # self.move.setTarget(0x05, 4000)
        # self.move.setTarget(0x06, 6000)
        # self.move.setTarget(0x08, 6000)
        # self.move.setTarget(0x09, 4000)
        # self.move.setTarget(0x0a, 6000)
        # self.move.setTarget(0x0b, 6000)
        # time.sleep(1)
        # if type == 'B':
        #     self.BatteArm(wait)
        # elif type == 'CO':
        #     self.CoffeeArm(wait)
        # elif type == 'CH':
        #     self.RechargeArm(wait)
        # elif type == 'T':
        #     self.TrickyArm(wait)
        # elif type == 'F':
        #     self.FunArm(wait)


    def screenControl(self, wait, type):
        print("ya")
        s = Screen(self.win)
        # if type == 'B':
        #     #self.BatteArm(wait)
        if type == 'CO':
            # self.move.setTarget(0x05, 8000)
            # time.sleep(0.1)
            # self.move.setTarget(0x0b, 4000)
            # time.sleep(0.1)
            # self.move.setTarget(0x08, 4000)
            iter = int(wait / 1.5)
            for i in range(iter):
                s.CoffeeScreen()
            # self.move.setTarget(0x05, 4000)
            # time.sleep(0.1)
            # self.move.setTarget(0x0b, 6000)
            # time.sleep(0.1)
            # self.move.setTarget(0x08, 6000)
            # self.move.setTarget(0x00, 6000)
        elif type == 'CH':
            # self.move.setTarget(0x05, 6000)
            # time.sleep(0.1)
            # self.move.setTarget(0x0b, 6000)
            # time.sleep(0.1)
            for i in range(wait / 2):
                # self.move.setTarget(0x06, 4000)
                s.RechargeScreen()
                # self.move.setTarget(0x06, 8000)
                s.RechargeScreen()
                # self.move.setTarget(0x05, 4000)
                # time.sleep(0.1)
                # self.move.setTarget(0x06, 6000)
                # time.sleep(0.1)
                # self.move.setTarget(0x00, 6000)
        # elif type == 'T':
        #     self.TrickyArm(wait)
        # elif type == 'F':
        #     self.FunArm(wait)


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
    #     self.move.setTarget(0x05, 11000)
    #     time.sleep(0.1)
    #     iter = int(wait / 2)
    #     for i in range(iter):
    #         self.move.setTarget(0x0a, 1000)
    #         time.sleep(1)
    #         self.move.setTarget(0x0a, 7000)
    #         time.sleep(1)
    #     self.move.setTarget(0x05, 4000)




