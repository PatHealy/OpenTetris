import os
import pickle
import neat

from core.utilities import try_possible_moves
from core.entities import Tetris
from runners.pygame_runner import PygameTetrisRunner

class SingleTester:
    def __init__(self, width=10, height=20, cell_size=50, pickle_fn="./single_player/winner.pickle"):
        self.width = width
        self.height = height
        self.pg = PygameTetrisRunner(width, height, cell_size=cell_size)
        self.human_watchable = True

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

    def display_game(self):
        self.pg.erase_board()
        self.pg.display_board()
        if self.human_watchable:
            self.pg.clock.tick_busy_loop(30)

    def play_loop(self):
        while not self.pg.game.is_failed():
            # get list possible moves along with the respective current and future fitness
            possible_moves_result = try_possible_moves(self.pg.game, self.model)
            # if list is not empty
            if possible_moves_result:
                # best moves correspond to 0th position because of descending sort
                best_rotation, x_position, _ = possible_moves_result[0]
                self.display_game()

                while self.pg.game.piece.shape != best_rotation.shape:
                    self.pg.game.rotate_piece()
                    self.display_game()

                # while min x coord does not match the best x coord keep shifting accordingly
                while x_position != self.pg.game.piece.center[0]:
                    # if it's toward right
                    if x_position > self.pg.game.piece.center[0]:
                        # move right
                        self.pg.game.move_piece("right")
                    # if it's toward left
                    else:
                        # move left
                        self.pg.game.move_piece("left")
                    self.display_game()

                self.pg.game.snap_piece()
                self.display_game()
                #
        self.display_game()
        return self.pg.game.get_score(), self.pg.game.board.get_lines_cleared()

    def test(self, trials=100):
        self.human_watchable = False
        scores = []
        lcs = []
        for i in range(trials):
            print("Playing game " + str(i))
            score, line_clear = self.play_loop()
            scores.append(score)
            lcs.append(line_clear)
            self.pg.new_game()

        print()
        print("======== PERFORMANCE SUMMARY ===========")
        print("Over " + str(trials) + " trials")
        print("Average score: " + str(sum(scores)/float(trials)))
        print("Average line clears: " + str(sum(lcs)/float(trials)))
        print("=================================")
        self.human_watchable = True

    def play(self):
        while True:
            self.play_loop()
            print("=================================")
            print("Game Over!")
            print("Score achieved: " + str(self.pg.game.get_score()))
            print("Lines cleared: " + str(self.pg.game.board.get_lines_cleared()))
            print("=================================")
            self.pg.wait_for_input()
            self.pg.new_game()
