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

def linear_conflicts(puzzle):
    size = len(puzzle)
    candidate = []
    solved = []
    for i in range(size):
        for j in range(size):
            candidate.append(puzzle[i][j])
            solved.append( (i*size) + j + 1)
    solved[size**2 - 1] = 0

    def count_conflicts(candidate_row, solved_row, size, ans=0):
        counts = [0 for x in range(size)]
        for i, tile_1 in enumerate(candidate_row):
            if tile_1 in solved_row and tile_1 != 0:
                for j, tile_2 in enumerate(candidate_row):
                    if tile_2 in solved_row and tile_2 != 0:
                        if tile_1 != tile_2:
                            if (solved_row.index(tile_1) > solved_row.index(tile_2)) and i < j:
                                counts[i] += 1
                            if (solved_row.index(tile_1) < solved_row.index(tile_2)) and i > j:
                                counts[i] += 1
        if max(counts) == 0:
            return ans * 2
        else:
            i = counts.index(max(counts))
            candidate_row[i] = -1
            ans += 1
            return count_conflicts(candidate_row, solved_row, size, ans)

    dist = 0
    for i in range(size):
        for j in range(size):
            num = puzzle[i][j]
            if num != 0:
                rowGoal = (num - 1) // size
                colGoal = (num - 1) % size
                diffRow = abs(rowGoal - i)
                diffCol = abs(colGoal - j)
                h = diffRow + diffCol
                dist += h
                
    res = dist
    
    candidate_rows = [[] for y in range(size)] 
    candidate_columns = [[] for x in range(size)] 
    solved_rows = [[] for y in range(size)] 
    solved_columns = [[] for x in range(size)] 
    for y in range(size):
        for x in range(size):
            idx = (y * size) + x
            candidate_rows[y].append(candidate[idx])
            candidate_columns[x].append(candidate[idx])
            solved_rows[y].append(solved[idx])
            solved_columns[x].append(solved[idx])
    for i in range(size):
            res += count_conflicts(candidate_rows[i], solved_rows[i], size)
    for i in range(size):
            res += count_conflicts(candidate_columns[i], solved_columns[i], size)
    #print 'h, d', res, dist
    return res


