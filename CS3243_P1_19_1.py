import os
import sys
import copy
import json
from time import time
from Queue import PriorityQueue, Queue
from math import sqrt


moveList = ["UP", "DOWN", "LEFT", "RIGHT"]
mMap = [1, 0, 3, 2]
INVALID = 0
FOUND = -1

### Node Class
# Inputs: puzzle(2d array), parent node(if any), <int>move(if any)
class Node(object):
    def __init__(self, puzzle, parent=None, move=None):
        self.puzzle = puzzle
        self.move = move
        self.key = int(self.getNodeKey(self.puzzle))
        self.parent = parent
 
    def __hash__(self):
        return hash(self.key)
    
    def __eq__(self, other):
        return self.key == other.key
    
    #Swaps the tiles
    def swap(self, data, p1, p2):
        (y1, x1) = p1; (y2, x2) = p2
        temp = data[y1][x1]
        data[y1][x1] = data[y2][x2]
        data[y2][x2] = temp
        
    #Returns a copy of 2d array<2d>
    def getCopy(self):
        copy = []
        for i in range(len(self.puzzle)):
            temp = []
            for j in range(len(self.puzzle)):
                temp.append(self.puzzle[i][j])
            copy.append(temp)
        return copy
    
    #Returns 2d array value in 1d form<str>
    def getNodeKey(self, puzzle):
        output = ''
        for i in puzzle:
            for j in i:
                output += str(j)
        return output
    
    #Return pair containing (y,x) of blank/zero tile
    def findZero(self, puzzle):
        (y, x) = (0, 0)
        for i in range(len(puzzle)):
            for j in range(len(puzzle)):
                if puzzle[i][j] == 0:
                    (y, x) = (i, j)
        return (y, x)

    #Returns list of potential children<list<tuple>>
    def getChildren(self, currNode):
        children = []
        (y, x) = self.findZero(self.puzzle)
        direction = [(y-1, x), (y+1, x), (y, x-1), (y, x+1)] #UP, DOWN, LEFT, RIGHT
        for move in range(len(direction)):
            (y1, x1) = direction[move]
            validFlag = False
            if (move == 0 and y > 0) or (move == 1 and y < (len(self.puzzle) - 1)):
                #Valid to move UP or DOWN
                validFlag = True
            elif (move == 2 and x > 0) or (move == 3 and x < (len(self.puzzle) - 1)):
                #Valid to move LEFT or RIGHT
                validFlag = True
            if validFlag == True:
                tempPuzzle = self.getCopy()
                self.swap(tempPuzzle, (y1,x1), (y,x))
                newNode = Node(tempPuzzle, currNode, move)
                children.append(newNode)
        #Child(in children) contains: Node
        return children

### Puzzle Class
# Inputs: Init State, Goal State
# 'solve' returns list containing moves (or UNSOLVABLE)
class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.timeTaken = 0
        self.nodesPopped = 0
        self.nodesInside = 0
        self.finalMoves = 0
        
    #Check if Goal is reached
    def isGoalState(self, puzzle):
        if puzzle == self.goal_state:
            return True
        
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
                    #print("Y, X", i, j)
                    #print 'Y', 'X', i, j
        for i in range(0, len(lineList)-1):
            for j in range(i+1, len(lineList)):
                if lineList[j] and lineList[i] and lineList[i] > lineList[j]:
                    inversions += 1
        del lineList
        #print 'INVERSIONS:', inversions
        if len(puzzle) % 2 == 1:
            #ODD, must have even inversions
            if (inversions % 2) == 0:
                #print 'ODD length Solvable'
                return True
            else:
                #print 'ODD length Unsolvable'
                return False
        else:
            #EVEN, must have:
            #1) blank on EVEN row & ODD inversions
            #2) blank on ODD row & EVEN inversions
            if (y % 2 == 0 and inversions % 2 == 1) or \
               (y % 2 == 1 and inversions % 2 == 0):
                #print 'EVEN length Solvable'
                return True
            else:
                #print 'EVEN length Unsolvable'
                return False
            
    #Returns movelist from finalNode
    def reconstruct(self, currentNode):
        path = []
        current = currentNode    
        while current is not None:
            if current.move is None:
                break
            path.append(moveList[current.move])
            current = current.parent
        return path[::-1]

    #Returns child PID
    def getTicks(self, currentNode):
        print 'ticks last', currentNode.tick
        path = []
        current = currentNode    
        while current is not None:
            if current.tick == 0:
                break
            path.append(current.tick)
            current = current.parent
        return path[::-1]
    
    #Solves the puzzle using Greedy Best First (suboptimal moves)
    def solve(self):
        startTime = time()
        currNode = Node(self.init_state)
        #self.printP()
        if self.checkSolvable(currNode.puzzle) == False:
            return ["UNSOLVABLE"]
        # 3 Data Structures to keep track of...
        openList = Queue()
        visited = set()
        openList.put(currNode) # STABLEST
        steps = 0 #Nodes popped off frontier
        while True:
            steps += 1
##            if steps % 100000 == 0:
##                print 'step:', steps, 'size', openList.qsize()
##                sys.stdout.flush()
            if openList.empty(): #Empty frontier
                print 'Empty Queue!'
                break
            currNode = openList.get() # STABLEST
            visited.add(currNode)
            if self.isGoalState(currNode.puzzle):
                #print 'Total nodes popped:', steps, 'size', openList.qsize()
                #timeTaken = time() - startTime
                #print 'Time taken:', str(timeTaken)
                #sys.stdout.flush()
                ans = self.reconstruct(currNode)
                self.timeTaken = time() - startTime
                self.nodesPopped = steps
                self.nodesInside = openList.qsize()
                self.finalMoves = len(ans)
                return ans
            for child in currNode.getChildren(currNode):
                #Child is now a Node
                if child not in visited:
                    openList.put(child) # STABLEST
        timeTaken = time() - startTime
        print 'Time taken:', str(timeTaken)
        return ["UNSOLVABLE"]

    #Debugging print 2d array
    def printP(self):
        for i in range(len(self.init_state)):
            for j in range(len(self.init_state)):
                print self.init_state[i][j],
            print ""

if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")
    
    lines = f.readlines()
    
    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]
    
    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0
    
    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'w') as f:
        for answer in ans:
            f.write(answer+'\n')
            print answer
            sys.stdout.flush()
        print "TOTAL", len(ans)
