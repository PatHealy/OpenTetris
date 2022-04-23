

from copy import copy

# importing numpy module for evaluating game paramters
import numpy as np

# import global variable of the game scope
from global_variables import NUM_COLUMNS, NUM_ROWS, SCORING_VECTOR
# import the Piece class to be used for type annotation
from piece import Piece



# template class to evaluate the metrics of an instance of Tetris
class TetrisParams:
    # default initialization
    def __init__(self, matrix):
        # initiate matrix
        self.matrix = np.array(matrix)
        # sum of heights of all columns
        self.agg_height = self.get_aggregate_height()
        # total number of holes in the matrix
        self.total_holes = self.get_total_holes()
        # bumpiness of the tetris instance
        self.bumpiness = self.get_bumpiness()
        # total number of empty columns in the matrix
        self.num_pits = self.get_num_pits()
        # height of the deepest well
        self.max_well = self.get_max_well()
        # number of columns with atleast one hole
        self.num_col_with_holes = self.get_num_column_with_holes()
        # number of row transitions i.e. block to hole and vice-versa transitions in a row
        self.row_transitions = self.get_row_transitions()
        # number of column transitions i.e. block to hole and vice-versa transitions in a column
        self.col_transitions = self.get_col_transitions()
        # score achieved in the this Tetris instance
        self.score_achieved = SCORING_VECTOR[self.get_num_lines_cleared()]

    # heights of ech column
    def get_peaks(self):
        # position of max index in each column
        peaks = np.argmax(self.matrix, axis=0)
        # set peaks with 0 height as 20
        peaks[peaks == 0] = len(self.matrix)
        # take compliment of the current peak values to get heights of each columns
        peaks = len(self.matrix) * np.ones(peaks.shape) - peaks
        # return heights
        return np.array(peaks, dtype=int)

    def get_highest_peak(self):
        # get max height
        return np.max(self.get_peaks())

    def get_aggregate_height(self):
        # get sum of all heights
        return np.sum(self.get_peaks())

    # get number of holes in each column
    def get_holes(self):
        # initialize empty list
        holes_per_col = list()
        # get heights of each list
        peaks = self.get_peaks()
        # iterate though columns
        for i in range(NUM_COLUMNS):
            # append to the list the number of holes in each column
            holes_per_col.append(peaks[i] - np.sum(self.matrix[-peaks[i]:, i]) if peaks[i] != 0 else 0)
        # return list of holes in each column
        return holes_per_col

    # get total number of holes in the matrix
    def get_total_holes(self):
        holes_per_col = np.array(self.get_holes())
        return np.sum(holes_per_col)

    # get number of columns with atleast one hole
    def get_num_column_with_holes(self):
        return np.count_nonzero(np.array(self.get_holes()))

    # get number of block to hole and vice-versa transitions in a row
    def get_row_transitions(self):
        # intialize as 0
        transitions_sum = 0
        # start from the max height of the tetris instance to ignore empty rows
        max_height = NUM_ROWS - self.get_highest_peak()
        # iterate through each row
        for i in range(max_height, NUM_ROWS, 1):
            # iterate through each column
            for j in range(1, NUM_COLUMNS, 1):
                # transition = XOR of the occupance of previous column cell to current column cell
                transitions_sum += self.matrix[i, j - 1] ^ self.matrix[i, j]
        # return total number of transitions
        return transitions_sum

    # get number of block to hole and vice-versa transitions in a column
    def get_col_transitions(self):
        # intialize as 0
        transitions_sum = 0
        # start from the peak of each column to ignore empty rows on top
        peaks = self.get_peaks()
        # iterate through each column
        for i in range(NUM_COLUMNS):
            # iterate through each row
            for j in range(NUM_ROWS - peaks[i], NUM_ROWS):
                # transition = XOR of the occupance of previous row cell to current row cell
                transitions_sum += self.matrix[j - 1, i] ^ self.matrix[j, i]
        # return total number of transitions
        return transitions_sum

    # bumpiness is the sum of the differences in consecutive heights
    def get_bumpiness(self):
        # get heights of each column
        peaks = self.get_peaks()
        # initialize as 0
        bumpiness = 0
        # iterate through columns
        for i in range(1, NUM_COLUMNS):
            bumpiness += abs(peaks[i] - peaks[i - 1])
        # return total
        return bumpiness

    # get number of columns with no blocks
    def get_num_pits(self):
        return NUM_COLUMNS - np.count_nonzero(np.sum(self.matrix, axis=0))

    # get depth of wells in each column if any
    def get_wells(self):
        # get heights of each column
        peaks = self.get_peaks()
        # initialize well depth as 0 for each column
        well_depth = [0 for _ in range(NUM_COLUMNS)]

        """
        max(x, 0)   ->  means rectified linear unit function (ReLU)
                        basically, it returns x if x > 0 else 0
        """

        # special case for first and last column
        well_depth[0] = max((peaks[1] - peaks[0]), 0)
        well_depth[NUM_COLUMNS - 1] = max((peaks[NUM_COLUMNS - 2] - peaks[NUM_COLUMNS - 1]), 0)

        # iterate through 2nd column to (n-1)th column
        for i in range(1, NUM_COLUMNS - 1):
            # depth wrt prev column
            well_before = max(peaks[i - 1] - peaks[i], 0)
            # depth wrt next column
            well_after = max(peaks[i + 1] - peaks[i], 0)
            # max depth out of the two
            well_depth[i] = max(well_before, well_after)

        # return depth of each column
        return well_depth

    # get max depth 
    def get_max_well(self):
        return np.max(self.get_wells())

    # get number of lines cleared in the Tetris instance
    def get_num_lines_cleared(self):
        # get sum of each row
        row_sums = np.sum(self.matrix, axis=1)
        # initialize as 0
        num_lines = 0
        # iterate through each row
        for r in row_sums:
            # increment number of cleared lines if sum for the row is same as number of columns
            num_lines += 1 if r == NUM_COLUMNS else 0
        # return the total number of lines
        return num_lines

    # return all the calculations as a tuple
    def return_all_params(self):

        """
        Note:   here, all the un-desirable attributes are put with '-' signs as a 
                fix, because after few trail runs, I observed that most generations
                were being initialized with positive weights, thus in-order save
                few generation cycles I negated these attributes by default. 
        """

        return (-self.agg_height, -self.total_holes, -self.bumpiness,
                -self.num_pits, -self.max_well, -self.num_col_with_holes,
                -self.row_transitions, -self.col_transitions, self.score_achieved)


