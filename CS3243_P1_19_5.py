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

#Run 3x3 test cases
def run_n_equals_3():
    start = 'new_test_cases/n_equals_3/input_'
    inputNum = ['1', '2', '3']
    for x in range(len(inputNum)):
        try:
            f = open(start + inputNum[x] + '.txt', 'r')
        except:
            raise IOError("Input file not found!")
        
        # Instantiate a 2D list of size n x n
        lines = f.readlines()
        n = len(lines)
        init = [[0 for i in range(n)] for j in range(n)]
        goal = [[0 for i in range(n)] for j in range(n)]
        scanInput(init, goal, lines, n)

        print '*'*20 + ' Starting input ' + inputNum[x] + ' ' + '*'*20
        printP(init)

        print '-'*30 + '\n' + 'Uninformed Search (BFS):'
        puzzle = algoU.Puzzle(init, goal); ans = puzzle.solve()
        print '-'*30 + '\n' + 'Informed Search (A-STAR with Euclidean Distance):'
        puzzle = algoI1.Puzzle(init, goal); ans = puzzle.solve()
        print '-'*30 + '\n' + 'Informed Search (A-STAR with Manhattan Distance):'
        puzzle = algoI2.Puzzle(init, goal); ans = puzzle.solve()
        print '-'*30 + '\n' + 'Informed Search (A-STAR with Manhattan Distance PLUS Linear Conflicts):'
        puzzle = algoI3.Puzzle(init, goal); ans = puzzle.solve()
        
        print '*'*28 + ' END ' + '*'*28

#Run 4x4 test cases
def run_n_equals_4():
    start = 'new_test_cases/n_equals_4/input_'
    inputNum = ['1', '2', '3', '4']
    for x in range(len(inputNum)):
        if x == 1: #takes too long for euclidean to test on local pc
            continue
        
        try:
            f = open(start + inputNum[x] + '.txt', 'r')
        except:
            raise IOError("Input file not found!")
        
        # Instantiate a 2D list of size n x n
        lines = f.readlines()
        n = len(lines)
        init = [[0 for i in range(n)] for j in range(n)]
        goal = [[0 for i in range(n)] for j in range(n)]
        scanInput(init, goal, lines, n)

        print '*'*20 + ' Starting input ' + inputNum[x] + ' ' + '*'*20
        printP(init)

        #print '-'*30 + '\n' + 'Uninformed Search (BFS):' #BFS TOO LONG...
        #puzzle = algoU.Puzzle(init, goal); ans = puzzle.solve()
        print '-'*30 + '\n' + 'Informed Search (A-STAR with Euclidean Distance):'
        puzzle = algoI1.Puzzle(init, goal); ans = puzzle.solve()
        print '-'*30 + '\n' + 'Informed Search (A-STAR with Manhattan Distance):'
        puzzle = algoI2.Puzzle(init, goal); ans = puzzle.solve()
        print '-'*30 + '\n' + 'Informed Search (A-STAR with Manhattan Distance PLUS Linear Conflicts):'
        puzzle = algoI3.Puzzle(init, goal); ans = puzzle.solve()
        
        print '*'*28 + ' END ' + '*'*28

#Run 5x5 test cases
def run_n_equals_5():
    start = 'new_test_cases/n_equals_5/input_'
    inputNum = ['1', '2', '3', '4', '5']
    for x in range(len(inputNum)):
        try:
            f = open(start + inputNum[x] + '.txt', 'r')
        except:
            raise IOError("Input file not found!")
        
        # Instantiate a 2D list of size n x n
        lines = f.readlines()
        n = len(lines)
        init = [[0 for i in range(n)] for j in range(n)]
        goal = [[0 for i in range(n)] for j in range(n)]
        scanInput(init, goal, lines, n)

        print '*'*20 + ' Starting input ' + inputNum[x] + ' ' + '*'*20
        printP(init)

        #print '-'*30 + '\n' + 'Uninformed Search (BFS):' #BFS TOO LONG...
        #puzzle = algoU.Puzzle(init, goal); ans = puzzle.solve()
        print '-'*30 + '\n' + 'Informed Search (A-STAR with Euclidean Distance):'
        puzzle = algoI1.Puzzle(init, goal); ans = puzzle.solve()
        print '-'*30 + '\n' + 'Informed Search (A-STAR with Manhattan Distance):'
        puzzle = algoI2.Puzzle(init, goal); ans = puzzle.solve()
        print '-'*30 + '\n' + 'Informed Search (A-STAR with Manhattan Distance PLUS Linear Conflicts):'
        puzzle = algoI3.Puzzle(init, goal); ans = puzzle.solve()
        
        print '*'*28 + ' END ' + '*'*28


if __name__ == "__main__":
    # do NOT modify below
    run_n_equals_3()
    run_n_equals_4()
    run_n_equals_5()
    
    
