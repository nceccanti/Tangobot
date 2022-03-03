import serial, time, sys

class Move:
    def __init__(self, magnitude, usb):
        self.center = 6000
        self.magnitude = magnitude
        self.usb = usb
        self.targetLinear = self.center
        self.targetPivot = self.center
        self.targetWaist = self.center
        self.targetNeckVert = self.center
        self.targetNeckHort = self.center
        self.limit = (self.magnitude * 3)
        self.limitNeck = (self.magnitude * 5)

    def writeCMD(self, c, target, type, limit):
        print(c, target, type, limit + self.center, self.center - limit)
        # if target <= (limit + self.center) and target >= (self.center - limit):
        lsb =  target &0x7F
        msb = (target >> 7) & 0x7F
        cmd = chr(0xaa) + chr(0xC) + chr(0x04) + c + chr(lsb) + chr(msb)
        print('writing', type)
        self.usb.write(cmd.encode('utf-8'))
        print('reading', type)
        # else:
        #     print("can't go faster/further")

    def stop(self):
        self.writeCMD(chr(0x00), self.center, "linear halt", self.limit)
        self.writeCMD(chr(0x01), self.center, "pivot halt", self.limit)
        self.writeCMD(chr(0x02), self.center, "waist halt", self.limit)
        self.writeCMD(chr(0x03), self.center, "neckhort halt", self.limitNeck)
        self.writeCMD(chr(0x04), self.center, "neckvert halt", self.limitNeck)

    def resetMovement(self):
        self.writeCMD(chr(0x00), self.center, "linear halt", self.limit)
        self.writeCMD(chr(0x01), self.center, "pivot halt", self.limit)

    def forwardWheel(self):
        # if self.targetPivot != self.center:
        #     self.resetMovement()
        self.targetLinear -= self.magnitude
        self.writeCMD(chr(0x01), self.targetLinear, "forward move", self.limit)

    def backwardWheel(self):
        # if self.targetPivot != self.center:
        #     self.resetMovement()
        self.targetLinear += self.magnitude
        self.writeCMD(chr(0x01), self.targetLinear, "backward move", self.limit)

    def pivotTest(self, num):
        # if self.targetLinear != self.center:
        #     self.resetMovement()
        self.targetPivot = num
        self.writeCMD(chr(0x02), self.targetPivot, "pivot left", self.limit)

    def pivotLeft(self):
        # if self.targetLinear != self.center:
        #     self.resetMovement()
        self.targetPivot -= self.magnitude
        self.writeCMD(chr(0x02), self.targetPivot, "pivot left", self.limit)

    def pivotRight(self):
        # if self.targetLinear != self.center:
        #     self.resetMovement()
        self.targetPivot += self.magnitude
        self.writeCMD(chr(0x02), self.targetPivot, "pivot right", self.limit)

    def waistLeft(self):
        self.targetWaist -= self.magnitude
        self.writeCMD(chr(0x00), self.targetWaist, "pivot right", self.limit)

    def waistRight(self):
        self.targetWaist += self.magnitude
        self.writeCMD(chr(0x00), self.targetWaist, "pivot right", self.limit)

    def neckLeft(self):
        self.targetNeckHort -= self.magnitude
        self.writeCMD(chr(0x03), self.targetNeckHort, "neck left", self.limitNeck)

    def neckRight(self):
        self.targetNeckHort += self.magnitude
        self.writeCMD(chr(0x03), self.targetNeckHort, "neck right", self.limitNeck)

    def neckUp(self):
        self.targetNeckVert -= self.magnitude
        self.writeCMD(chr(0x04), self.targetNeckVert, "neck up", self.limitNeck)

    def neckDown(self):
        self.targetNeckVert += self.magnitude
        self.writeCMD(chr(0x04), self.targetNeckVert, "neck down", self.limitNeck)