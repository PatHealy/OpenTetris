import random
import sys
sys.path.insert(0, './core')
from entities import *

board = None

def aggregate_height(board):

    # get column heights
    # average height
    pass

def column_height(board):

    # for column in columns
    # "highest" square
    pass

def hole_count(board):

    # for squares in columns
    # empty square with filled square on top
    pass

def bumpiness(board):

    # get column heights []
    # for column in columns
    # bumpiness += abs(height - the next height)
    pass

def lines_cleared(board):
    
    count = 0
    # for row in board
    # if row is "filled" >= len(board)
    # count += 1
    return count

def get_score():

    score = 0
    count = lines_cleared(board)
    #modify, multiplier, etc
    score = count

    return score

def random_weight():

    # return random
    pass
