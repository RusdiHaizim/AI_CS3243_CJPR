import os
import sys
import copy
from queue import PriorityQueue, Queue
from math import sqrt

moveList = ["UP", "DOWN", "LEFT", "RIGHT"]
mMap = [1, 0, 3, 2]
finalGoal = []

class Node:
    def __init__(self, puzzle, parent=None, action=-1):
        self.state = puzzle
        self.parent = parent
        self.g = 0
        #if parent exists, increment distance/step from parent's
        if parent is not None:
            self.g = parent.g + 1
        else:
            self.g = 0
        self.moves = action
        #self.key = self.getNodeKey(self.state.puzzle)
        self.key = int(self.getNodeKey(self.state.puzzle)) + self.g
        #print(self.key)
            
    #Returns heuristic 1, no. of misplaced tiles
    def getHvalue(self):
        #Scrub heuristic
        #return self.getMisplacedValue()
        
        #Slightly less scrub heuristic
        return self.getManhattanValue()

        #Testing Euclid heuristic
        #return self.getEuclideanValue()*1.01
        
        #Legit Combined
        #h3 = self.getEuclideanValue() + self.getManhattanValue()
        #h3 /= 2
        #return h3

        #Tes
        #h5 = self.getMisplacedValue() + self.getManhattanValue() + self.getEuclideanValue()
        #h5 /= 3
        #return h5

    def getMisplacedValue(self):
        h = 0
        size = len(self.state.puzzle)
        for i in range(0, size):
            for j in range(0, size):
                if self.state.puzzle[i][j] != finalGoal[i][j] \
                   and int(self.state.puzzle[i][j]) != 0:
                    h += 1
        #print("H", h)
        return h
        
    def getManhattanValue(self):
        h = 0
        size = len(self.state.puzzle)
        for i in range(0, size):
            for j in range(0, size):
                num = self.state.puzzle[i][j]
                #print("num:", num, " ", end='')
                if num != 0:
                    rowGoal = (num - 1) // size
                    colGoal = (num - 1) % size
                    diffRow = abs(rowGoal - i)
                    diffCol = abs(colGoal - j)
                    dist = diffRow + diffCol
                    h += dist
                    #print("man", dist)
        #print("manTotal", h)
        linearCon = 0
        linearCon = self.getLinearConflict()
        return h + linearCon

    def getLinearConflict(self):
        size = len(self.state.puzzle)
        inCol = [0]*(size**2)
        inRow = [0]*(size**2)
        conflicts = 0
        #Precompute bools for numbers in right row and col
        for y in range(size):
            for x in range(size):
                num = self.state.puzzle[y][x]
                rowGoal = (num - 1) // size
                colGoal = (num - 1) % size
                inRow[num] = (rowGoal == y)
                inCol[num] = (colGoal == x)
        #Traverse board to check if linear conflict exists
        for y in range(size):
            for x in range(size):
                num = self.state.puzzle[y][x]
                if self.state.puzzle[y][x] == 0:
                    continue
                #check if num is inside column
                if inCol[num]:
                    #check downwards for conflict(AVOID DOUBLE COUNT)
                    for r in range(y, size):
                        numCol = self.state.puzzle[r][x]
                        if self.state.puzzle[r][x] == 0:
                            continue
                        if inCol[numCol] and \
                           self.state.puzzle[r][x] < self.state.puzzle[y][x]:
                            conflicts += 1
                #check if num is inside row
                if inRow[num]:
                    #check rightwards for conflict(SAME AVOID)
                    for c in range(x, size):
                        numRow = self.state.puzzle[y][c]
                        if self.state.puzzle[y][c] == 0:
                            continue
                        if inRow[numRow] and \
                           self.state.puzzle[y][c] < self.state.puzzle[y][x]:
                            conflicts += 1                
        #print("conflicts:", conflicts)
        return 2 * conflicts

    def getEuclideanValue(self):
        h = 0
        size = len(self.state.puzzle)
        for i in range(0, size):
            for j in range(0, size):
                num = self.state.puzzle[i][j]
                if num != 0:
                    rowGoal = (num - 1) // size
                    colGoal = (num - 1) % size
                    dist = sqrt( (rowGoal - i)**2 + (colGoal - j)**2 )
                    h += dist
        #print("euclid", h)
        return h

    def isGoalState(self):
        return self.state.checkPuzzle()

    def swap(self, puzzle, p1, p2):
        (y1, x1) = p1
        (y2, x2) = p2
        temp = puzzle[y1][x1]
        puzzle[y1][x1] = puzzle[y2][x2]
        puzzle[y2][x2] = temp

    def getNodeKey(self, puzzle):
        output = ''
        for i in puzzle:
            for j in i:
                output += str(j)
        return output

    def copy(self, puzzle):
        copy = []
        for i in range(0, len(puzzle)):
            temp = []
            for j in range(0, len(puzzle)):
                temp.append(puzzle[i][j])
            copy.append(temp)
        return copy

    def findZero(self, puzzle):
        (y, x) = (0, 0)
        for i in range(0, len(puzzle)):
            for j in range(0, len(puzzle)):
                if puzzle[i][j] == 0:
                    (y, x) = (i, j)
        return (y, x)

    def getChildren(self):
        #children contains a child(of 3 elements)
        #child contains: puzzle, action(str), nodekey
        children = []
        (y, x) = self.findZero(self.state.puzzle)
        #print("Original", "(y, x)", y, x)
        moves = [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]
        iniPuzzle = self.state.puzzle
        for action in range(0, len(moves)):
            (y1, x1) = moves[action]
            flag = False
            if action == 0 and y > 0:
                #move up
                flag = True
            elif action == 1 and y < (self.state.size - 1):
                #move down
                flag = True
            elif action == 2 and x > 0:
                #move left
                flag = True
            elif action == 3 and x < (self.state.size - 1):
                #move right
                flag = True

            if flag == True:
                tempPuzzle = self.copy(iniPuzzle)
                self.swap(tempPuzzle, (y1, x1), (y, x))
                #print("New", "(y, x)", y1, x1)
                children.append( (tempPuzzle,\
                                action, \
                                str(tempPuzzle)) )
            
        return children
        

