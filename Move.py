import serial, time, sys

class Move:
    def __init__(self, magnitude, usb):
        self.magnitude =  magnitude
        self.usb = usb
        self.center = 5869
    def writeCMD(self, c, target, type):
        lsb =  target &0x7F
        msb = (target >> 7) & 0x7F
        cmd = chr(0xaa) + chr(0xC) + chr(0x04) + c + chr(lsb) + chr(msb)
        print('writing', type)
        self.usb.write(cmd.encode('utf-8'))
        print('reading', type)

    # def controller(self, c):


    # def stop(self):
    #     self.writeCMD(chr(0x00), self.center, "waist halt")
    #     self.writeCMD(chr(0x01), self.center, "move halt")
    #     self.writeCMD(chr(0x02), self.center, "pivot halt")
    #     self.writeCMD(chr(0x03), self.center, "neckside halt")
    #     self.writeCMD(chr(0x04), self.center, "neckvert halt")

    def forwardWheel(self):
        target = self.center - self.magnitude
        self.writeCMD(chr(0x01), target, "forward move")

    def backwardWheel(self):
        target = self.center + self.magnitude
        self.writeCMD(chr(0x01), target, "backward move")

    def pivotLeft(self):
        target = self.center - self.magnitude
        self.writeCMD(chr(0x02), target, "pivot left")

    def pivotRight(self):
        target = self.center + self.magnitude
        self.writeCMD(chr(0x02), target, "pivot right")

    def waistLeft(self):
        target = self.center - self.magnitude
        self.writeCMD(chr(0x00), target, "pivot right")

    def waistRight(self):
        target = self.center + self.magnitude
        self.writeCMD(chr(0x00), target, "pivot right")

    def neckLeft(self):
        target = self.center - self.magnitude
        self.writeCMD(chr(0x03), target, "neck left")

    def neckRight(self):
        target = self.center + self.magnitude
        self.writeCMD(chr(0x03), target, "neck right")

    def neckUp(self):
        target = self.center - self.magnitude
        self.writeCMD(chr(0x04), target, "neck up")

    def neckDown(self):
        target = self.center + self.magnitude
        self.writeCMD(chr(0x04), target, "neck down")