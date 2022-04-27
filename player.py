from Nav import *

class Player:
    def __init__(self, hp, map):
        self.hp = hp
        self.MAXHP = hp
        self.map = map
        self.current = self.map.start

    #Checks to see if user has reached end point
    def isEnd(self):
        if self.current == self.map.end:
            return False
        return True

    #Plays each "turn"
    def playerTurn(self):
        isValid = False
        choices = []
        next = ''
        while isValid == False:
            print(self.current)
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
                print(self.map.adjList[self.current][i][0])
                self.current = self.map.adjList[self.current][i][0]

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

    #Charging station functionality
    def ChargingStation(self):
        print("Charging Stations")

    #Coffee shop functionality
    def CoffeeShop(self):
        print('Coffee Shop')

    #Easy battle functionality
    def EasyBattle(self):
        print('Easy Battle')

    #Medium battle functionality
    def MediumBattle(self):
        print('Medium Battle')

    #Hard battle functionality
    def HardBattle(self):
        print('Hard Battle')

    #Fun functionality
    def FunNode(self):
        print('Fun Node')

    #Tricky functionality
    def TrickyNode(self):
        print('Tricky Node')

if __name__ == '__main__':
    n = Nav()
    n.readFile('map2.txt')
    n.addNode(0,4,'NS')
    n.addNode(4, 4, 'WE')
    n.addNode(8, 4, 'NS')
    n.postProcess()
    n.addSpecialNodes()
    print(n.adjList)
    p = Player(100, n)
    while p.isEnd():
        p.playerTurn()