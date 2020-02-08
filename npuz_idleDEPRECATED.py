import os
import sys
import copy
from queue import PriorityQueue, Queue

fileInput = 'n_equals_3/input_3.txt'
fileOutput = 'out_idle.txt'

class Node:
    def __init__(self, puzzle, parent=None, action=""):
        self.state = puzzle
        self.parent = parent
        self.g = 0
        if parent is not None:
            self.g = parent.g + 1
            self.moves = action
        else:
            self.g = 0
            self.moves = action
            
    #Returns heuristic 1, no. of misplaced tiles
    def getHvalue(self):
        h = 0
        for i in range(0, self.state.size):
            for j in range(0, self.state.size):
                if self.state.puzzle[i][j] != self.state.end[i][j] \
                   and int(self.state.puzzle[i][j]) != 0:
                    h += 1
        #print("H", h)
        return h

    def isGoalState(self):
        return self.state.checkPuzzle()

    def getChildren(self):
        children = Queue()
        for action in self.state.moveList:
            tempNode = copy.deepcopy(self.state)
            tempNode.move(action)
            children.put(Node(tempNode, self, action))
        return children
        

class Puzzle:
    def __init__(self, initState, goalState):
        #todo
        self.size = len(initState)
        self.puzzle = initState
        self.end = goalState
        self.zero = (0, 0)
        self.moveList = ["UP", "DOWN", "LEFT", "RIGHT"]
        for i in range(0, self.size):
            for j in range(0, self.size):
                if int(self.puzzle[i][j]) == 0:
                    self.zero = (i, j)
                    
    #prints out puzzle for debugging
    def printP(self):
        for i in range(0, self.size):
            for j in range(0, self.size):
                print(self.puzzle[i][j], " ",end="")
            print("")
            
    #check if Goal is reached
    def checkPuzzle(self):
        if self.puzzle == self.end:
            return True

    #do bubble swap
    def swap(self, a1, a2):
        y1, x1 = a1
        y2, x2 = a2
        temp = self.puzzle[y1][x1]
        self.puzzle[y1][x1] = self.puzzle[y2][x2]
        self.puzzle[y2][x2] = temp

    #Iterate through moves
    def move(self, action):
        if action == "UP":
            if (self.zero[0] != 0):
                self.swap((self.zero[0] - 1, self.zero[1]), self.zero)
                self.zero = (self.zero[0] - 1, self.zero[1])
        if action == "DOWN":
            if (self.zero[0] != self.size - 1):
                self.swap((self.zero[0] + 1, self.zero[1]), self.zero)
                self.zero = (self.zero[0] + 1, self.zero[1])
        if action == "LEFT":
            if (self.zero[1] != 0):
                self.swap((self.zero[0], self.zero[1] - 1), self.zero)
                self.zero = (self.zero[0], self.zero[1] - 1)
        if action == "RIGHT":
            if (self.zero[1] != self.size - 1):
                self.swap((self.zero[0], self.zero[1] + 1), self.zero)
                self.zero = (self.zero[0], self.zero[1] + 1)



class Search:
    def __init__(self, puzzle):
        self.startNode = Node(puzzle)
    
    def aStarOne(self):
        ticks = 0
        currNode = self.startNode
        
        if self.checkSolvable(currNode.state.puzzle) == False:
            return None
        
        openList = PriorityQueue()
        openList.put((currNode.getHvalue(), (ticks, currNode)))
        closedList = {}

        stepCount = 0
        while True:
            stepCount += 1
            if stepCount % 10000 == 0:
                print("step:", stepCount)
            #Check frontier
