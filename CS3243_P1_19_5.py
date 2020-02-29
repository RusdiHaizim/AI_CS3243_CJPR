import os
import sys
import CS3243_P1_19_1 as algoU
import CS3243_P1_19_2 as algoI1
import CS3243_P1_19_3 as algoI2
import CS3243_P1_19_4 as algoI3

#Debugging print 2d array
def printP(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            print puzzle[i][j],
        print ""

#Scanning input from lines into init and goal
def scanInput(init, goal, lines, n):
    max_num = n ** 2 - 1
    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0
    for i in range(1, max_num + 1):
        goal[(i-1)//n][(i-1)%n] = i
    goal[n - 1][n - 1] = 0

def printParams(puzzle):
    print 'Time taken: ' + str(puzzle.timeTaken)
    print 'Total nodes popped: ' + str(puzzle.nodesPopped)
    print 'Size of frontier: ' + str(puzzle.nodesInside)
    print 'Total moves: ' + str(puzzle.finalMoves)    

#Run 3x3 test cases
def run_n_equals_3():
    fileList = []
    path = "public_tests_p1/n_equals_3"
    for file in sorted(os.listdir(path)):
        if file.endswith(".txt"):
            fileList.append(os.path.join(path, file))
    for x in range(len(fileList)):
        try:
            f = open(fileList[x], 'r')
        except:
            raise IOError("Input file not found!")
        
        # Instantiate a 2D list of size n x n
        lines = f.readlines()
        n = len(lines)
        init = [[0 for i in range(n)] for j in range(n)]
        goal = [[0 for i in range(n)] for j in range(n)]
        scanInput(init, goal, lines, n)

        print '>'*20 + ' Starting input ' + str(x+1) + ' ' + '>'*20
        printP(init)

        print '-'*30 + '\n' + 'Uninformed Search (BFS):'
        puzzle = algoU.Puzzle(init, goal); ans = puzzle.solve(); printParams(puzzle)
        print '-'*30 + '\n' + 'Informed Search (A-STAR with Euclidean Distance):'
        puzzle = algoI1.Puzzle(init, goal); ans = puzzle.solve(); printParams(puzzle)
        print '-'*30 + '\n' + 'Informed Search (A-STAR with Manhattan Distance):'
        puzzle = algoI2.Puzzle(init, goal); ans = puzzle.solve(); printParams(puzzle)
        print '-'*30 + '\n' + 'Informed Search (A-STAR with Manhattan Distance PLUS Linear Conflicts):'
        puzzle = algoI3.Puzzle(init, goal); ans = puzzle.solve(); printParams(puzzle)
        
        print '<'*28 + ' END ' + '<'*28

#Run 4x4 test cases
def run_n_equals_4():
    fileList = []
    path = "public_tests_p1/n_equals_4"
    for file in sorted(os.listdir(path)):
        if file.endswith(".txt"):
            fileList.append(os.path.join(path, file))
    for x in range(len(fileList)):
##        if x == 1: #takes too long for euclidean to test on local pc
##            continue
        
        try:
            f = open(fileList[x], 'r')
        except:
            raise IOError("Input file not found!")
        
        # Instantiate a 2D list of size n x n
        lines = f.readlines()
        n = len(lines)
        init = [[0 for i in range(n)] for j in range(n)]
        goal = [[0 for i in range(n)] for j in range(n)]
        scanInput(init, goal, lines, n)

        print '>'*20 + ' Starting input ' + str(x+1) + ' ' + '>'*20
        printP(init)

##        print '-'*30 + '\n' + 'Uninformed Search (BFS):' #BFS TOO LONG...
##        puzzle = algoU.Puzzle(init, goal); ans = puzzle.solve(); printParams(puzzle)
        print '-'*30 + '\n' + 'Informed Search (A-STAR with Euclidean Distance):'
        puzzle = algoI1.Puzzle(init, goal); ans = puzzle.solve(); printParams(puzzle)
        print '-'*30 + '\n' + 'Informed Search (A-STAR with Manhattan Distance):'
        puzzle = algoI2.Puzzle(init, goal); ans = puzzle.solve(); printParams(puzzle)
        print '-'*30 + '\n' + 'Informed Search (A-STAR with Manhattan Distance PLUS Linear Conflicts):'
        puzzle = algoI3.Puzzle(init, goal); ans = puzzle.solve(); printParams(puzzle)
        
        print '<'*28 + ' END ' + '<'*28

#Run 5x5 test cases
def run_n_equals_5():
    fileList = []
    path = "public_tests_p1/n_equals_5"
    for file in sorted(os.listdir(path)):
        if file.endswith(".txt"):
            fileList.append(os.path.join(path, file))
    for x in range(len(fileList)):
        try:
            f = open(fileList[x], 'r')
        except:
            raise IOError("Input file not found!")
        
        # Instantiate a 2D list of size n x n
        lines = f.readlines()
        n = len(lines)
        init = [[0 for i in range(n)] for j in range(n)]
        goal = [[0 for i in range(n)] for j in range(n)]
        scanInput(init, goal, lines, n)

        print '>'*20 + ' Starting input ' + str(x+1) + ' ' + '>'*20
        printP(init)

##        print '-'*30 + '\n' + 'Uninformed Search (BFS):' #BFS TOO LONG...
##        puzzle = algoU.Puzzle(init, goal); ans = puzzle.solve(); printParams(puzzle)
        print '-'*30 + '\n' + 'Informed Search (A-STAR with Euclidean Distance):'
        puzzle = algoI1.Puzzle(init, goal); ans = puzzle.solve(); printParams(puzzle)
        print '-'*30 + '\n' + 'Informed Search (A-STAR with Manhattan Distance):'
        puzzle = algoI2.Puzzle(init, goal); ans = puzzle.solve(); printParams(puzzle)
        print '-'*30 + '\n' + 'Informed Search (A-STAR with Manhattan Distance PLUS Linear Conflicts):'
        puzzle = algoI3.Puzzle(init, goal); ans = puzzle.solve(); printParams(puzzle)
        
        print '<'*28 + ' END ' + '<'*28


if __name__ == "__main__":
    # do NOT modify below
    run_n_equals_3()
    run_n_equals_4()
    run_n_equals_5()
    
    
