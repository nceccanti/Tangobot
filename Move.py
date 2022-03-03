import serial, time, sys

class Move:
    def __init__(self, magnitude, usb):
        self.center = 6001
        self.magnitude = magnitude
        self.usb = usb
        self.targetLinear = self.center
        self.targetPivot = self.center
        self.targetWaist = self.center
        self.targetNeckVert = self.center
        self.targetNeckHort = self.center
        self.limit = self.magnitude
        self.limitNeck = (self.magnitude * 2)

    def writeCMD(self, c, target, type, limit):
        print(c, target, type, limit + self.center, self.center - limit)
        if self.targetLinear > self.center + self.limit:
            self.targetLinear = self.center + self.limit
        if self.targetLinear < self.center - self.limit:
            self.targetLinear = self.center - self.limit
        if self.targetWaist > self.center + self.limit:
            self.targetWaist = self.center + self.limit
        if self.targetWaist < self.center - self.limit:
            self.targetWaist = self.center - self.limit
        if self.targetNeckVert > self.center + self.limitNeck:
            self.targetNeckVert = self.center + self.limitNeck
        if self.targetNeckVert < self.center - self.limitNeck:
            self.targetNeckVert = self.center - self.limitNeck
        if self.targetNeckHort > self.center + self.limitNeck:
            self.targetNeckHort = self.center + self.limitNeck
        if self.targetNeckHort < self.center - self.limitNeck:
            self.targetNeckHort = self.center - self.limitNeck

        if target <= (limit + self.center) and target >= (self.center - limit):
            lsb = target &0x7F
            msb = (target >> 7) & 0x7F
            cmd = chr(0xaa) + chr(0xC) + chr(0x04) + c + chr(lsb) + chr(msb)
            print('writing', type)
            self.usb.write(cmd.encode('utf-8'))
            print('reading', type)
        else:
            print("can't go faster/further")


    def stop(self):
        self.writeCMD(chr(0x00), self.center, "linear halt", self.limit * 3)
        self.writeCMD(chr(0x01), self.center, "linear halt", self.limit * 3)
        self.writeCMD(chr(0x02), self.center, "pivot halt", self.limit * 3)
        self.writeCMD(chr(0x03), self.center, "linear halt", self.limit * 3)
        self.writeCMD(chr(0x04), self.center, "linear halt", self.limit * 3)

    def resetMovement(self):
        self.writeCMD(chr(0x01), 6001, "linear halt", self.limit * 3)
        #self.writeCMD(chr(0x02), self.center, "pivot halt", self.limit)

    def forwardWheel(self):
        # if self.targetPivot != self.center:
        #     self.resetMovement()
        self.targetLinear -= self.magnitude
        self.writeCMD(chr(0x01), self.targetLinear, "forward move", self.limit * 3)

    def backwardWheel(self):
        # if self.targetPivot != self.center:
        #     self.resetMovement()
        self.targetLinear += self.magnitude
        self.writeCMD(chr(0x01), self.targetLinear, "backward move", self.limit * 3)

    def pivotTest(self, num):
        while True:
            self.stop()
            self.targetPivot = num
            self.writeCMD(chr(0x02), self.targetPivot, "pivot left", self.limit * 3)
            time.sleep(2)

    def pivotLeft(self):
        self.backwardWheel()
        time.sleep(0.1)
        self.forwardWheel()
        time.sleep(0.1)
        self.resetMovement()
        newTarg = self.targetPivot - self.magnitude * 3
        self.writeCMD(chr(0x02), newTarg, "pivot left", self.limit * 3)

    def pivotRight(self):
        self.backwardWheel()
        time.sleep(0.1)
        self.forwardWheel()
        time.sleep(0.1)
        self.resetMovement()
        newTarg = self.targetPivot + self.magnitude * 3
        self.writeCMD(chr(0x02), newTarg, "pivot right", self.limit * 3)

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