##            if openList.empty():
##                print("Unsolvable")
##            else:
##                print("~"*8)
##                for i in openList.queue:
##                    print(" - "*2)
##                    print("F:", i[0])
##                    print(i[1][1].state.printP())
##                    print(" - "*2)
##                print("~"*8)
            currNode = openList.get()[1][1]
            #Check if goal
            nodeKey = self.getNodeKey(currNode.state.puzzle)
            #print(nodeKey)
            
            if currNode.isGoalState():
                print(stepCount)
                return currNode
            #Won't visit same state
            closedList[nodeKey] = 1
            if currNode.isGoalState():
                print(stepCount)
                return currNode
            
            children = currNode.getChildren()
            while not children.empty():
                child = children.get()
                childKey = self.getNodeKey(child.state.puzzle)
                if childKey in closedList:
                    continue
                ticks += 1
                openList.put((child.getHvalue()+child.g, (ticks, child)))
            
##            elif nodeKey not in closedList or \
##                 (nodeKey in closedList and closedList[nodeKey] != 1):
##                #check if previously visited state
##                closedList[nodeKey] = 1
##                children = currNode.getChildren()
##                while not children.empty():
##                    child = children.get()
##                    ticks += 1
##                    openList.put((child.getHvalue()+child.g, (ticks, child)))
##
##                del children
##
##            del nodeKey
##            del currNode

        return None

    def getNodeKey(self, puzzle):
        output = ''
        for i in puzzle:
            for j in i:
                output += str(j)
        return output
                    

    #Function to check for solvable state
    def checkSolvable(self, puzzle):
            inversions = 0
            lineList = []
            (y, x) = (0, 0)
            for i in range(0, len(puzzle)):
                for j in range(0, len(puzzle)):
                    lineList.append(puzzle[i][j])
                    if puzzle[i][j] == 0:
                        (y, x) = (i, j)
                        print("Y, X", i, j)

            for i in range(0, len(lineList)-1):
                for j in range(i+1, len(lineList)):
                    if lineList[j] and lineList[i] and lineList[i] > lineList[j]:
                        inversions += 1

            del lineList
            #print(lineList)
            print("INV:", inversions)
            if len(puzzle) % 2 == 1:
                #ODD, must have even inversions
                if (inversions % 2) == 0:
                    print("ODD N, S")
                    return True
                else:
                    print("ODD N, US")
                    return False
            else:
                #EVEN, must have:
                #1) blank on EVEN row & ODD inversions
                #2) blank on ODD row & EVEN inversions
                if (y % 2 == 0 and inversions % 2 == 1) or \
                   (y % 2 == 1 and inversions % 2 == 0):
                    print("EVEN N, S")
                    return True
                else:
                    print("EVEN N, US")
                    return False
                    
            
            

def reconstruct(currentNode):
    path = []
    current = currentNode    
    while current is not None:
        path.append(current.moves)
        current = current.parent
    return path[::-1]

if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file

##    #PROPER USE[1]
##    if len(sys.argv) != 3:
##        raise ValueError("Wrong number of arguments!")
    
    try:
        f = open(fileInput, 'r')
##        #PROPER USE[2]
##        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()
    
    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    print(lines)

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]
    
    #Parse file into 2d list
    i,j = 0, 0
    for line in lines:
        lll = line.split()
        #print(lll)
        ll = [int(x) for x in lll]
        #print(ll)
        for number in ll:
            #print("num:", number)
            if 0 <= number <= max_num:
                init_state[i][j] = int(number)
                j += 1
                if j == n:
                    i += 1
                    j = 0

    #print(init_state)

    #Set goal state
    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    #Initialise the puzzle
    puzzle = Puzzle(init_state, goal_state)
    #prints out initial state
    puzzle.printP()

    #Solve the puzzle
    search = Search(puzzle)
    result = search.aStarOne()

    #PROPER USE[3]
##    with open(sys.argv[2], 'w') as out:
##        if result is None:
##            print("UNSOLVABLE")
##            out.write('UNSOLVABLE')
##        else:
##            path = reconstruct(result)
##            output = ''
##            for action in path:
##                #print(action)
##                output = output + str(action) + '\n'
##            print(output)
##            out.write(output)

    with open(fileOutput, 'w') as out:
        if result is None:
            print("UNSOLVABLE")
            out.write('UNSOLVABLE')
        else:
            path = reconstruct(result)
            output = ''
            for action in path:
                output = output + str(action) + '\n'
            print(output)
            out.write(output)
    







