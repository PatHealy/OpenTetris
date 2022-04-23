
from random import choice
# import respective object type for type hint specification
from typing import List, Tuple, Dict

# import pygame module
import pygame
# from piece import Piece
# from shapes import *
# from global_variables import *
# import global variable for the game scope
from global_variables import *
# import the Piece class to be used as instance variables for Tetris class
from piece import Piece
# import the list of Shapes and their respective colors
from shapes import *


# template class for the game
class Tetris:
    # type specifiers for class instance variables
    window: pygame.Surface
    fall_speed: float
    fall_time: int
    game_clock: pygame.time.Clock
    change_current_piece: bool
    next_piece: Piece
    current_piece: Piece
    game_over: bool
    game_running: bool
    locked_pos: Dict[Tuple[int, int], Tuple[int, int, int]]
    score: int
    grid: List[List[Tuple[int, int, int]]]

    # default initialization
    def __init__(self):
        # keep track of the grid as 2-D list of (R,G,B) values
        self.grid = [[(0, 0, 0) for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]
        # score for game as 10x for each line removed
        self.score = 0
        # dictionary of grid points that have been occupied by the various pieces
        self.locked_pos = dict()
        # to kill game if ESC is pressed or windows is closed
        self.game_running = True
        # to kill game if blocks reach out the visible region
        self.game_over = False
        # variable to track the current piece
        self.current_piece = Piece(5, 0, choice(SHAPES_LIST))
        # variable to display the next piece
        self.next_piece = Piece(5, 0, choice(SHAPES_LIST))
        # variable to indicate that current piece has reached the maximum ground and next piece needs to be loaded
        self.change_current_piece = False
        # game clock to keep track of game ticks
        self.game_clock = pygame.time.Clock()
        # variable indicate the speed of the block and to indicate the motion of falling pieces
        self.fall_time = 0
        # variable that caps the max fall time
        self.fall_speed = 0.27
        # game window surface
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # generate grid from locked_pos variable
    def set_grid(self):
        # iterate through grid rows
        for i, g in enumerate(self.grid):
            # iterate through grid columns for respective row
            for j, _ in enumerate(g):
                # if the respective block is occupied then put that specific color
                if (j, i) in self.locked_pos:
                    self.grid[i][j] = self.locked_pos[(j, i)]
                # else set the block as empty
                else:
                    self.grid[i][j] = (0, 0, 0)

        # return grid object in case required
        return self.grid

    # check if game is over
    def check_game_over(self):
        # iterate through all locked coordinates
        for pos in self.locked_pos:
            # if y coordinate is out of grid region
            if pos[1] < 0:
                return True
        return False

    # clear the rows that are full and update locked_pos
    def clear_rows(self):
        # set initial number of cleared lines as 0
        num_cleared_rows = 0
        # check for each row
        for i in range(len(self.grid)):
            # if any block is empty skip row
            if (0, 0, 0) in self.grid[i]:
                continue

            # if row is complete then increment number of cleared lines
            num_cleared_rows += 1
            # for all columns in the respective row
            for j in range(len(self.grid[i])):
                # remove the old keys for the cleared row
                if (j, i) in self.locked_pos.keys():
                    del self.locked_pos[(j, i)]

            # make a temporary dictionary
            temp_locked_pos = dict()
            # iterate through key-value pairs
            for pos, val in self.locked_pos.items():
                x, y = pos
                # for rows above the cleared row
                if y < i:
                    # shift the row by one row
                    temp_locked_pos[(x, y + 1)] = val
                else:
                    # no need to shift rows
                    temp_locked_pos[(x, y)] = val

            # update old dictionary
            self.locked_pos = temp_locked_pos

        # increment score according to the scoring_vector
        self.score += SCORING_VECTOR[num_cleared_rows]

    # make game window
    def draw_game_window(self):
        # set background
        self.window.fill((100, 100, 100))
        # create font variable for on-screen text
        font = pygame.font.SysFont('comicsans', 48)
        # create TETRIS Heading for game window
        label = font.render('TETRIS', 1, (255, 255, 255))
        # display game heading
        self.window.blit(label, (TOP_LEFT[X] + PLAY_WIDTH / 2 - (label.get_width() / 2), 10))

        # fill the respective blocks with the color of the grids
        for i in range(len(self.grid)):  # row iteration
            for j in range(len(self.grid[i])):  # column iteration
                # draw a filled rectangle of the color according to that in the grid variable
                pygame.draw.rect(self.window, self.grid[i][j],
                                 (TOP_LEFT[X] + j * BLOCK_SIZE, TOP_LEFT[Y] + i * BLOCK_SIZE,
                                  BLOCK_SIZE, BLOCK_SIZE), 0)

        # draw reference grid white lines
        for i in range(NUM_ROWS):  # horizontal lines
            pygame.draw.line(self.window, (128, 128, 128),
                             (TOP_LEFT[X], TOP_LEFT[Y] + i * BLOCK_SIZE),
                             (TOP_LEFT[X] + PLAY_WIDTH, TOP_LEFT[Y] + i * BLOCK_SIZE))
        for i in range(NUM_COLUMNS):  # vertical lines
            pygame.draw.line(self.window, (128, 128, 128),
                             (TOP_LEFT[X] + i * BLOCK_SIZE, TOP_LEFT[Y]),
                             (TOP_LEFT[X] + i * BLOCK_SIZE, TOP_LEFT[Y] + PLAY_HEIGHT))

        # draw play area border
        pygame.draw.rect(self.window, (255, 0, 0),
                         (TOP_LEFT[X], TOP_LEFT[Y],
                          PLAY_WIDTH, PLAY_HEIGHT), 4)

        # create font variable for on-screen text with different font size
        font = pygame.font.SysFont('comicsans', 40)
        # create score label
        label = font.render('SCORE: ' + str(self.score), 1, (255, 255, 255))
        # display the score label on-screen
        self.window.blit(label, (TOP_LEFT[X] - 200, TOP_LEFT[Y] + PLAY_HEIGHT / 2 - 130))

        # draw next shape window
        start_x = TOP_LEFT[X] + PLAY_WIDTH + 20
        start_y = TOP_LEFT[Y] + PLAY_HEIGHT / 2 - 100
        # create next shape label
        label = font.render('Next Shape:', 1, (255, 255, 255))
        # display the next shape label on-screen
        self.window.blit(label, (start_x + 10, start_y - 30))
        # get the formatted shape of the next piece, so it can be easily drawn
        formatted_shape = self.next_piece.shape[self.next_piece.rotation % len(self.next_piece.shape)]

        # iterate through the list of lists of each shape
        for i, line in enumerate(formatted_shape):
            row = list(line)
            # for each column in the row
            for j, column in enumerate(row):
                # if the block is marked by * in the list
                if column == '*':
                    # draw a corresponding block of the respective shape color
                    pygame.draw.rect(self.window, self.next_piece.color,
                                     (start_x + j * BLOCK_SIZE, start_y + i * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE), 0)

    # return the state of grid with 0 as un-occupied and 1 as occupied blocks in a 2-D Array
    def get_grid_state(self):
        # make 2D list of lists with zeroes
        matrix = [[0 for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]
        # iterate through the actual grid
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                # if the grid element is black then mark as 0 else 1
                if self.grid[i][j] != (0, 0, 0):
                    matrix[i][j] = 1
        return matrix

    # function to play the game with the specified action for each frame
    def play_game(self, action=None):

        # create grid for this frame
        self.grid = self.set_grid()
        # increase fall time
        self.fall_time += self.game_clock.get_rawtime()
        # increase the game_clock so that it works the same way on platforms with different fps
        self.game_clock.tick()

        # piece falling effect
        # fall_time is in milliseconds
        # fall_time is greater than 0.27 seconds
        if self.fall_time / 1000 >= self.fall_speed:
            # reset fall time
            self.fall_time = 0
            # then increase the current piece y coordinate by 1 block
            self.current_piece.y += 1
            # if the piece is not in valid space i.e. it is out of grid space
            if not self.current_piece.in_valid_space(self.grid) and self.current_piece.y > 0:
                # then put it back in grid
                self.current_piece.y -= 1
                # change next_piece to current_piece
                self.change_current_piece = True

        if action is not None:
            # if user presses LEFT_KEY
            if action == LEFT_KEY:
                # decrease x coordinate
                self.current_piece.x -= 1
                # if block goes out of scope then undo
                if not self.current_piece.in_valid_space(self.grid):
                    self.current_piece.x += 1

            # if user presses RIGHT_KEY
            elif action == RIGHT_KEY:
                # increase x coordinate
                self.current_piece.x += 1
                # if block goes out of scope then undo
                if not self.current_piece.in_valid_space(self.grid):
                    self.current_piece.x -= 1

            # if user presses ROTATE_KEY
            elif action == ROTATE_KEY:
                # change current_piece orientation
                self.current_piece.rotation = (self.current_piece.rotation + 1) % len(self.current_piece.shape)
                # if block goes out of scope then undo
                if not self.current_piece.in_valid_space(self.grid):
                    self.current_piece.rotation = (self.current_piece.rotation - 1) % len(self.current_piece.shape)

            # if user presses DOWN_KEY
            elif action == DOWN_KEY:
                # while the current_piece does'nt reach the bottom, keep increase y coordinate                
                while self.current_piece.in_valid_space(self.grid):
                    self.current_piece.y += 1
                # since in valid space is violated now, so fix y coordinate by shifting one block up
                self.current_piece.y -= 1
                # set change_current_piece to get new_piece in the same frame cycle
                self.change_current_piece = True

                # add current piece to the grid
        # get formatted shape
        formatter_shape = self.current_piece.get_formatted_shape()
        # for each coordinate in formatted_shape
        for i in range(len(formatter_shape)):
            x, y = formatter_shape[i]
            # only if y is visible in grid space, then add color to grid
            if y > -1:
                self.grid[y][x] = self.current_piece.color

        # add to locked positions
        # if piece reaches the max height at the bottom of a column
        if self.change_current_piece:
            # for coordinates in formatted shape
            for pos in formatter_shape:
                # locked_pos[(x,y) of formatted_shape] = color of piece
                self.locked_pos[pos] = self.current_piece.color
            # reassign current piece to next piece
            self.current_piece = self.next_piece
            # select a new next piece for next_piece variable
            self.next_piece = Piece(5, 0, choice(SHAPES_LIST))
            # re-initialise change_current_piece state to False
            self.change_current_piece = False
            # clear rows if any full
            self.clear_rows()

        # draw game window
        self.draw_game_window()
        # update current screen
        pygame.display.update()
