import time, sys
# import serial

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
        self.limit = self.magnitude
        self.limitNeck = (self.magnitude * 2)

    def sendCmd(self, cmd):
        cmdStr = chr(0xaa) + chr(0x0c) + cmd
        self.usb.write(bytes(cmdStr, 'latin-1'))

    def setTarget(self, chan, target):
        print(chan, target)
        lsb = target & 0x7f  # 7 bits for least significant byte
        msb = (target >> 7) & 0x7f  # shift 7 and take next 7 bits for msb
        cmd = chr(0x04) + chr(chan) + chr(lsb) + chr(msb)
        self.sendCmd(cmd)

    def stop(self):
        self.setTarget(0x00, 6000)
        self.setTarget(0x01, 6000)
        self.setTarget(0x02, 6000)
        self.setTarget(0x03, 6000)
        self.setTarget(0x04, 6000)

    def forward(self):
        self.setTarget(0x01, 5000)
        time.sleep(1)
        self.setTarget(0x01, 6000)

    def leftTurn(self):
        self.setTarget(0x02, 7000)
        time.sleep(1)
        self.setTarget(0x02, 6000)

    def rightTurn(self):
        self.setTarget(0x02, 5000)
        time.sleep(1)
        self.setTarget(0x02, 6000)

    def backward(self):
        self.setTarget(0x01, 7000)
        time.sleep(1)
        self.setTarget(0x01, 6000)

    # def forwardWheel(self):
    #     if self.targetLinear == self.center or 6200 == self.targetLinear:
    #         self.targetLinear -= 200
    #     else:
    #         self.targetLinear -= self.magnitude
    #     self.setTarget(0x01, self.targetLinear)
    #
    # def backwardWheel(self):
    #     if self.targetLinear == self.center or 5800 == self.targetLinear:
    #         self.targetLinear += 200
    #     else:
    #         self.targetLinear += self.magnitude
    #     self.setTarget(0x01, self.targetLinear)
    #
    #
    # def pivotLeft(self):
    #     self.stop()
    #     self.setTarget(0x02, 6700)
    #
    # def pivotRight(self):
    #     self.stop()
    #     self.setTarget(0x02, 5300)
    #
    # def waistLeft(self):
    #     self.targetWaist += self.magnitude
    #     self.setTarget(0x00, self.targetWaist)
    #
    # def waistRight(self):
    #     self.targetWaist -= self.magnitude
    #     self.setTarget(0x00, self.targetWaist)
    #
    # def neckLeft(self):
    #     self.targetNeckHort += self.magnitude
    #     self.setTarget(0x03, self.targetNeckHort)
    #
    # def neckRight(self):
    #     self.targetNeckHort -= self.magnitude
    #     self.setTarget(0x03, self.targetNeckHort)
    #
    # def neckUp(self):
    #     self.targetNeckVert += self.magnitude
    #     self.setTarget(0x04, self.targetNeckVert)
    #
    # def neckDown(self):
    #     self.targetNeckVert -= self.magnitude
    #     self.setTarget(0x04, self.targetNeckVert)