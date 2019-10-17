import sys
import copy
from random import randint

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

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

    def solve(self):
        #TODO: Your code here

        given_vals = set()
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] != 0:
                    given_vals.add((i, j))
                else:
                    self.puzzle[i][j] = randint(1, 9)


        # don't print anything here. just resturn the answer
        # self.ans is a list of lists
        return self.ans

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY

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

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
