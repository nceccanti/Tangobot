import sys
import pptree
import re
import random

# dict to store definitions
definitions = {}
variables = {}


# Parses text file, txt field is 2D array of text
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
            temp = i.lower().split(":")
            temp[0] = temp[0].strip()
            if len(temp) > 2:
                temp[1] = temp[1].strip()
                temp[2] = temp[2].strip()
            if temp[0].find('~') == 0 and len(temp[0]) > 0:
                definitions[temp[0][1:]] = self.parse_array(temp[1][2:-1])
            elif temp[0].find('#') == -1 and len(temp[0]) > 0:
                if len(temp) != 3:
                    print("ERROR: ", ":".join(temp))
                    print()
                    continue
                self.txt.append(temp)
        #print(self.txt)

    # Creates array for definitions using really ugly regex :(
    def parse_array(self, temp):
        arr = list(temp)
        countq = 0
        for i in range(len(arr)):
            if arr[i] == "\"":
                countq += 1
                if countq % 2 != 0:
                    arr[i] = "("
                else:
                    arr[i] = ")"
        return (re.split(r"\s+(?=[^()]*(?:\(|$))", ''.join(arr)))


class TreeNode(object):
    def __init__(self, name='root', children=None, parent=None):
        self.name = name
        self.parent = parent
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
        node.parent = self
        assert isinstance(node, TreeNode)
        self.children.append(node)

    def disp(self):
        pptree.print_tree(self, 'children', 'name')


class Tree:
    def __init__(self):
        self.root = None
        self.height = 0
        self.nodes = []

    def insert(self, node, parent):
        if parent is not None:
            parent.add_child(node)
        else:
            if self.root is None:
                self.root = node
        self.nodes.append(node)

    def search(self, data):
        index = -1
        for N in self.nodes:
            index += 1
            if N.name == data:
                break
        if index == len(self.nodes) - 1:
            return -1
        else:
            return index

    def getNode(self, id):
        return self.nodes[id]

    def getRoot(self):
        return self.root


# Builds generic tree
def TreeBuilder(text):
    root = TreeNode('root')
    tree = Tree()
    tree.insert(root, None)
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
                current = TreeNode(i[1] + "|" + i[2])
                levelList[index].append(current)
                tree.insert(current, parent)
            except IndexError:
                parent = levelList[index - 1][len(levelList[index - 1]) - 1]
                current = TreeNode(i[1] + "|" + i[2])
                levelList.append([current])
                tree.insert(current, parent)
    return tree


class Dialogue:
    def __init__(self, t):
        self.tree = t
        self.currentSpeech = t.getRoot().name
        self.response = None

    def reset(self):
        self.currentSpeech = self.tree.getRoot().name

    # Gets names of nodes children
    def getChildren(self, name):
        children = []
        for i in self.tree.getNode(self.tree.search(name)).children:
            children.append(i.name)
        return children

    # Checks to see if dialogue is completed
    def isEnd(self):
        if len(self.tree.getNode(self.tree.search(self.currentSpeech)).children) < 1:
            return True
        return False

    # Handles user input, called in while loop below
    def speechInput(self, user):
        user = user.lower()
        user = user.strip()
        prevR = self.response
        children = self.getChildren(self.currentSpeech)
        punct = ",.<>/?;:\'\"\\|]}[{-_=+!@#%$^&*()"
        for i in punct:
            user = user.replace(i, '')
        if user == "exit":
            print("Goodbye!")
            sys.exit(0)
        user = "(" + user + ")"
        for i in children:
            inter = i.split('|')
            if inter[0].find("_") != -1:
                userl = user.strip("()").split(" ")
                expected = inter[0].strip("()").split(" ")
                rwords = inter[1].split(" ")
                name = ""
                value = ""
                match = 0

                matchArray = 0
                iter = 0
                userlMod = 0
                while iter + userlMod < len(userl) and iter < len(expected):
                    if expected[iter] == userl[iter + userlMod]:
                        matchArray += 1
                        iter += 1
                    elif expected[iter] == "_":
                        iter += 1
                    else:
                        userlMod += 1
                print(matchArray, len(expected))
                if matchArray == len(expected) - 1:
                    for word in rwords:
                        if word.find("$") != -1:
                            name = word.strip("$")
                    variables[name] = userl[expected.index("_")]
                    self.currentSpeech = i
                    self.response = inter[1]
            if inter[0].find("~") != -1:
                if user.strip("()") in definitions[inter[0].strip("()~")]:
                    self.currentSpeech = i
                    self.response = inter[1]
            elif inter[0].find(user) != -1:
                self.currentSpeech = i
                if len(inter) > 1:
                    self.response = inter[1]
        if prevR != self.response:
            self.talk(self.response)
        else:
            print("That is not an answer. Try again.")

    # Use this method to print to user
    def talk(self, text):
        punct = "()"
        for i in punct:
            text = text.replace(i, '')
        if text.startswith("~"):
            text = text.replace('~', '')
            if text in definitions:
                c = random.choice(definitions[text])
                for i in punct:
                    c = c.replace(i, '')
                print(c)
        elif text.find("$") != -1:
            textarr = text.split(" ")
            foundVar = False
            for i in range(len(textarr)):
                if textarr[i].find("$") != -1:
                    if textarr[i].strip("$") in variables:
                        textarr[i] = variables[textarr[i].strip("$")]
                        foundVar = True
            if foundVar == True:
                c = ' '.join(textarr)
                print(c)
            else:
                print("I don't know")
                D.reset()
        elif text.startswith("[") and text.endswith("]"):
            text = text.replace('[', '')
            text = text.replace(']', '')
            arr = list(text)
            countq = 0
            for i in range(len(arr)):
                if arr[i] == "\"":
                    countq += 1
                    if countq % 2 != 0:
                        arr[i] = "("
                    else:
                        arr[i] = ")"
            c = random.choice(re.split(r"\s+(?=[^()]*(?:\(|$))", ''.join(arr)))
            print(c.strip("()"))
        else:
            print(text)

    # parses variable from user input
    def parse_variable(self, user, child):
        temp = []
        arr = list(user)
        if arr.find('$') > 0:
            var = (arr.index('$'))
            for i in len(arr):
                while arr[var + i] != ' ' or '':
                    temp.append(arr[var + 1])
            varname = ''.join(temp)
        if arr.find('_') > 0:
            var1 = (arr.index('_'))
            #print(var1)
            for i in len(arr):
                while arr[var1 + i] != ' ' or '':
                    temp.append(arr[var1 + 1])
            varvalue = ''.join(temp)
        variables[varname] = varvalue

P = Parser("chat.txt")
newtree = TreeBuilder(P.txt)
#newtree.root.disp()
D = Dialogue(newtree)
#D.talk(D.currentSpeech)

#print(variables)
while True:
    s = input("Input: ")
    D.speechInput(s)
    if D.isEnd():
        D.reset()