def get_numpy_shape(formatted_shape):
    """
    Returns a numpy matrix representing orientaions of a single
    shape using 0s and 1s, where 0 represents grid cell unoccupied 
    and 1 represents grid cell occupied.

    Eg - 

      *                     0 1
    * *     is encoded as   1 1
      *                     0 1

      *                     0 1 0
    * * *   is encoded as   1 1 1

    *                       1 0
    * *     is encoded as   1 1
    *                       1 0  

    * * *   is encoded as   1 1 1
      *                     0 1 0
    """
    # list of x coordinates
    x_coords = [x for x, _ in formatted_shape]
    # list of y coordinates
    y_coords = [y for _, y in formatted_shape]
    # shape of matrix
    rows = (max(y_coords) - min(y_coords) + 1)
    cols = (max(x_coords) - min(x_coords) + 1)
    # initialize matrix as zeros
    template = np.zeros(shape=(rows, cols), dtype=int)
    # iterate through all coordinates
    for x, y in formatted_shape:
        # mark those coordinates as 1
        template[y - min(y_coords)][x - min(x_coords)] = 1
    # return the numpy array
    return template


def get_piece_rotations(piece_temp: Piece):
    """
    Returns all the possible orientations for a Piece
    in the format specified by get_numpy_shape

    Check: ``help(utils.get_numpy_shape)`` for example
    """
    # initialize list
    possible_numpy_shapes = list()
    # iterate through each rotation for the piece
    for rotation in range(len(piece_temp.shape)):
        # generate the numpy shape for each rotation and append it to the list
        possible_numpy_shapes.append(get_numpy_shape(piece_temp.get_formatted_shape()))
        # rotate the piece 
        piece_temp.rotation = (piece_temp.rotation + 1) % len(piece_temp.shape)
    # return the list
    return possible_numpy_shapes


