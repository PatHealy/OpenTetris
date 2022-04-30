import random
import sys
sys.path.insert(0, './core')
from entities import *
import numpy as np

class ModelParams:
    def __init__(self, generate=False, board=None):
        if generate:
            self.get_aggregate_height(board)
            self.get_hole_count(board)
            self.get_bumpiness(board)
            self.get_lines_cleared(board)
            self.get_score(board)
            self.get_random_weight()
            self.get_num_pits(board)
            self.get_num_col_with_holes(board)
            self.get_row_transitions(board)
            self.get_col_transitions(board)
            self.get_max_well(board)

    def get_aggregate_height(self, board):
        #board is a Board object (see the class definition in core/entities.py
        # get column heights
        # average height
        heights = self.get_column_height(board)
        self.aggregate_height = sum(heights)/float(board.width)
        return self.aggregate_height

    def get_column_height(self, board):
        # "highest" square in each column
        heights = [0] * board.width
        data = board.get_data()
        for i in range(board.height):
            for j in range(board.width):
                if not data[i][j] == (0,0,0):
                    heights[j] = i + 1
        self.column_height = heights
        return self.column_height

    def get_hole_count(self, board):
        # for squares in columns
        # empty square with filled square on top
        heights = self.get_column_height(board)
        data = board.get_data()

        holes = 0
        for i in range(board.height):
            for j in range(board.width):
                if i < heights[j] - 1:
                    if data[i][j] == (0,0,0):
                        holes = holes + 1
        self.hole_count = holes
        return self.hole_count

    def get_bumpiness(self, board):
        # get column heights []
        heights = self.get_column_height(board)
        # for column in columns
        # bumpiness += abs(height - the next height)
        bumpiness = 0
        for i in range(board.width-1):
            bumpiness = bumpiness + abs(heights[i] - heights[i + 1])
        self.bumpiness = bumpiness
        return bumpiness

    def get_lines_cleared(self, board):
        self.lines_cleared = board.get_lines_cleared()
        return self.lines_cleared

    def get_score(self,board):
        score = board.get_score()
        self.score = score
        return self.score

    def get_random_weight(self):
        # return random
        self.random_weight = random.random()
        return self.random_weight

    def get_num_pits(self, board):
        heights = self.get_column_height(board)
        self.num_pits = 0
        for c in heights:
            if c == 0:
                self.num_pits += 1
        return self.num_pits

    def get_num_col_with_holes(self, board):
        heights = self.get_column_height(board)
        data = board.get_data()

        has_holes = [0] * board.width
        for i in range(board.height):
            for j in range(board.width):
                if i < heights[j] - 1:
                    if data[i][j] == (0, 0, 0):
                        has_holes[j] = 1

        self.num_col_with_holes = sum(has_holes)
        return self.num_col_with_holes

    def get_row_transitions(self, board):
        # intialize as 0
        transitions_sum = 0
        dt = board.get_data()
        # start from the max height of the tetris instance to ignore empty rows
        max_height = board.height - max(self.get_column_height(board))
        # iterate through each row
        for i in range(max_height, board.height, 1):
            # iterate through each column
            for j in range(1, board.width, 1):
                # transition = XOR of the occupance of previous column cell to current column cell
                p1 = not (dt[i][j-1] == (0, 0, 0))
                p2 = not (dt[i][j] == (0, 0, 0))
                transitions_sum += p1 ^ p2
        # return total number of transitions
        self.row_transitions = transitions_sum
        return transitions_sum

    def get_col_transitions(self, board):
        # intialize as 0
        transitions_sum = 0
        dt = board.get_data()
        # start from the peak of each column to ignore empty rows on top
        peaks = self.get_column_height(board)
        # iterate through each column
        for i in range(board.width):
            # iterate through each row
            for j in range(board.height - peaks[i], board.width):
                # transition = XOR of the occupance of previous row cell to current row cell
                p1 = not (dt[j-1][i] == (0,0,0))
                p2 = not (dt[j][i] == (0,0,0))
                transitions_sum += p1 ^ p2
        # return total number of transitions
        self.col_transitions = transitions_sum
        return transitions_sum

    # get depth of wells in each column if any
    def get_wells(self, board):
        # get heights of each column
        peaks = self.get_column_height(board)
        # initialize well depth as 0 for each column
        well_depth = [0 for _ in range(board.width)]

        # special case for first and last column
        well_depth[0] = max((peaks[1] - peaks[0]), 0)
        well_depth[board.width - 1] = max((peaks[board.width - 2] - peaks[board.width - 1]), 0)

        # iterate through 2nd column to (n-1)th column
        for i in range(1, board.width - 1):
            # depth wrt prev column
            well_before = max(peaks[i - 1] - peaks[i], 0)
            # depth wrt next column
            well_after = max(peaks[i + 1] - peaks[i], 0)
            # max depth out of the two
            well_depth[i] = max(well_before, well_after)

        self.well_depth = well_depth
        # return depth of each column
        return well_depth

    def get_max_well(self, board):
        wells = self.get_wells(board)
        self.max_well = max(wells)
        return self.max_well

    def print_summary(self):
        print("=============================")
        print("Aggregate Height: " + str(self.aggregate_height))
        print("Column Height: " + str(self.column_height))
        print("Hole Count: " + str(self.hole_count))
        print("Bumpiness: " + str(self.bumpiness))
        print("Lines Cleared: " + str(self.lines_cleared))
        print("Score: " + str(self.score))
        print("Random Weight: " + str(self.random_weight))

    def return_all_params(self):
        return (-self.aggregate_height, -self.hole_count, -self.bumpiness,
                -self.num_pits, -self.max_well, -self.num_col_with_holes,
                -self.row_transitions, -self.col_transitions, self.score)

    def return_opponent_params(self):
        return (self.aggregate_height, self.hole_count, self.bumpiness,
                self.num_pits, self.max_well, self.num_col_with_holes,
                self.row_transitions, self.col_transitions, -self.score)

