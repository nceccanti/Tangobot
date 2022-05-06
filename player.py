#import serial
import random
import time
from random import *
#from voiceinput import *
#from speak import *
#from Move import *
from Nav import *
#from Animation import *
import tkinter as tk
from Animation import *

class Player:
    def __init__(self, hp, map):
        self.NofT = 0
        #self.move = move
        #self.voice = VoiceInput()
        #self.s = Speaker()
        self.hp = hp
        self.MAXHP = hp
        self.map = map
        self.enemies = {}
        self.current = self.map.start
        self.prevPos = self.map.start
        self.direction = random.choice(self.map.nodeList[self.map.start][2])
        #self.animation = AnimationController(m)
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
            #self.s.TTS("You have taken too many turns, Game over! Loser")
            print("You have taken too many turns, Game over! Loser")
            return False
        return True

    #Checks to see if user has reached end point or if user has ran out of health
    def isEnd(self):
        if self.current == self.map.end:
            print("Reach end point!")
            return False
        if self.hp <= 0:
            #s = Speaker()
            #s.TTS("You ran out of health")
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
            str = 'Your choices are you go: '
            #print(self.map.nodeList[self.current][2])
            #print(self.map.nodeList[self.current][2])
            #print(self.map.adjList[self.current])
            paths = self.relativeDirection(self.map.nodeList[self.current][2])
            choices = []
            #print(self.map.nodeList[self.current][2])
            print(paths)
            for i in paths:
                if i[0] == 'F':
                    str += 'Forward, '
                    choices.append('forward')
                elif i[0] == "B":
                    str += 'Backward, '
                    choices.append('backward')
                elif i[0] == 'L':
                    str += "Left, "
                    choices.append('left')
                elif i[0] == 'R':
                    choices.append('right')
                    str += 'Right, '
            print(str)
            # self.s.TTS(str)
            # self.s.TTS("What do you choose?")
            self.NofT += 1
            user = input('What do you choose: ')
            #user = self.voice.listen(choices)
            user = user.lower().strip()
            for i in range(len(choices)):
                if user.find(choices[i]) > -1:
                    #self.move.stop()
                    time.sleep(1)
                    next = paths[i][1]
                    #self.Move(paths[i][0])
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
                #self.s.TTS("Your hint is to go forward")
                print("(Hint): Go Forward!")
            elif hint == 'B':
                #self.s.TTS("Your hint is to go backward")
                print("(Hint): Go Backward!")
            elif hint == 'L':
                #self.s.TTS("Your hint is to go left")
                print("(Hint): Go Left!")
            elif hint == 'R':
                #self.s.TTS("Your hint is to go right")
                print("(Hint): Go Right!")

    #Charging station functionality
    def ChargingStation(self):
        #self.animation.control(5, 'CH')
        self.hp = self.MAXHP
        #self.s.TTS("You have reached a charging station, Gaining max health")
        print("Charging Stations")

    #Coffee shop functionality
    def CoffeeShop(self):
        #self.animation.control(5, 'CO')
        self.shortestPath()
        #self.s.TTS("You have made it to Coffee Shop")
        print('Coffee Shop')

    #Easy battle functionality
    def EasyBattle(self):
        #self.s.TTS("you have ran into a low level adversary")
        print('Easy Battle')
        enemy_hp = 0
        if self.current in self.enemies.keys():
            enemy_hp = self.enemies[self.current]*6
        else:
            count = random.randint(2,6)
            enemy_hp = count*6
            self.enemies[self.current] = count

        while enemy_hp > 0 and self.hp > 0:
            if self.Battle():
                #self.animation.control(5, 'B')
                player_dmg = random.randint(5, 26)
                self.hp -= random.randint(1,12)
                if player_dmg >= 23:
                    #self.s.TTS("Critical Hit!")
                    print("Critical Hit!")
                    enemy_hp -= player_dmg
                enemy_hp -= player_dmg
                self.enemies[self.current] = int(enemy_hp/6)
                print("\nplayer hp is", self.hp, "\nenemy hp is", enemy_hp)
            else:
                break
        self.map.nodeList[self.current][3] = ''

    #Medium battle functionality
    def MediumBattle(self):
        #self.s.TTS("you have stumbled on a medium level adversary")
        print('Medium Battle')
        enemy_hp = 0
        if self.current in self.enemies.keys():
            enemy_hp = self.enemies[self.current]*15
        else:
            count = random.randint(2,3)
            enemy_hp = count*15
            self.enemies[self.current] = count

        while enemy_hp > 0 and self.hp > 0:
            if self.Battle():
                #self.animation.control(5, 'B')
                player_dmg = random.randint(5, 26)
                self.hp -= random.randint(3,19)
                if player_dmg >= 23:
                    #self.s.TTS("Critical Hit")
                    print("Critical Hit!")
                    enemy_hp -= player_dmg
                enemy_hp -= player_dmg
                self.enemies[self.current] = int(enemy_hp/15)
                print("\nplayer hp is", self.hp, "\nenemy hp is", enemy_hp)
            else:
                break
        self.map.nodeList[self.current][3] = ''

    #Hard battle functionality
    def HardBattle(self):
        #self.s.TTS("You have ran into a heavily armored enemy")
        print('Hard Battle')
        enemy_hp = 0
        if self.current in self.enemies.keys():
            enemy_hp = self.enemies[self.current]*47
        else:
            count = random.randint(1,2)
            enemy_hp = count*47
            self.enemies[self.current] = count

        while enemy_hp > 0 and self.hp > 0:
            if self.Battle():
                #self.animation.control(5, 'B')
                player_dmg = random.randint(5, 26)
                self.hp -= random.randint(10,22)
                if player_dmg >= 23:
                    #self.s.TTS("Critical Hit")
                    print("Critical Hit!")
                    enemy_hp -= player_dmg
                enemy_hp -= player_dmg
                if enemy_hp > 0 and enemy_hp <=47:
                    self.enemies[self.current] = 1
                print("\nplayer hp is", self.hp, "\nenemy hp is", enemy_hp)
            else:
                break
        self.map.nodeList[self.current][3] = ''

    def Battle(self):
        battlechoice = ['run', 'fight']
        print("would you like to run or fight?")
        #self.s.TTS("would you like to run or fight?")
        #user = self.voice.listen(battlechoice)
        user = input("Run or fight?: ")
        user = user.lower()
        if user.find("run") != -1:
            if random.randint(1,4) != 1:
                #self.s.TTS("you ran away")
                print("you ran away!")
                self.current = random.randint(0, self.map.id-1)
                self.direction = random.choice(self.map.nodeList[self.current][2])
                print(self.direction, "direction")
                #print(self.map.nodeList[self.current][2])
                return False
            else:
                #self.s.TTS("You cannot run anymore buddy")
                print("you cant run! :(")
        return True

    #Fun functionality
    def FunNode(self):
        #self.animation.control(5, 'F')
        #self.s.TTS("You have reached the fun node, you are about to teleport")
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
        #self.animation.control(5, 'T')
        #self.s.TTS("you have reached the troll under the bridge")
        print("you have reached the troll under the bridge")
        riddle = random.choice(self.riddles)
        for i in riddle:
            #self.s.TTS(i)
            print(i)
        user = input("Answer: ")
        #user = self.voice.listen(answer)
        if int(float(user)) == 1:
            #self.s.TTS("You guessed right, 10+ hp!")
            print("You guessed right, 10+ hp!")
            self.hp += 10
        else:
            #self.s.TTS("You guessed wrong, 10- hp!")
            print("You guessed wrong, 10- hp!")
            self.hp -= 10
        print('Tricky Node')

if __name__ == '__main__':
    # usb = ""
    # try:
    #     usb = serial.Serial('/dev/ttyACM0')
    # except:
    #     try:
    #         usb = serial.Serial('/dev/ttyACM1')
    #     except:
    #         print("No serial ports")
    #         sys.exit(0)
    # m = Move(500, usb)
    # n = Nav()
    # n.readFile('map2.txt')
    # n.postProcess()
    # n.addSpecialNodes()
    # print(n.nodeList)
    # print(n.adjList)
    # print(n.edgeNodes)
    # p = Player(100, n)
    win = tk.Tk()
    a = Animation(win)
    a.initial()
    time.sleep(5)
    a.screenControl(5, 'CH')
    time.sleep(1)
    a.screenControl(5, "CO")
    win.mainloop()
    # while p.isEnd() and p.tmt():
    #     p.playerTurn()