def generate_piece_possibilities(init_matrix, model, piece_rotations, next_piece_rotations=None):

    # initialize list
    possible_moves_result = []
    # initialize as negative infinity
    best_next_fitness = np.NINF

    # iterate through each rotation
    for rotation, piece in enumerate(piece_rotations):
        # get shape of piece
        y_len, x_len = piece.shape
        # iterate through each column possible
        for x_start in range(NUM_COLUMNS - x_len + 1):

            # initialize to start from the 0th row
            y_start = 0
            # copy of the matrix, so that the same original matrix is used for each case
            matrix = init_matrix.copy()

            # run loop while the piece doesnt reach the bottom of the column
            while y_start + y_len <= NUM_ROWS:
                # copy of the matrix, so that the same original matrix is used for each case
                matrix = init_matrix.copy()
                # add the piece to the matrix
                matrix[y_start:y_start + y_len, x_start:x_start + x_len] += piece
                # if any coordinate overlaps, it means the bottom for that column is reached
                if 2 in matrix:
                    # reset the matrix
                    matrix = init_matrix.copy()
                    # since this iteration overlapped, it means previous y coordinate was to be used
                    y_start -= 1
                    # if previous iteration was 0th row, it means column full, so skip this column
                    if y_start == -1:
                        # mark x_start none for this so that it can be skipped
                        x_start = None
                    # if the column is not full
                    else:
                        # get the matrix from previous iteration of y_start
                        matrix[y_start:y_start + y_len, x_start:x_start + x_len] += piece
                    break
                # increment y_start to shift the piece down                    
                y_start += 1

            # ================================= CASE 2 =================================
            # the calculation is for next_piece 
            if next_piece_rotations is None:
                # calculate Parameters of the matrix with the next_piece
                params = TetrisParams(matrix)
                # calculate fitness for the respective next_piece orientation
                fitness = model.activate(params.return_all_params())[0]
                # if this is more than best_fitness
                if fitness > best_next_fitness:
                    # then replace it
                    best_next_fitness = fitness
            # ================================= CASE 1 =================================
            # the calculation is for current_piece
            else:
                # call the function again for Case 2, to get the best fitness achievable with the next_piece
                next_piece_fitness = generate_piece_possibilities(matrix, model, next_piece_rotations,
                                                                  next_piece_rotations=None)
                # calculate Parameters of the matrix with the current_piece
                params = TetrisParams(matrix)
                # calculate fitness for the current_piece orientation
                fitness = model.activate(params.return_all_params())[0]
                # if the column was not full
                if x_start is not None:
                    # append rotation, column number, fitness and next_piece_fitness rounded to 5 decimals
                    possible_moves_result.append([rotation, x_start, round(fitness, 5), round(next_piece_fitness, 5)])

    # ================================= CASE 2 =================================
    if next_piece_rotations is None:
        # just return the best possible fitness with the next_piece
        return best_next_fitness
    # ================================= CASE 1 =================================
    else:
        # return the list of possible moves along with the possible fitness and best possible future fitness
        return possible_moves_result


def try_possible_moves(tetris, model):
    """
    Driver method for generate_piece_possibilities.
    It generates the respective numpy arrays for further 
    computations in generate_piece_possibilities.
    """

    # generate numpy array equivalent of the tetris grid
    matrix = np.array(tetris.get_grid_state(), dtype=int)
    # generate possible numpy orientations for current_piece
    current_piece_temp = get_piece_rotations(copy(tetris.current_piece))
    # generate possible numpy orientations for next_piece
    next_piece_temp = get_piece_rotations(copy(tetris.next_piece))

    """
    sort all the possible moves based on sum of the current and future possibilities,
    then based on the least number of shifts required, then based on the least
    number of rotations required, in a descending order

    """
    possible_moves_result = sorted(generate_piece_possibilities(matrix, model, current_piece_temp, next_piece_temp),
                                   key=lambda p: (p[2] + p[3],
                                                  - abs(p[1] - tetris.current_piece.x),
                                                  - abs(p[0] - tetris.current_piece.rotation)),
                                   reverse=True)
    # return the list of possibilities
    return possible_moves_result
