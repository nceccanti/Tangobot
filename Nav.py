import os
import random

class Nav:
    id = 0
    def __init__(self):
        self.map = None
        self.nodeList = dict({})
        self.adjList = dict({})
        self.xLimit = 0
        self.yLimit = 0
        self.start = 0
        self.end = 0
        self.edgeNodes = []

    #Adds node
    def addNode(self, x, y, adj):
        self.nodeList.update({self.id: [x,y,adj, '']})
        self.adjList[self.id] = dict({})
        self.id += 1

    #Adds edge
    def addEdge(self, n1, n2, dist, direct):
        temp = self.adjList[n1]
        temp[n2] = [dist, direct]
        self.adjList[n1].update(temp)

    #File input
    def readFile(self, fileName):
        if os.path.isfile(fileName):
            with open(fileName, 'r') as file:
                f = file.read()
                lines = f.split('\n')
                self.map = lines
                self.yLimit = len(lines)
                self.xLimit = len(lines[0])
                for i in range(len(lines)):
                    for j in range(len(lines[i])):
                        paths = 0
                        inter = ""
                        if lines[i][j] == '.':
                            if i + 1 < self.yLimit:
                                if lines[i+1][j] == '.':
                                    inter += 'S'
                            if j + 1 < self.xLimit:
                                if lines[i][j + 1] == '.':
                                    inter += 'E'
                            if j > 0:
                                if lines[i][j-1] == '.':
                                    inter += 'W'
                            if i > 0:
                                if lines[i-1][j] == '.':
                                    inter += 'N'
                            isNode = False
                            if len(inter) == 2:
                                if (inter.find("N") > -1 or inter.find("S") > -1) and (inter.find("W") > -1 or inter.find("E") > -1):
                                    isNode = True
                                    #print(inter)
                            elif len(inter) > 0:
                                isNode = True
                                #print(self.id, "bottom")
                            if isNode and i == 0 or j==0 or self.xLimit - 1 == j or self.yLimit - 1 == i:
                                self.edgeNodes.append(self.id)
                            if isNode:
                                self.addNode(j, i, inter)

    #Connects nodes
    def postProcess(self):
        for i in self.nodeList.keys():
            for j in self.nodeList[i][2]:
                modX = 0
                modY = 0
                if j == 'N':
                    modY = 1
                elif j == 'S':
                    modY = -1
                elif j == 'W':
                    modX = 1
                elif j == 'E':
                    modX = -1
                x = self.nodeList[i][0]
                y = self.nodeList[i][1]
                intersect = False
                while intersect == False:
                    x -= modX
                    y -= modY
                    if x < 0 or y < 0 or x > self.xLimit - 1 or y > self.yLimit - 1:
                        intersect = True
                        print("Map error")
                        break;
                    for k in self.nodeList.keys():
                        if self.nodeList[k][0] == x and self.nodeList[k][1] == y and k != i:
                            intersect = True
                            dist = abs(self.nodeList[i][0] - x) + abs(self.nodeList[i][1] - y)
                            self.addEdge(i, k, dist, j)

    #Adds attributes to nodes like coffee shops, etc
    def addSpecialNodes(self):
        CHARGING = 3
        COFFEE = 2
        EASY = 6
        MEDIUM = 5
        HARD = 3
        FUN = 2
        TRICKY = 1

        nodes = []
        for i in range(self.id):
            nodes.append(i)

        self.start = random.choice(self.edgeNodes)
        self.edgeNodes.remove(self.start)
        self.end = random.choice(self.edgeNodes)
        self.current = self.start
        nodes.remove(self.start)
        nodes.remove(self.end)

        i = 0
        while i < CHARGING:
            w = random.choice(nodes)
            nodes.remove(w)
            if len(self.nodeList[w][3]) == 0 and w != self.start and w != self.end:
                self.nodeList[w][3] = 'CH'
                i += 1
        i = 0
        while i < COFFEE:
            w = random.choice(nodes)
            nodes.remove(w)
            if len(self.nodeList[w][3]) == 0 and w != self.start and w != self.end:
                self.nodeList[w][3] = 'CO'
                i += 1
        i = 0
        while i < EASY:
            w = random.choice(nodes)
            nodes.remove(w)
            if len(self.nodeList[w][3]) == 0 and w != self.start and w != self.end:
                self.nodeList[w][3] = 'E'
                i += 1
        i = 0
        while i < MEDIUM:
            w = random.choice(nodes)
            nodes.remove(w)
            if len(self.nodeList[w][3]) == 0 and w != self.start and w != self.end:
                self.nodeList[w][3] = 'M'
                i += 1
        i = 0
        while i < HARD:
            w = random.choice(nodes)
            nodes.remove(w)
            if len(self.nodeList[w][3]) == 0 and w != self.start and w != self.end:
                self.nodeList[w][3] = 'H'
                i += 1
        i = 0
        print(self.nodeList)
        while i < FUN:
            w = random.choice(nodes)
            nodes.remove(w)
            if len(self.nodeList[w][3]) == 0 and w != self.start and w != self.end:
                self.nodeList[w][3] = 'F'
                i += 1
        i = 0
        while i < TRICKY:
            w = random.choice(nodes)
            nodes.remove(w)
            if len(self.nodeList[w][3]) == 0 and w != self.start and w != self.end:
                self.nodeList[w][3] = 'T'
                i += 1
        #print('Nav complete')