### Node Class
# Inputs: puzzle(2d array), parent node(if any), <int>move(if any)
class Node(object):
    def __init__(self, puzzle, parent=None, move=None):
        self.puzzle = puzzle
        self.move = move
        self.h = 0
        self.g = 0
        self.tick = 0
        self.key = self.tupify()
        self.parent = parent

    def tupify(self):
        outer = []
        for i in self.puzzle:
            outer.append(tuple(i))
        return tuple(outer)
 
    def __hash__(self):
        return hash(self.key)

    def __ne__(self, other):
        return self.key != other.key

    def __eq__(self, other):
        return self.key == other.key
        #return (self.key, self.g) == (other.key, other.g)

    def __lt__(self, other):
        if self.g != other.g:
            return self.g > other.g
        return self.tick > other.tick
    
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
    
    #Gets the heuristic value of state
    def getH(self):
        #BIGGEST BOSS (H3)
        return linear_conflicts(self.puzzle)

    #Gets the manhattan distance (H2)
    def getManhattanDistance(self):
        h = 0; size = len(self.puzzle)
        for i in range(0, size):
            for j in range(0, size):
                num = self.puzzle[i][j]
                if num != 0:
                    rowGoal = (num - 1) // size
                    colGoal = (num - 1) % size
                    diffRow = abs(rowGoal - i)
                    diffCol = abs(colGoal - j)
                    dist = diffRow + diffCol
                    h += dist
        return h
    
    #Gets the number of Linear Conflicts (H3) #DEPRECATED
    def getLinearConflict(self):
        size = len(self.puzzle)
        inCol = [0] * (size**2)
        inRow = [0] * (size**2)
        conflicts = 0
        manD = 0
        #Precompute bools for numbers in right row and col
        for y in range(size):
            for x in range(size):
                num = self.puzzle[y][x]
                if num != 0:
                    rowGoal = (num - 1) // size
                    colGoal = (num - 1) % size
                    inRow[num] = rowGoal
                    inCol[num] = colGoal
                    #calculate manD
                    manD += abs(rowGoal - y) + abs(colGoal - x)
        #Check row conflicts
        for r in range(size):
            for cI in range(size):
                for cN in range(cI+1, size):
                    if self.puzzle[r][cI] and self.puzzle[r][cN] and\
                       r == inRow[self.puzzle[r][cI]] and\
                       inRow[self.puzzle[r][cI]] == inRow[self.puzzle[r][cN]] and\
                       inCol[self.puzzle[r][cI]] > inCol[self.puzzle[r][cN]]:
                        #Conflict exists!
                        conflicts += 1
                        #print 'left, right', self.puzzle[r][cI], self.puzzle[r][cN]
        #Check col conflicts
        for c in range(size):
            for rI in range(size):
                for rN in range(rI+1, size):
                    if self.puzzle[rI][c] and self.puzzle[rN][c] and\
                       c == inCol[self.puzzle[rI][c]] and\
                       inCol[self.puzzle[rI][c]] == inCol[self.puzzle[rN][c]] and\
                       inRow[self.puzzle[rI][c]] > inRow[self.puzzle[rN][c]]:
                        #Conflict exists!
                        conflicts += 1
        #print 'h:', conflicts*2 + manD, 'manD', manD, "conflicts:", conflicts
        #pp(self.puzzle)
        return conflicts*2 + manD
    
    #Gets the number of tiles that are out of Row and out of Col (H1a)
    def getOutOfLine(self):
        size = len(self.puzzle)
        out = 0
        for i in range(size):
            for j in range(size):
                num = self.puzzle[i][j]
                if num == 0:
                    continue
                rowGoal = (num - 1) // size
                colGoal = (num - 1) % size
                out += (rowGoal != i)
                out += (colGoal != j)
        return out

    #Gets the euclidean distance (H1b)
    def getEuclideanValue(self):
        h = 0
        size = len(self.puzzle)
        for i in range(size):
            for j in range(size):
                num = self.puzzle[i][j]
                if num != 0:
                    rowGoal = (num - 1) // size
                    colGoal = (num - 1) % size
                    dist = sqrt( (rowGoal - i)**2 + (colGoal - j)**2 )
                    h += dist
        return h

    #Returns list of potential children<list<tuple>>
    def getChildren(self, currNode):
        children = []
        (y, x) = self.findZero(self.puzzle)
        direction = [(y-1, x), (y+1, x), (y, x-1), (y, x+1)] #UP, DOWN, LEFT, RIGHT
        for move in range(len(direction)):
            (y1, x1) = direction[move]
            if currNode.move is not None and move == mMap[currNode.move]:
                continue
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
            path.append(moveList[mMap[current.move]])
            current = current.parent
        return path[::-1]

    #Returns child PID
    def getMoves(self, cameFrom, currentNode):
        path = []
        current = currentNode
        while current is not None:
            if cameFrom[current] is None:
                break
            path.append(moveList[mMap[current.move]])
            current = cameFrom[current]
        return path[::-1]
    
    #Solves the puzzle using A-STAR
    def solve(self):
        ID = 0
        startTime = time()
        currNode = Node(self.init_state)
        #self.printP()
        if self.checkSolvable(currNode.puzzle) == False:
            return ["UNSOLVABLE"]
        # 2 Data Structures to keep track of...
        openList = PriorityQueue()
        openList.put((currNode.getH(), currNode)) # STABLEST
        costMap = {currNode.key:0}
        steps = 0 #Nodes popped off frontier
        while True:
            steps += 1
##            if steps % 100000 == 0:
##                print 'step:', steps, 'size', openList.qsize()
##                sys.stdout.flush()
            if openList.empty(): #Empty frontier
                print 'Empty Queue!'
                break
            currNode = openList.get()[1] # STABLEST
            if self.isGoalState(currNode.puzzle):
                ans = self.reconstruct(currNode)
                self.timeTaken = time() - startTime
                self.nodesPopped = steps
                self.nodesInside = openList.qsize()
                self.finalMoves = len(ans)
##                print 'TIME:', self.timeTaken
##                print 'nodesPopped', self.nodesPopped
                return ans
            for child in currNode.getChildren(currNode):
                ID += 1
                child.g = currNode.g + 1
                #Child is now a Node          
                if child.key not in costMap or child.g < costMap[child.key]:
                    costMap[child.key] = child.g
                    child.h = child.getH() #ONLINE
                    child.tick = ID
                    openList.put((child.g + child.h, child)) # STABLEST
        timeTaken = time() - startTime
        print 'Time taken:', str(timeTaken)
        return ["UNSOLVABLE"]

    #Debugging print 2d array
    def printP(self):
        for i in range(len(self.init_state)):
            for j in range(len(self.init_state)):
                print self.init_state[i][j],
            print ""

def pp(data):
    for i in range(len(data)):
        for j in range(len(data)):
            print data[i][j],
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
            #print answer
            sys.stdout.flush()
        print "TOTAL", len(ans)
