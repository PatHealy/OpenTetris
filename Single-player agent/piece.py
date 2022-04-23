
from typing import List
# from global_variables import *
# from shapes import *
# import global variable for the game scope
from global_variables import *
# # import the list of Shapes and their respective colors
from shapes import *


# template class for the current piece and next piece in the game
class Piece:
    # default initialization
    def __init__(self, column: int, row: int, shape: List[List]):
        # initial x coordinate
        self.x = column
        # initial y coordinate
        self.y = row
        # shape of piece
        self.shape = shape
        # color of shape
        self.color = SHAPE_COLORS[SHAPES_LIST.index(shape)]
        # initial rotational orientation index
        self.rotation = 0

    # format the list of lists as (x,y) readable coordinates
    def get_formatted_shape(self):
        # empty list
        positions = list()
        # get the list of coordinates based on the orientation
        formatted_shape = self.shape[self.rotation % len(self.shape)]

        # iterate through rows of the list
        for i, line in enumerate(formatted_shape):
            row = list(line)
            # iterate through columns
            for j, column in enumerate(row):
                # if coordinate marked by '*' then record this position
                if column == '*':
                    # append position
                    positions.append((self.x + j, self.y + i))

        # To fix shape structure notation from shapes.py
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)

        # return list of tuples as [(x1,y1), ...... ,(xn,yn)]
        return positions

    # check if the current piece is in visible grid space
    def in_valid_space(self, grid):
        # create an empty grid
        accepted_pos = [[(j, i) for j in range(NUM_COLUMNS) if grid[i][j] == (0, 0, 0)] for i in range(NUM_ROWS)]
        # flatten the list of lists as a single list of coordinates
        accepted_pos = [pos for sub in accepted_pos for pos in sub]
        # get the formatted_shape
        formatted_shape = self.get_formatted_shape()

        # iterate through coordinates from formatted_shape
        for pos in formatted_shape:
            # if a part of the block piece is out of visible region
            if pos not in accepted_pos:
                if pos[1] > -1:
                    # then return false
                    return False
        # else return true
        return True

    # this method is used to override the default implementation of copy.copy() method
    def __copy__(self):
        # it returns another object of the same class with identical parameters
        return Piece(self.x, self.y, self.shape)
