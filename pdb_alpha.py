import os
import sys
import json
import copy
from Queue import PriorityQueue, Queue
from math import sqrt

moveList = ["UP", "DOWN", "LEFT", "RIGHT"]
mMap = [1, 0, 3, 2]
finalGoal = []
PDB4_3 = 3360
FINISHED = -1
pdb33a = {0:0, 2:0, 3:0, 4:0}
pdb33b = {2:0, 3:0, 4:0}

def getP3(puzzle, pattern):
    output = ''
    tempMap = {}
    for key in pattern:
        tempMap[key] = 0
        #print 'keyA', key
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] in pattern:
                temp = ''
                temp += str(i+1)
                temp += str(j+1)
                tempMap[puzzle[i][j]] = temp
                #print 'num',puzzle[i][j],i,j
    for key in tempMap:
        output += tempMap[key]
        #print 'keyB', key, 'value', tempMap[key]
    return output

###
class Node:
    #PDB node contains
    #state, parent, moves
    #cost
    def __init__(self, puzzle, parent=None, action=None):
        self.state = puzzle
        self.parent = parent
        self.g = 0
        #self.h = self.getHvalue()
        self.movelist = []
        self.cost = 0
        #if parent exists, increment distance/step from parent's
        if parent is not None:
            self.g = parent.g + 1
            self.cost = parent.cost
            if self.parent.movelist is None:
                self.movelist = [moveList[action]]
            else:
                self.movelist = copy.deepcopy(self.parent.movelist)
                self.movelist.append(moveList[action])
        else:
            self.g = 0
            self.movelist = None
        self.moves = action
        self.key = int(self.getNodeKey(self.state.puzzle))
            
    def getHvalue(self):
        return self.getManhattanValue()
        
    def getManhattanValue(self):
        h = 0
        size = len(self.state.puzzle)
        for i in range(0, size):
            for j in range(0, size):
                num = self.state.puzzle[i][j]
                if num != 0:
                    rowGoal = (num - 1) // size
                    colGoal = (num - 1) % size
                    diffRow = abs(rowGoal - i)
                    diffCol = abs(colGoal - j)
                    dist = diffRow + diffCol
                    h += dist
        linearCon = 0
        linearCon = self.getLinearConflict()
        manTotal = h + linearCon*2
        return manTotal

    def getLinearConflict(self):
        size = len(self.state.puzzle)
        inCol = [0]*(size**2)
        inRow = [0]*(size**2)
        conflicts = 0
        #Precompute coordinates for all the numbers
        for y in range(size):
            for x in range(size):
                num = self.state.puzzle[y][x]
                rowGoal = (num - 1) // size
                colGoal = (num - 1) % size
                inRow[num] = rowGoal
                inCol[num] = colGoal
        #Check row conflicts
        for r in range(size):
            for cI in range(size):
                for cN in range(cI+1, size):
                    if self.state.puzzle[r][cI] and self.state.puzzle[r][cN] and\
                       r == inRow[self.state.puzzle[r][cI]] and\
                       inRow[self.state.puzzle[r][cI]] == inRow[self.state.puzzle[r][cN]] and\
                       inCol[self.state.puzzle[r][cI]] > inCol[self.state.puzzle[r][cN]]:
                        #Conflict exists!
                        conflicts += 1
        #Check col conflicts
        for c in range(size):
            for rI in range(size):
                for rN in range(rI+1, size):
                    if self.state.puzzle[rI][c] and self.state.puzzle[rN][c] and\
                       c == inCol[self.state.puzzle[rI][c]] and\
                       inCol[self.state.puzzle[rI][c]] == inCol[self.state.puzzle[rN][c]] and\
                       inRow[self.state.puzzle[rI][c]] > inRow[self.state.puzzle[rN][c]]:
                        #Conflict exists!
                        conflicts += 1
        return conflicts

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
        #children(list) contains a child(tuple)
        #child contains: (puzzle, action(str), nodekey)
        children = []
        (y, x) = self.findZero(self.state.puzzle)
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
                children.append( (tempPuzzle,\
                                action, \
                                str(tempPuzzle)) )
        return children
    
    def getNeighbour(self, pattern, pattern0):
        children = []
        (y, x) = self.findZero(self.state.puzzle)
        moves = [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]
        iniPuzzle = self.state.puzzle
        for action in range(len(moves)):
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
                cost = 0
                #if neighbour is inside pattern, add to the cost
                #pdb33a = {2:0, 3:0, 4:0, 0:0}
                #pdb33b = {2:0, 3:0, 4:0}
                if tempPuzzle[y1][x1] in pattern:
                    #print tempPuzzle[y1][x1], 'in', y1, x1
                    #print 'swapping', y1, x1, 'with', y, x
                    cost += 1
                self.swap(tempPuzzle, (y1, x1), (y, x))
                newKey = getP3(tempPuzzle, pattern0)
                #print 'zero @', self.findZero(tempPuzzle), newKey
                #print 'newKey', newKey
                children.append( (tempPuzzle,\
                                action, \
                                newKey, \
                                  cost, \
                                  int(self.getNodeKey(tempPuzzle))) )
        return children
            
        
