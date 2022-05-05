import timeit
import tkinter as tk
import _thread, threading
import time
from Move import *

class Animation:
    def __init__(self, move):
        self.move = move

    def arm(self, wait, type):
        self.move.setTarget()
    def screen(self, wait, type):
        print('screen')
        time.sleep(1)

    def BatteArm(self, wait):
        self.move.setTarget(0x05, 8000)
        time.sleep(0.2)
        iter = int(wait / 2)
        for i in range(iter):
            self.move.setTarget(0x09, 8000)
            time.sleep(1)
            self.move.setTarget(0x09, 6000)
            time.sleep(1)
        self.move.setTarget(0x05, 8000)

    def CoffeeArm(self, wait):
        self.move.setTarget(0x05, 4000)
        time.sleep(0.1)
        self.move.setTarget(0x09, 8000)
        time.sleep(0.1)
        self.move.setTarget(0x08, 4000)
        time.sleep(wait)
        self.move.setTarget(0x05, 8000)
        time.sleep(0.1)
        self.move.setTarget(0x09, 4000)
        time.sleep(0.1)
        self.move.setTarget(0x08, 6000)

    def RechargeArm(self, wait):
        self.move.setTarget(0x05, 4000)
        time.sleep(0.1)
        self.move.setTarget(0x0b, 6000)
        time.sleep(0.1)
        self.move.setTarget(0x08, 6000)
        time.sleep(0.1)
        iter = int(wait / 2)
        for i in range(iter):
            self.move.setTarget(0x06, 4000)
            time.sleep(1)
            self.move.setTarget(0x06, 8000)
            time.sleep(1)
        self.move.setTarget(0x05, 6000)

    def TrickyArm(self, wait):
        self.move.setTarget(0x09, 3000)
        time.sleep(wait)
        self.move.setTarget(0x09, 5000)

    def FunArm(self, wait):
        self.move.setTarget(0x05, 2000)
        time.sleep(0.1)
        iter = int(wait / 2)
        for i in range(iter):
            self.move.setTarget(0x0b, 3000)
            time.sleep(1)
            self.move.setTarget(0x0b, 6000)
            time.sleep(1)
        self.move.setTarget(0x05, 4000)

class AnimationController:
    def control(self, time, type, move):
        start = timeit.default_timer()
        inst = Animation(move)
        t1 = threading.Thread(target=inst.arm, args=(time,type))
        t2 = threading.Thread(target=inst.screen, args=(time,type))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        end = timeit.default_timer()
        print(end-start)
        print("Done")

if __name__ == '__main__':
    a = AnimationController
    a.control(1,10,100)




