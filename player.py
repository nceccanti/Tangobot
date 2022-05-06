import serial
import random
from random import *
from voiceinput import *
from speak import *
from Move import *
from Nav import *
import tkinter as tk
from Animation import *
import time

class Player:
    def __init__(self, hp, map, a, m):
        self.NofT = 0
        self.move = m
        self.voice = VoiceInput()
        self.s = Speaker()
        self.hp = hp
        self.MAXHP = hp
        self.map = map
        self.enemies = {}
        self.current = self.map.start
        self.prevPos = self.map.start
        self.direction = random.choice(self.map.nodeList[self.map.start][2])
        self.animation = a
        self.riddles = [

            [
                "What's white, black and red all over?",
                "(1): Newspaper",
                "(2): Your mom",
                "(3): A zebra"
            ],
            [
                "What has a foot on each side and one in the middle?",
                "(1): A yardstick",
                "(2): Your mom",
                "(3): A leg"
            ]
        ]

    #Feed cardinal directions at node, returns array of ordered pairs of relative direction and corresponding cardinal directions
    def relativeDirection(self, string):
        relativeDir = []
        dir = "WNES"
        #print(string)
        for i in string:
            iter = dir.find(i)
            target = dir.find(self.direction)
            #print(iter, target, i, self.direction)
            moves = 0
            while dir[iter] != self.direction:
                moves += 1
                iter += 1
                if iter >= len(dir):
                    iter = 0
            #print(moves)
            if moves == 0:
                relativeDir.append(["F", i])
            elif moves == 1:
                relativeDir.append(["L", i])
            elif moves == 2:
                relativeDir.append(["B", i])
            elif moves == 3:
                relativeDir.append(["R", i])
            else:
                print('Relative direction error')
        return relativeDir

    #Tells robot to move.  Remember if turning you still have to move forward afterward
    def Move(self, dir):
        self.move.setTarget(0x01, 6000)
        self.move.setTarget(0x02, 6000)
        if dir == 'F':
            self.move.setTarget(0x01, 5000)
            time.sleep(1)
        elif dir == 'B':
            self.move.setTarget(0x02, 7000)
            time.sleep(2.8)
            self.move.setTarget(0x02, 6000)
            self.move.setTarget(0x01, 6000)
            self.move.setTarget(0x01, 5000)
            time.sleep(1)
            self.move.setTarget(0x01, 6000)
        elif dir == 'L':
            self.move.setTarget(0x02, 7000)
            time.sleep(1.4)
            self.move.setTarget(0x02, 6000)
            self.move.setTarget(0x01, 5000)
            time.sleep(1)
            self.move.setTarget(0x01, 6000)
        elif dir == 'R':
            self.move.setTarget(0x02, 5000)
            time.sleep(1)
            self.move.setTarget(0x02, 6000)
            self.move.setTarget(0x01, 5000)
            time.sleep(1)
            self.move.setTarget(0x01, 6000)
        self.move.setTarget(0x02, 6000)
        self.move.setTarget(0x01, 6000)

    def tmt(self):
        if self.NofT > 35:
            self.s.TTS("You have taken too many turns, Game over! Loser")
            print("You have taken too many turns, Game over! Loser")
            return False
        return True

    #Checks to see if user has reached end point or if user has ran out of health
    def isEnd(self):
        if self.current == self.map.end:
            print("Reach end point!")
            return False
        if self.hp <= 0:
            s = Speaker()
            s.TTS("You ran out of health")
            print('You ran out of health')
            return False
        if self.hp > self.MAXHP:
            self.hp = self.MAXHP
        return True

    #Plays each "turn"
    def playerTurn(self):
        isValid = False
        #cardinal = ''
        next = ''
        while isValid == False:
            string = 'Your choices are you go: '
            #print(self.map.nodeList[self.current][2])
            #print(self.map.nodeList[self.current][2])
            #print(self.map.adjList[self.current])
            paths = self.relativeDirection(self.map.nodeList[self.current][2])
            choices = []
            #print(self.map.nodeList[self.current][2])
            print(paths)
            for i in paths:
                if i[0] == 'F':
                    string += 'Forward, '
                    choices.append('forward')
                elif i[0] == "B":
                    string += 'Backward, '
                    choices.append('backward')
                elif i[0] == 'L':
                    string += "Left, "
                    choices.append('left')
                elif i[0] == 'R':
                    choices.append('right')
                    string += 'Right, '
            print(string)
            self.s.TTS(string)
            self.s.TTS("What do you choose?")
            self.NofT += 1
            print(self.enemies)
            #user = input('What do you choose: ')
            user = self.voice.listen(choices)
            user = user.lower().strip()
            for i in range(len(choices)):
                if user.find(choices[i]) > -1:
                    self.move.stop()
                    time.sleep(1)
                    next = paths[i][1]
                    self.Move(paths[i][0])
            if len(next) > 0:
                isValid = True
        for i in self.map.adjList[self.current].keys():
            if next == self.map.adjList[self.current][i][1]:
                self.prevPos = self.current
                self.current = i
                self.direction = next
                print(self.direction, "player")
                break;
        self.NodeController(self.map.nodeList[self.current][3])
        self.animation.initial()
        we = "You have " + str(self.hp) + " health"
        self.s.TTS(we)


    #Selects function based on node attribute
    def NodeController(self, select):
        if select == 'CH':
            self.ChargingStation()
        elif select == 'CO':
            self.CoffeeShop()
        elif select == 'E':
            self.EasyBattle()
        elif select == 'M':
            self.MediumBattle()
        elif select == 'H':
            self.HardBattle()
        elif select == 'F':
            self.FunNode()
        elif select == 'T':
            self.TrickyNode()

    def minDistance(self, dist, sptSet):
        min = float('inf')
        for i in self.map.adjList.keys():
            for j in self.map.adjList[i].keys():
                if dist[j] < min and sptSet[j] == False:
                    min = dist[j]
                    min_index = j
        return min_index

    #Finds shortest path to end node for coffee shop hints
    def shortestPath(self):
        #print(self.map.end, self.current)
        #print(self.map.adjList[self.current])
        dist = []
        sptSet = []
        path = []
        for i in self.map.adjList.keys():
            dist.append(float('inf'))
            sptSet.append(False)
            path.append([i])
        dist[self.current] = 0
        for cout in self.map.adjList.keys():
            x = self.minDistance(dist, sptSet)
            sptSet[x] = True
            for y in self.map.adjList[x].keys():
                if self.map.adjList[x][y][0] > 0 and sptSet[y] == False and dist[y] > dist[x] + self.map.adjList[x][y][0]:
                    dist[y] = dist[x] + self.map.adjList[x][y][0]
                    for j in path[x]:
                        if path[y][len(path[y]) - 1] in self.map.adjList[j]:
                            path[y].append(j)
                        else:
                            break
        temp = path[self.map.end]
        temp.reverse()
        if len(temp) > 1:
            card = self.map.adjList[self.current][temp[1]][1]
            hint = self.relativeDirection(card)[0][0]
            if hint == 'F':
                self.s.TTS("Your hint is to go forward")
                print("(Hint): Go Forward!")
            elif hint == 'B':
                self.s.TTS("Your hint is to go backward")
                print("(Hint): Go Backward!")
            elif hint == 'L':
                self.s.TTS("Your hint is to go left")
                print("(Hint): Go Left!")
            elif hint == 'R':
                self.s.TTS("Your hint is to go right")
                print("(Hint): Go Right!")

    #Charging station functionality
    def ChargingStation(self):
        self.animation.screenControl(5, 'CO', 0)
        self.hp = self.MAXHP
        self.s.TTS("You have reached a charging station, Gaining max health")
        print("Charging Stations")

    #Coffee shop functionality
    def CoffeeShop(self):
        self.animation.screenControl(5, 'CO', 0)
        self.shortestPath()
        self.s.TTS("You have made it to Coffee Shop")
        print('Coffee Shop')

    #Easy battle functionality
    def EasyBattle(self):
        badguys = random.randint(1, 2)
        self.s.TTS("you have ran into " + str(badguys) + " low level adversaries")
        print("you have ran into", str(badguys), "low level adversaries")
        enemy_hp = 0
        enem = []
        if self.current in self.enemies.keys():
            enem = self.enemies[self.current]
            for i in range(len(self.enemies[self.current])):
                enem[i] = enem[i] * 2
        else:
            for i in range(badguys):
                enem.append(random.randint(2, 6) * 3)
            self.enemies[self.current] = enem
        print(enem)
        while len(enem) > 0 and self.hp > 0:
            if self.Battle():
                self.animation.screenControl(5, 'B', len(enem))
                player_dmg = random.randint(5, 26)
                self.hp -= random.randint(1,12)
                if player_dmg >= 23:
                    self.s.TTS("Critical Hit!")
                    print("Critical Hit!")
                enem[0] -= player_dmg
                self.enemies[self.current] = enem
                if enem[0] < 1:
                    enem.pop(0)
                    if len(enem) == 0:
                        self.s.TTS("You killed all the enemy\'s")
                    else:
                        self.s.TTS("You killed an enemy! " + str(len(enem)) + " enemies remain!")
                else:
                    we = "player hp is " + str(self.hp) + ", enemy hp is" + enem[0]
                    self.s.TTS(we)
            else:
                break
        self.map.nodeList[self.current][3] = ''

    #Medium battle functionality
    def MediumBattle(self):
        badguys = random.randint(3, 4)
        self.s.TTS("you have ran into " + str(badguys) + " medium level adversaries")
        print("you have ran into " + str(badguys) + " medium level adversaries")
        enemy_hp = 0
        enem = []
        if self.current in self.enemies.keys():
            enem = self.enemies[self.current]
            for i in range(len(self.enemies[self.current])):
                enem[i] = enem[i] * 2
        else:
            for i in range(badguys):
                enem.append(random.randint(2, 6) * 3)
            self.enemies[self.current] = enem
        print(enem)
        while len(enem) > 0 and self.hp > 0:
            if self.Battle():
                self.animation.screenControl(5, 'B', badguys)
                player_dmg = random.randint(5, 26)
                self.hp -= random.randint(1, 12)
                if player_dmg >= 23:
                    self.s.TTS("Critical Hit!")
                    print("Critical Hit!")
                enem[0] -= player_dmg
                self.enemies[self.current] = enem
                if enem[0] < 1:
                    enem.pop(0)
                    if len(enem) == 0:
                        self.s.TTS("You killed all the enemies")
                    else:
                        self.s.TTS("You killed an enemy! " + str(len(enem)) + " enemies remain!")
                else:
                    we = "player hp is " + str(self.hp) + ", enemy hp is" + enem[0]
                    self.s.TTS(we)
            else:
                break
        self.map.nodeList[self.current][3] = ''

    #Hard battle functionality
    def HardBattle(self):
        badguys = random.randint(5, 6)
        self.s.TTS("you have ran into " + str(badguys) + " hard level adversaries")
        print("you have ran into", str(badguys), "hard level adversaries")
        enemy_hp = 0
        enem = []
        if self.current in self.enemies.keys():
            enem = self.enemies[self.current]
            for i in range(len(self.enemies[self.current])):
                enem[i] = enem[i] * 2
        else:
            for i in range(badguys):
                enem.append(random.randint(2, 6) * 3)
            self.enemies[self.current] = enem
        print(enem)
        while len(enem) > 0 and self.hp > 0:
            if self.Battle():
                self.animation.screenControl(5, 'B', badguys)
                player_dmg = random.randint(5, 26)
                self.hp -= random.randint(1, 12)
                if player_dmg >= 23:
                    self.s.TTS("Critical Hit!")
                    print("Critical Hit!")
                enem[0] -= player_dmg
                self.enemies[self.current] = enem
                if enem[0] < 1:
                    enem.pop(0)
                    if len(enem) == 0:
                        self.s.TTS("You killed all the enemies")
                    else:
                        self.s.TTS("You killed an enemy! " + str(len(enem)) + " enemies remain!")
                else:
                    we = "player hp is " + str(self.hp) + ", enemy hp is " + enem[0]
                    self.s.TTS(we)
            else:
                break
        self.map.nodeList[self.current][3] = ''

    def Battle(self):
        battlechoice = ['run', 'fight']
        print("would you like to run or fight?")
        self.s.TTS("would you like to run or fight?")
        user = self.voice.listen(battlechoice)
        #user = input("Run or fight?: ")
        user = user.lower()
        if user.find("run") != -1:
            if random.randint(1,4) != 1:
                self.s.TTS("you ran away")
                print("you ran away!")
                self.current = random.randint(0, self.map.id-1)
                self.direction = random.choice(self.map.nodeList[self.current][2])
                print(self.direction, "direction")
                #print(self.map.nodeList[self.current][2])
                return False
            else:
                self.s.TTS("You cannot run anymore")
                print("you cant run! :(")
        return True

    #Fun functionality
    def FunNode(self):
        #self.animation.control(5, 'F')
        self.s.TTS("You have reached the fun node, you are about to teleport")
        self.animation.screenControl(5, 'F', 0)
        print("You have reached the fun node, you are about to teleport")
        #print("You are about to teleport!! Hold on tight!")
        self.current = random.randint(0, self.map.id-1)
        self.direction = random.choice(self.map.nodeList[self.current][2])
        time.sleep(2)
        self.NodeController(self.map.nodeList[self.current][3])
        print('Fun Node')

    #Tricky functionality
    def TrickyNode(self):
        answer = ['1']
        self.animation.screenControl(5, 'T', 0)
        self.s.TTS("you have reached the troll under the bridge")
        print("you have reached the troll under the bridge")
        riddle = random.choice(self.riddles)
        for i in riddle:
            self.s.TTS(i)
            print(i)
        #user = input("Answer: ")
        user = self.voice.listen(answer)
        if int(float(user)) == 1:
            self.s.TTS("You guessed right, 10+ hp!")
            print("You guessed right, 10+ hp!")
            self.hp += 10
        else:
            self.s.TTS("You guessed wrong, 10- hp!")
            print("You guessed wrong, 10- hp!")
            self.hp -= 10
        print('Tricky Node')

if __name__ == '__main__':
    usb = ""
    try:
        usb = serial.Serial('/dev/ttyACM0')
    except:
        try:
            usb = serial.Serial('/dev/ttyACM1')
        except:
            print("No serial ports")
            sys.exit(0)
    m = Move(500, usb)
    n = Nav()
    n.readFile('map2.txt')
    n.postProcess()
    n.addSpecialNodes()
    # print(n.nodeList)
    # print(n.adjList)
    # print(n.edgeNodes)
    win = tk.Tk()
    a = Animation(win, m)
    a.initial()
    p = Player(100, n, a, m)
    while p.isEnd() and p.tmt():
        p.playerTurn()
    win.mainloop()