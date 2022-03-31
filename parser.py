import sys
import pptree

#Parses text file, txt field is 2D array of text
class Parser:
    txt = []
    lines = []
    def __init__(self, file):
        try:
            f = open(file, 'r')
            self.lines = f.read().split('\n')
        except:
            print("Dialogue file not found.")
        for i in self.lines:
            temp = i.split(":")
            temp[0] = temp[0].strip()
            if temp[0].find('#') == -1 and len(temp[0]) > 0:
                self.txt.append(temp)
        print(self.txt)

class TreeNode(object):
    def __init__(self, name='root', children=None,parent=None):
        self.name = name
        self.parent=parent
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def __repr__(self):
        return self.name

    def is_root(self):
        if self.parent is None:
            return True
        else:
            return False

    def is_leaf(self):
        if len(self.children) == 0:
            return True
        else:
            return False

    def depth(self):
        if self.is_root():
            return 0
        else:
            return 1 + self.parent.depth()

    def add_child(self, node):
        node.parent=self
        assert isinstance(node, TreeNode)
        self.children.append(node)

    def disp(self):
        pptree.print_tree(self,'children','name')

class Tree:
    def __init__(self):
       self.root=None
       self.height=0
       self.nodes=[]

    def insert(self,node,parent):
        if parent is not None:
            parent.add_child(node)
        else:
            if self.root is None:
                self.root=node
        self.nodes.append(node)

    def search(self,data):
        index=-1
        for N in self.nodes:
            index+=1
            if N.name == data:
                break
        if index == len(self.nodes)-1:
            return -1
        else:
            return index

    def getNode(self,id):
        return self.nodes[id]

    def getRoot(self):
        return self.root

#Builds generic tree
def TreeBuilder(text):
    root=TreeNode('root')
    tree=Tree()
    tree.insert(root,None)
    levelList = []
    levelList.append([root])
    prev = -1
    for i in text:
        if i[0][len(i[0]) - 1] == "u":
            index = 1
        elif i[0][len(i[0]) - 1] == "c" or i[0][len(i[0]) - 1] == "e":
            index = -1
        else:
            index = int(i[0][len(i[0]) - 1]) + 1
        if index > 0:
            try:
                parent = levelList[index - 1][len(levelList[index - 1]) - 1]
                current = TreeNode(i[1])
                levelList[index].append(current)
                tree.insert(current, parent)
            except IndexError:
                parent = levelList[index - 1][len(levelList[index - 1]) - 1]
                current = TreeNode(i[1])
                levelList.append([current])
                tree.insert(current, parent)
    return tree

class Dialogue:
    def __init__(self, t):
        self.tree = t
        self.currentSpeech = t.getRoot().children[0].name

    #Gets names of nodes children
    def getChildren(self, name):
        children = []
        for i in self.tree.getNode(self.tree.search(name)).children:
            children.append(i.name)
        return children

    #Checks to see if dialogue is completed
    def isEnd(self):
        if len(self.tree.getNode(self.tree.search(self.currentSpeech)).children) < 1:
            print("Goodbye!")
            sys.exit(0)

    #Handles user input, called in while loop below
    def speechInput(self, user):
        user = user.lower()
        user = user.strip()
        prev = self.currentSpeech
        children = self.getChildren(self.currentSpeech)
        punct = ",.<>/?;:\'\"\\|]}[{-_=+!@#$%^&*()"
        for i in punct:
            user = user.replace(i, '')
        if user == "exit":
            print("Goodbye!")
            sys.exit(0)
        user = "(" + user + ")"
        for i in children:
            if i.find(user) != -1:
                self.currentSpeech = i
        if prev == self.currentSpeech:
            print("That is not an answer. Try again.")
        else:
            print(self.currentSpeech)
        self.isEnd()

P = Parser("chat.txt")
newtree = TreeBuilder(P.txt)
newtree.root.disp()
D = Dialogue(newtree)
print(D.currentSpeech)
while True:
    s = input("Input: ")
    D.speechInput(s)
