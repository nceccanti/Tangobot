import sys
from random import *

from Nav import *

class Player:
    def __init__(self, hp, map):
        self.hp = hp
        self.MAXHP = hp
        self.map = map
        self.current = self.map.start
        self.prevPos = self.map.start
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

    #Checks to see if user has reached end point or if user has ran out of health
    def isEnd(self):
        if self.current == self.map.end:
            print("Reach end point!")
            return False
        if self.hp <= 0:
            print('You ran out of health')
            return False
        if self.hp > self.MAXHP:
            self.hp = self.MAXHP
        return True

    #Plays each "turn"
    def playerTurn(self):
        isValid = False
        choices = []
        next = ''
        while isValid == False:
            str = 'Your choices are you go: '
            #print(self.map.nodeList[self.current][2])
            if self.map.nodeList[self.current][2].find('N') > -1:
                str += 'North, '
                choices.append(['north', 'N'])
            if self.map.nodeList[self.current][2].find('W') > -1:
                str += 'West, '
                choices.append(['west', 'W'])
            if self.map.nodeList[self.current][2].find('S') > -1:
                str += 'South, '
                choices.append(['south', 'S'])
            if self.map.nodeList[self.current][2].find('E') > -1:
                str += 'East'
                choices.append(['east', 'E'])
            print(str)
            user = input('What do you choose: ')
            user = user.lower().strip()
            for i in choices:
                if user.find(i[0]) > -1:
                    next = i[1]
            if len(next) > 0:
                isValid = True
        for i in self.map.adjList[self.current].keys():
            if next == self.map.adjList[self.current][i][1]:
                self.prevPos = self.current
                self.current = i
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
            hint = self.map.adjList[self.current][temp[1]][1]
            if hint == 'N':
                print("(Hint): Go North!")
            elif hint == 'S':
                print("(Hint): Go South!")
            elif hint == 'W':
                print("(Hint): Go West!")
            elif hint == 'E':
                print("(Hint): Go East!")

    #Charging station functionality
    def ChargingStation(self):
        self.hp = self.MAXHP
        print("Charging Stations")

    #Coffee shop functionality
    def CoffeeShop(self):
        self.shortestPath()
        print('Coffee Shop')

    #Easy battle functionality
    def EasyBattle(self):
        print('Easy Battle')
        if self.Battle():
            print("Fight!")

    #Medium battle functionality
    def MediumBattle(self):
        print('Medium Battle')
        if self.Battle():
            print("Fight!")

    #Hard battle functionality
    def HardBattle(self):
        print('Hard Battle')
        if self.Battle():
            print("Fight!")

    def Battle(self):
        user = input("Run or fight?: ")
        user = user.lower()
        if user.find("run") != -1:
            self.current = self.prevPos
            return False
        return True

    #Fun functionality
    def FunNode(self):
        #print("You are about to teleport!! Hold on tight!")
        self.current = random.randint(0, self.map.id-1)
        self.NodeController(self.map.nodeList[self.current][3])
        print('Fun Node')

    #Tricky functionality
    def TrickyNode(self):
        riddle = random.choice(self.riddles)
        for i in riddle:
            print(i)
        user = input('Answer: ')
        if int(float(user)) == 1:
            print("You guessed right, 10+ hp!")
            self.hp += 10
        else:
            print("You guessed wrong, 10- hp!")
            self.hp -= 10
        print('Tricky Node')

if __name__ == '__main__':
    n = Nav()
    n.readFile('map2.txt')
    n.postProcess()
    n.addSpecialNodes()
    #print(n.nodeList)
    #print(n.adjList)
    #print(n.id)
    p = Player(100, n)
    #p.TrickyNode()
    while p.isEnd():
        #print(p.current)
        p.playerTurn()