import sys
import copy
from random import randint
import heapq
"""
variables = {(i, j):domain[(i, j)]}
domains = {(i, j):[0:9]}
minConflictVars = heapq([((i, j), numConflicts)])
"""

DEBUG = False
MAX_ITER = 1000

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists
        self.domains = {}
        self.given_vals = set()
        self.target_vals = set()
        
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] != 0:
                    self.given_vals.add((i, j))
                else:
                    self.puzzle[i][j] = randint(1, 9)
                    self.target_vals.add((i, j))
        for target in self.target_vals:
            newSet = set()
            for i in range(1, 10):
                newSet.add(i)
            self.domains[target] = newSet

    # For trying out a value and checking the num
    # of conflicts without it being assigned to the
    # puzzle yet
    """
    def num_conflicts_for_val(self, y, x, val):
        sum = 0
        # check horizontal case
        for j in range(9):
            if j == x:
                continue
            if self.puzzle[y][j] == val:
                sum += 1
        # check vertical case
        for i in range(9):
            if i == y:
                continue
            if self.puzzle[i][x] == val:
                sum += 1
        # check 3x3 case
        y_boxnum = y//3
        x_boxnum = x//3
        y_start = y_boxnum * 3
        x_start = x_boxnum * 3
        for i in range(y_start, y_start+3):
            for j in range(x_start, x_start+3):
                if i == y and j == x:
                    continue
                if self.puzzle[i][j] == val:
                    sum += 1
        return sum
    """
    def num_conflicts(self, y, x):
        sum = 0
        # check horizontal case
        for j in range(9):
            if j == x:
                continue
            if self.puzzle[y][j] == self.puzzle[y][x]:
                sum += 1
        # check vertical case
        for i in range(9):
            if i == y:
                continue
            if self.puzzle[i][x] == self.puzzle[y][x]:
                sum += 1
        # check 3x3 case
        y_boxnum = y//3
        x_boxnum = x//3
        y_start = y_boxnum * 3
        x_start = x_boxnum * 3
        for i in range(y_start, y_start+3):
            for j in range(x_start, x_start+3):
                if i == y and j == x:
                    continue
                if self.puzzle[i][j] == self.puzzle[y][x]:
                    sum += 1
        return sum

    def total_conflicts(self):
        sum = 0
        for i in range(9):
            for j in range(9):
                sum += self.num_conflicts(i, j)
        return sum

    # Based on the current fixed values in the puzzle,
    # domains of affected cells in the same row/column/subgrid
    # are reduced.
    def reduce_domains(self,):
        for givenGrid in self.given_vals:
            row = givenGrid[0]
            col = givenGrid[1]
            conflict_val = self.puzzle[row][col]

            # Reduce row
            for j in range(9):
                grid = (row, j)
                if (grid == givenGrid) or (grid in self.given_vals):
                    continue
                else:
                    if conflict_val in self.domains[grid]:
                        self.domains[grid].remove(conflict_val)
                print

            # Reduce column
            for i in range(9):
                grid = (i, col)
                if (grid == givenGrid) or (grid in self.given_vals):
                    continue
                else:
                    if conflict_val in self.domains[grid]:
                        self.domains[grid].remove(conflict_val)

            # Reduce subgrid
            boxStartRow = (row//3) * 3
            boxEndRow = boxStartRow + 3
            boxStartCol = (col//3) * 3
            boxEndCol = boxStartCol + 3
            for i in range(boxStartRow, boxEndRow):
                for j in range(boxStartCol, boxEndCol):
                    grid = (i, j)
                    if (grid == givenGrid) or (grid in self.given_vals):
                        continue
                    else:
                        if conflict_val in self.domains[grid]:
                            self.domains[grid].remove(conflict_val)

    # For domains with only one value left, the variable is set to
    # the value and fixed for the rest of the search. This variable is
    # considered solved and transferred to the given_values set.
    def set_singles(self):
        changed = False
        toTransfer = set()
        for target_grid in self.domains:
            if len(self.domains[target_grid]) == 1:
                changed = True
                row = target_grid[0]
                col = target_grid[1]
                final_val = self.domains[target_grid].pop()
                self.puzzle[row][col] = final_val
                toTransfer.add(target_grid)
        for fixed_grid in toTransfer:
            self.domains.pop(fixed_grid)
            self.target_vals.remove(fixed_grid)
            self.given_vals.add(fixed_grid)
        return changed

    def isSolution(self):
        return self.total_conflicts == 0

    def getRandomVar(self):
        pass

    def solve(self):
        #TODO: Your code here
        cont = True
        while cont:
            if DEBUG:
                print"==================================="
                print len(self.given_vals), len(self.target_vals)
                for var in sudoku.target_vals:
                    print var, sudoku.domains[var]
                print"==================================="

            self.reduce_domains()
            cont = self.set_singles()
        
        if DEBUG:
            print len(self.given_vals), len(self.target_vals)
            for var in sudoku.target_vals:
                print var, sudoku.domains[var]

        # Main min-conflicts algorithm
        for iter in range(MAX_ITER):
            if self.isSolution():
                break

            currVar = self.getRandomVar();

            # set value ← the value v for var that minimizes CONFLICTS(var,v,current_state,csp)
            # set var ← value in current_state

        # don't print anything here. just resturn the answer
        # self.ans is a list of lists
        #return self.ans
        return self.puzzle

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY

def printPuzzle(puzzle):
    # print ans in console
    for i in range(9):
        for j in range(9):
            s = str(puzzle[i][j]) + " "
            print s,
        print

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python sudoku_A2_xx.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python sudoku_A2_xx.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    printPuzzle(puzzle)

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    printPuzzle(sudoku.puzzle)

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
