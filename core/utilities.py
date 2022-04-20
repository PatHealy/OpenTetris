import random
import sys
sys.path.insert(0, './core')

board = None

def aggregate_height(board):
    #board is a Board object (see the class definition in core/entities.py
    # get column heights
    # average height
    heights = column_height(board)
    return sum(heights)/float(board.width)

def column_height(board):
    # "highest" square in each column
    heights = [0] * board.width
    data = board.get_data()
    for i in range(board.height):
        for j in range(board.width):
            if not data[i][j] == (0,0,0):
                heights[j] = i + 1
    return heights

def hole_count(board):
    # for squares in columns
    # empty square with filled square on top
    heights = column_height(board)
    data = board.get_data()

    holes = 0
    for i in range(board.height):
        for j in range(board.width):
            if i < heights[j] - 1:
                if data[i][j] == (0,0,0):
                    holes = holes + 1
    return holes

def bumpiness(board):
    # get column heights []
    heights = column_height(board)
    # for column in columns
    # bumpiness += abs(height - the next height)
    bumpiness = 0
    for i in range(board.width-1):
        bumpiness = bumpiness + abs(heights[i] - heights[i + 1])
    return bumpiness

def lines_cleared(board):
    count = board.get_lines_cleared()
    return count

def get_score(board):
    score = board.get_score()
    return score

def random_weight():
    # return random
    return random.random()
