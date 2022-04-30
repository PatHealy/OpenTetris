import os
import pickle
import neat

from core.utilities import try_possible_moves
from core.entities import Tetris

from rgbmatrix import RGBMatrix, RGBMatrixOptions

import time

class LEDTester:
    def __init__(self, width=10, height=20, pickle_fn="./led_board/winner.pickle"):
        self.width = width
        self.height = height

        self.game = Tetris(self.width, self.height, debug_mode=False)
        self.prior_data = self.game.get_board()

        matrix_options = RGBMatrixOptions()
        matrix_options.rows = 64
        matrix_options.cols = 64
        matrix_options.brightness = 100

        self.matrix = RGBMatrix(options=matrix_options)

        self.offset_canvas = self.matrix.CreateFrameCanvas()

        print(self.matrix.width)
        print(self.matrix.height)

        # open the winner genome file
        with open(pickle_fn, 'rb') as genome_file:
            # load the winner genome to the genome variable
            genome = pickle.load(genome_file)

        # name of directory containing this file
        local_dir = os.path.dirname(__file__)
        # path to the config file
        config_path = os.path.join(local_dir, 'config.txt')
        # extract details from the config file
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    config_path)
        # model corresponding to the winning genome
        self.model = neat.nn.FeedForwardNetwork.create(genome, config)

    def new_game(self):
        self.game = Tetris(self.width, self.height)
        self.erase_board()

    def erase_board(self):
        self.matrix.Clear()

    def display_game(self):
        data = self.game.get_board()
        for x in range(self.matrix.width):
            for y in range(self.matrix.height):
                if data[int(y / 4)][int(x / 4)] != self.prior_data[int(y / 4)][int(x / 4)]:
                    c = data[int(y / 4)][int(x / 4)]
                    # self.offset_canvas.SetPixel(x, y, c[0], c[1], c[2])
                    self.matrix.SetPixel(x, y, c[0], c[1], c[2])
        # self.offset_canvas = self.matrix.SwapOnVSync(self.offset_canvas)
        self.prior_data = data

    def play_loop(self):
        while not self.game.is_failed():
            # get list possible moves along with the respective current and future fitness
            possible_moves_result = try_possible_moves(self.game, self.model)
            # if list is not empty
            if possible_moves_result:
                # best moves correspond to 0th position because of descending sort
                best_rotation, x_position, _ = possible_moves_result[0]
                self.display_game()

                while self.game.piece.shape != best_rotation.shape:
                    self.game.rotate_piece()
                    self.display_game()

                # while min x coord does not match the best x coord keep shifting accordingly
                while x_position != self.game.piece.center[0]:
                    # if it's toward right
                    if x_position > self.game.piece.center[0]:
                        # move right
                        self.game.move_piece("right")
                    # if it's toward left
                    else:
                        # move left
                        self.game.move_piece("left")
                    self.display_game()

                while self.game.move_piece("down"):
                    self.display_game()
                self.display_game()

        self.display_game()
        return self.game.get_score(), self.game.board.get_lines_cleared()

    def play(self):
        while True:
            self.play_loop()
            self.display_game()
            time.sleep(10)
            self.new_game()

if __name__ == "__main__":
    tester = LEDTester(width=16, height=16)
    tester.play()