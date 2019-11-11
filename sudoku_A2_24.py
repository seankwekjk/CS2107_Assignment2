"""
CS3243 Assignment 2 (Sudoku)
Members:
    Benn Tay Guobin | A0167647N
    Kwek Jun Kai Sean | A0155565X
"""

import sys
import copy
import random
import heapq as pq

PRINT = False

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists
        self.domains = {}
        self.given_vals = set()
        self.target_vals = []
        
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] != 0:
                    self.given_vals.add((i, j))
                else:
                    self.target_vals.append((i, j))
        for target in self.target_vals:
            newSet = set()
            for i in range(1, 10):
                newSet.add(i)
            self.domains[target] = newSet

    # For trying out a value and checking the num
    # of conflicts without it being assigned to the
    # puzzle yet
    def num_conflicts_for_val(self, y, x, val):
        sum = 0
        # check horizontal case
        for j in range(9):
            if j == x:
                continue
            if self.ans[y][j] == val:
                sum += 1
        # check vertical case
        for i in range(9):
            if i == y:
                continue
            if self.ans[i][x] == val:
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
                if self.ans[i][j] == val:
                    sum += 1
        return sum

    def num_conflicts(self, y, x):
        sum = 0
        # check horizontal case
        for j in range(9):
            if j == x:
                continue
            if self.ans[y][j] == self.ans[y][x]:
                sum += 1
        # check vertical case
        for i in range(9):
            if i == y:
                continue
            if self.ans[i][x] == self.ans[y][x]:
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
                if self.ans[i][j] == self.ans[y][x]:
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
    # are reduced. Prunes the search tree.
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
                self.ans[row][col] = final_val
                toTransfer.add(target_grid)
        for fixed_grid in toTransfer:
            self.domains.pop(fixed_grid)
            self.target_vals.remove(fixed_grid)
            self.given_vals.add(fixed_grid)
        return changed

    def is_complete(self):
        for i in range(9):
            for j in range(9):
                if self.ans[i][j] == 0:
                    return False
        return True

    def get_next_zero_var(self):
        for var in self.target_vals:
            if self.ans[var[0]][var[1]] == 0:
                return var

    def backtrack_search(self):
        if self.is_complete():
            return True

        currVar = self.get_next_zero_var()
        currDom = self.domains[currVar]
        row = currVar[0]
        col = currVar[1]

        for val in currDom:
            if self.num_conflicts_for_val(row, col, val) == 0:
                self.ans[row][col] = val
                result = self.backtrack_search()
                if result:
                    return result
                self.ans[row][col] = 0

    def solve(self):
        #TODO: Your code here
        if PRINT:
            print "STARTING NUM CONFLICTS: ", self.total_conflicts()

        cont = True
        while cont:
            self.reduce_domains()
            cont = self.set_singles()

        self.backtrack_search()

        # don't print anything here. just resturn the answer
        # self.ans is a list of lists
        return self.ans

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY

# Auxiliary print  method
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

    if PRINT:
        printPuzzle(puzzle)
        print

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    if PRINT:
        printPuzzle(ans)
        print "total num of conflicts remaining", sudoku.total_conflicts()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