### Class 'Puzzle' to store initial state
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
                #print(self.puzzle[i][j], " ",end="")
                print self.puzzle[i][j],
            #print("")
            print ""
            
    #check if Goal is reached
    def checkPuzzle(self):
        if self.puzzle == finalGoal:
            return True

### Class 'Search' to run path-finding algorithm
class Search:
    def __init__(self, puzzle):
        self.startNode = Node(puzzle)

    def generate4x4(self):
        currNode = self.startNode
        #Frontier to pop off more nodes
        openList = Queue()
        #Start from goal state
        openList.put(currNode)
        #Visited list: key(2d key), value(node.g)
        #closedList = {12131444:0}
        #Visited list wo blank: key(pdb33a), value(cost)
        p3 = {121314:0}
        #pdb33a: 0, pdb33b: no 0
        stepCount = 0
        while True:
            stepCount += 1
            if stepCount % 10000 == 0:
                #print("step:", stepCount)
                print "step:", stepCount
                print 'hashTable size', len(p3)
            if openList.empty():
                print "EMPTY FRONTIER, help"
                return None
            currNode = openList.get()
            patKey = getP3(currNode.state.puzzle, pdb33a)
            #set visited list to curr dist
            #if visited with less g, then prune that search branch
            #closedList[currNode.key] = currNode.g
            #if len(p3) >= PDB4_3:
            if len(p3) >= 1000:
                print 'FINISHED'
                self.storeHash(p3)
                return FINISHED
            #child: puzzle, action(int), patternkey0, cost, nodekey
            for child in currNode.getNeighbour(pdb33b, pdb33a):
                if currNode.moves is not None and child[1] == mMap[currNode.moves]:
                    #print 'b: prevMove'
                    continue
                newPuz = copy.deepcopy(currNode.state)
                newPuz.puzzle = child[0]
                newNode = Node(newPuz, currNode, child[1])
                newNode.cost += child[3]
                hashKey = getP3(child[0], pdb33b)
                
##                print '*'*10
##                newNode.state.printP()
##                print 'key0:', child[2]
##                print 'step:', newNode.g, 'dir:', moveList[child[1]]
##                print 'hashCost:', newNode.cost
##                print '*'*10
                
##                if child[4] in closedList and closedList[child[4]] <= newNode.g:
##                    #prune search if less than g
##                    #print 'a: closedList'
##                    #print 'closedList', child[4],'old',closedList[child[4]],'new',newNode.g
##                    del newNode, newPuz
##                    continue
##                elif child[4] in closedList and closedList[child[4]] > newNode.g:
##                    print 'wow'
                
                #print hashKey
                if hashKey in p3:
                    if p3[hashKey] < newNode.cost:
                        #print 'hashTable: same'
                        continue
                    elif newNode.cost < p3[hashKey]:
##                        print 'hashTable: lower g changed!'
##                        newNode.state.printP()
##                        print 'old',p3[hashKey],'new',newNode.cost
##                        print 'g', newNode.g, newNode.movelist
##                        print currNode.cost
                        p3[hashKey] = newNode.cost
                else:
                    p3[hashKey] = newNode.cost 
                openList.put(newNode)
        print 'GG end of while loop'
        return None
    
    def storeHash(self, hashTable):
        with open('pdbTest.json', 'w') as f:
            json.dump(hashTable, f, indent=4, sort_keys=True)
                        
            
        
    