def get_piece_rotations(piece_temp):
    rotation_groups = [
        ['I', '_'],
        ['O'],
        ['uT', '-|', 'T', '|-'],
        ['S', 'h'],
        ['Z', 'nl'],
        [':__', 'r', '--,', 'J'],
        ['__:', '`|', ',--', 'L']
    ]
    possible_shapes_nm = []
    for g in rotation_groups:
        if piece_temp.shape in g:
            possible_shapes_nm = g

    possible_shapes = []
    # iterate through each rotation for the piece
    for rotation in possible_shapes_nm:
        # generate the numpy shape for each rotation and append it to the list
        p = Piece(piece_temp.width, piece_temp.height, -1)
        p.shape = rotation
        possible_shapes.append(p)
    # return the list
    return possible_shapes

def generate_piece_possibilities(tetris, model, piece_rotations, opponent=None):
    width = tetris.width
    height = tetris.height
    possible_moves_result = []
    initial_board = tetris.board

    if not initial_board.data[-1][0] == (0,0,0):
        #print("Failed!")
        return []

    for piece in piece_rotations:
        # print("Checking piece: " + piece.shape)
        for x_start in range(width):
            # print("Checking x: " + str(x_start))
            piece.center = (x_start, piece.center[1])
            tmp_tetris = Tetris(width, height)
            tmp_tetris.piece = piece
            tmp_tetris.board = initial_board.get_copy()

            if not tmp_tetris.is_overlap():
                tmp_tetris.snap_piece()
                params = ModelParams(generate=True, board=tmp_tetris.board)
                # calculate fitness for the respective next_piece orientation
                if opponent == None:
                    fitness = model.activate(params.return_all_params())[0]
                else:
                    opponent_params = ModelParams(generate=True, board=opponent).return_opponent_params()
                    training_params = params.return_all_params()
                    combined_params = training_params + opponent_params
                    fitness = model.activate(combined_params)[0]

                if x_start is not None:
                    # append rotation, column number, fitness and next_piece_fitness rounded to 5 decimals
                    possible_moves_result.append([piece, x_start, round(fitness, 5)])
    return possible_moves_result


def try_possible_moves(tetris, model, opponent=None):
    """
    Driver method for generate_piece_possibilities.
    It generates the respective numpy arrays for further
    computations in generate_piece_possibilities.
    """

    current_piece_temp = get_piece_rotations(tetris.piece)

    """
    sort all the possible moves based on sum of the current and future possibilities,
    then based on the least number of shifts required, then based on the least
    number of rotations required, in a descending order
    """
    possible_moves_result = sorted(generate_piece_possibilities(tetris, model, current_piece_temp, opponent=opponent),
                                   key=lambda p: (p[2],
                                                  - abs(p[1] - tetris.piece.center[0])),
                                   reverse=True)
    # return the list of possibilities
    return possible_moves_result