class Puzzle:
    def __init__(self, initState):
        #todo
        self.size = len(initState)
        self.puzzle = initState
        #self.end = goalState
                    
    #prints out puzzle for debugging
    def printP(self):
        for i in range(0, self.size):
            for j in range(0, self.size):
                print(self.puzzle[i][j], " ",end="")
            print("")
            
    #check if Goal is reached
    def checkPuzzle(self):
        if self.puzzle == finalGoal:
            return True

class Search:
    def __init__(self, puzzle):
        self.startNode = Node(puzzle)
    
    def aStarOne(self):
        #ticks = 0
        currNode = self.startNode
        
        if self.checkSolvable(currNode.state.puzzle) == False:
            return None
        
        openList = PriorityQueue()
        openList.put((currNode.getHvalue(), (currNode.key, currNode)))
        closedList = {}
        openMap = {}
        openMap[currNode.key] = currNode

        stepCount = 0
        while True:
            stepCount += 1
            if stepCount % 10000 == 0:
                print("step:", stepCount)
            #Check frontier
            if openList.empty():
                print("Unsolvable")
                return None
##            else:
##                print("~"*4)
##                for i in openList.queue:
##                    print(" - "*2)
##                    print("F:", i[0])
##                    print(i[1][1].state.printP())
##                    print(" - "*2)
##                print("~"*8)
            
            currNode = openList.get()[1][1]
            #Check if goal
            nodeKey = currNode.key
            #print(nodeKey)

            #Won't visit same state
            closedList[nodeKey] = 1
            if currNode.isGoalState():
                print(stepCount)
                return currNode
            
            children = currNode.getChildren()
            #child contains: puzzle, action(int), nodekey
            #child IS NOT A NODE
            for child in children:
                #check if previously visited child, using nodekey
                if child[2] in closedList:
                    continue
                #ticks += 1
                if child[1] == mMap[currNode.moves]:
                    continue
                newPuz = copy.deepcopy(currNode.state)
                #change initial state of puzzle only
                newPuz.puzzle = child[0]
                
                newNode = Node(newPuz, currNode, child[1])
                if newNode.key in openMap:
                    continue
                openList.put( (newNode.getHvalue() + newNode.g,\
                               (newNode.key, newNode)) )
                openMap[newNode.key] = newNode
            
        return None
    
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
        if current.moves == -1:
            break
        path.append(moveList[current.moves])
        current = current.parent
    return path[::-1]

if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file

    #PROPER USE[1]
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")
    
    try:
        #f = open("n_equals_3/input_2.txt", 'r')
        #PROPER USE[2]
        f = open(sys.argv[1], 'r')
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
    finalGoal = goal_state

    #Initialise the puzzle
    #puzzle = Puzzle(init_state, goal_state)
    puzzle = Puzzle(init_state)
    #prints out initial state
    puzzle.printP()

    #Solve the puzzle
    search = Search(puzzle)
    result = search.aStarOne()

    #PROPER USE[3]
    with open(sys.argv[2], 'w') as out:
        if result is None:
            print("UNSOLVABLE")
            out.write('UNSOLVABLE')
        else:
            path = reconstruct(result)
            output = ''
            for action in path:
                #print(action)
                output = output + str(action) + '\n'
            print(output)
            out.write(output)
            print("TOTAL:", len(path))
    







