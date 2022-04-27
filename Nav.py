import os

class Nav:
    id = 0
    def __init__(self):
        self.nodeList = dict({})
        self.adjList = dict({})

    def addNode(self, x, y, adj):
        self.nodeList.update({self.id: [x,y,adj]})
        self.adjList[self.id] = dict({})
        self.id += 1

    def addEdge(self, n1, n2):
        self.adjList[n1] = n2
        self.adjList[n2] = n1

    def readFile(self, fileName):
        if os.path.isfile(fileName):
            with open(fileName, 'r') as file:
                f = file.read()
                lines = f.split('\n')
                yLimit = len(lines)
                xlimit = len(lines[0])
                for i in range(len(lines)):
                    for j in range(len(lines[i])):
                        inter = ""
                        if lines[i][j] == '.':
                            if i + 1 < yLimit:
                                if lines[i+1][j] == '.':
                                    inter += 'S'
                            if j + 1 < xlimit:
                                if lines[i][j + 1] == '.':
                                    inter += 'E'
                            if j > 0:
                                if lines[i][j-1] == '.':
                                    inter += 'W'
                            if i > 0:
                                if lines[i-1][j] == '.':
                                    inter += 'N'
                        self.addNode(i, j, inter)
                        print(inter)

    def postProcess(self):
        for i in self.nodeList.keys():
            for j in self.nodeList.keys():
                minIndex1 = -1
                min = -1
                if self.nodeList[i][0] == self.nodeList[j][0] or self.nodeList[i][1] == self.nodeList[j][1]:
                    dist = (self.nodeList[i][0] - self.nodeList[j][0]) + (self.nodeList[i][1] + )

n = Nav()
n.readFile('map.txt')