##    def aStarOne(self):
##        currNode = self.startNode
##        if self.checkSolvable(currNode.state.puzzle) == False:
##            return None
##        openList = PriorityQueue()
##        openList.put((currNode.h, (currNode.key, currNode)))
##        closedList = {}
##        openMap = {}
##        openMap[currNode.key] = currNode
##        stepCount = 0
##        while True:
##            stepCount += 1
##            if stepCount % 10000 == 0:
##                print "step:", stepCount
##            #Check frontier if empty
##            if openList.empty():
##                #print("Unsolvable")
##                print "Unsolvable"
##                return None
##            currNode = openList.get()[1][1]
##            nodeKey = currNode.key
##            #Set state to visited
##            closedList[nodeKey] = 1
##            #Current node is the GOAL!!!
##            if currNode.isGoalState():
##                #print(stepCount)
##                print 'Total steps:', stepCount
##                return currNode
##            #child contains: (puzzle, action(int), nodekey)
##            #child IS NOT A NODE!!! its a tuple...
##            for child in currNode.getChildren():
##                #If previously visited child, skip child
##                if child[2] in closedList:
##                    continue
##                #If parent is not first node popped AND
##                #If child's move does not lead back to parent
##                #THEN skip child
##                if currNode.moves is not None and child[1] == mMap[currNode.moves]:
##                    continue
##                #Copies parent' puzzle, changing only initial state
##                newPuz = copy.deepcopy(currNode.state)
##                newPuz.puzzle = child[0]
##                
##                newNode = Node(newPuz, currNode, child[1])
##                #Checks if child state in openMap
##                #If in openMap and more moves needed, skip child
##                if newNode.key in openMap:
##                    if openMap[newNode.key].g < newNode.g:
##                        continue
##                #newNode.state.printP()
##                newH = newNode.h
##                newG = newNode.g
##                newF = newG + newH
##                openList.put( (newF,\
##                               (newNode.key, newNode)) )
##                openMap[newNode.key] = newNode
##        return None
##    
##    #Function to check for solvable state
##    def checkSolvable(self, puzzle):
##        inversions = 0
##        lineList = []
##        (y, x) = (0, 0)
##        for i in range(0, len(puzzle)):
##            for j in range(0, len(puzzle)):
##                lineList.append(puzzle[i][j])
##                if puzzle[i][j] == 0:
##                    (y, x) = (i, j)
##                    print 'Y', 'X', i, j
##
##        for i in range(0, len(lineList)-1):
##            for j in range(i+1, len(lineList)):
##                if lineList[j] and lineList[i] and lineList[i] > lineList[j]:
##                    inversions += 1
##
##        del lineList
##        #print("INV:", inversions)
##        print 'INV:', inversions
##        if len(puzzle) % 2 == 1:
##            #ODD, must have even inversions
##            if (inversions % 2) == 0:
##                print 'ODD length Solvable'
##                return True
##            else:
##                print 'ODD length Unsolvable'
##                return False
##        else:
##            #EVEN, must have:
##            #1) blank on EVEN row & ODD inversions
##            #2) blank on ODD row & EVEN inversions
##            if (y % 2 == 0 and inversions % 2 == 1) or \
##               (y % 2 == 1 and inversions % 2 == 0):
##                print 'EVEN length Solvable'
##                return True
##            else:
##                print 'EVEN length Unsolvable'
##                return False
##                    
### Convenient function to retrace path
def reconstruct(currentNode):
    path = []
    current = currentNode    
    while current is not None:
        if current.moves is None:
            break
        path.append(moveList[current.moves])
        current = current.parent
    return path[::-1]

if __name__ == "__main__":
##    data = {}
##    data[112122313242] = 1
##    data[112122313241] = 0
##    field = {}
##    try:
##        #check if pdb exist
##        f = open('pdbTest.json', 'r')
##        #read from json file into dict
##        field = json.load(f)
##    except IOError:
##        #print("No File detected")
##        #print("Writing new data")
##        #populate json file with dict
##        with open('pdbTest.json', 'w') as f:
##            json.dump(data, f)
##    finally:
##        f.close()
    n = 4
    max_num = n ** 2 - 1
    goal_state = [[0 for i in range(n)] for j in range(n)]

    #Set goal state
    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0
    #Global reference to goal state
    finalGoal = goal_state
    puzzle = Puzzle(goal_state)
    #Prints initial state
    puzzle.printP()
    #Solve the puzzle
    search = Search(puzzle)
    result = search.generate4x4()
    if result is None:
        print 'END OF Q'
    elif result == FINISHED:
        print 'DONE GENERATING PDB'
        
    
    
    
    
##    # do NOT modify below
##
##    # argv[0] represents the name of the file that is being executed
##    # argv[1] represents name of input file
##    # argv[2] represents name of destination output file
##
##    #PROPER USE[1]
##    if len(sys.argv) != 3:
##        raise ValueError("Wrong number of arguments!")
##    
##    try:
##        #f = open("n_equals_3/input_2.txt", 'r')
##        #PROPER USE[2]
##        f = open(sys.argv[1], 'r')
##    except IOError:
##        raise IOError("Input file not found!")
##
##    lines = f.readlines()
##    
##    # n = num rows in input file
##    n = len(lines)
##    # max_num = n to the power of 2 - 1
##    max_num = n ** 2 - 1
##    
##    # Instantiate a 2D list of size n x n
##    init_state = [[0 for i in range(n)] for j in range(n)]
##    goal_state = [[0 for i in range(n)] for j in range(n)]
##    
##    #Parse file into 2d list
##    i,j = 0, 0
##    for line in lines:
##        lll = line.split()
##        ll = [int(x) for x in lll]
##        for number in ll:
##            if 0 <= number <= max_num:
##                init_state[i][j] = int(number)
##                j += 1
##                if j == n:
##                    i += 1
##                    j = 0
##    #Set goal state
##    for i in range(1, max_num + 1):
##        goal_state[(i-1)//n][(i-1)%n] = i
##    goal_state[n - 1][n - 1] = 0
##    #Global reference to goal state
##    finalGoal = goal_state
##    puzzle = Puzzle(init_state)
##    #Prints initial state
##    puzzle.printP()
##    #Solve the puzzle
##    search = Search(puzzle)
##    result = search.aStarOne()
##
##    #PROPER USE[3]
##    with open(sys.argv[2], 'w') as out:
##        if result is None:
##            #print("UNSOLVABLE")
##            print "UNSOLVABLE"
##            out.write('UNSOLVABLE')
##        else:
##            path = reconstruct(result)
##            output = ''
##            for action in path:
##                #print(action)
##                output = output + str(action) + '\n'
##            print output
##            out.write(output)
##            #print("TOTAL:", len(path))
##            print "TOTAL", len(path)
    






