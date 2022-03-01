import serial, time, sys

class Move:
    def __init__(self, magnitude, usb):
        self.magnitude = 500
        self.usb = usb
        self.targetLinear = 5869
        self.targetPivot = 5869
        self.targetWaist = 5869
        self.targetNeckVert = 5869
        self.targetNeckHort = 5869

    def writeCMD(self, c, target, type):
        lsb =  target &0x7F
        msb = (target >> 7) & 0x7F
        cmd = chr(0xaa) + chr(0xC) + chr(0x04) + c + chr(lsb) + chr(msb)
        print('writing', type)
        self.usb.write(cmd.encode('utf-8'))
        print('reading', type)

    def forwardWheel(self):
        self.targetLinear -= self.magnitude
        self.writeCMD(chr(0x01), self.targetLinear, "forward move")

    def backwardWheel(self):
        self.targetLinear += self.magnitude
        self.writeCMD(chr(0x01), self.targetLinear, "backward move")

    def pivotLeft(self):
        self.targetPivot -= self.magnitude
        self.writeCMD(chr(0x02), self.targetPivot, "pivot left")

    def pivotRight(self):
        self.targetPivot += self.magnitude
        self.writeCMD(chr(0x02), self.targetPivot, "pivot right")

    def waistLeft(self):
        self.targetWaist -= self.magnitude
        self.writeCMD(chr(0x00), self.targetWaist, "pivot right")

    def waistRight(self):
        self.targetWaist += self.magnitude
        self.writeCMD(chr(0x00), self.targetWaist, "pivot right")

    def neckLeft(self):
        self.targetNeckHort -= self.magnitude
        self.writeCMD(chr(0x03), self.targetNeckHort, "neck left")

    def neckRight(self):
        self.targetNeckHort += self.magnitude
        self.writeCMD(chr(0x03), self.targetNeckHort, "neck right")

    def neckUp(self):
        self.targetNeckVert -= self.magnitude
        self.writeCMD(chr(0x04), self.targetNeckVert, "neck up")

    def neckDown(self):
        self.targetNeckVert += self.magnitude
        self.writeCMD(chr(0x04), self.targetNeckVert, "neck down")