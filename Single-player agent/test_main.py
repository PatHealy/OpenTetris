
import os
import pickle

from time import sleep

import neat

import pygame

from tetris import Tetris

from global_variables import ROTATE_KEY, RIGHT_KEY, LEFT_KEY, DOWN_KEY

from utils import try_possible_moves


pygame.init()
# set caption of game window
pygame.display.set_caption('Tetris')
# load icon for game
icon = pygame.image.load('./.images/game_logo.png')
# set icon for the game
pygame.display.set_icon(icon)

# open the winner genome file
with open("winner.pickle", 'rb') as genome_file:
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
model = neat.nn.FeedForwardNetwork.create(genome, config)


# cdriver method
def main():
    # create tetris instance
    t = Tetris()
    # while game is not over and game window is not closed
    while t.game_running and not t.game_over:

        # iterate through events in the pygame window
        for event in pygame.event.get():
            # if the window is closed or escape key is pressed
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # end game
                t.game_running = False
                # kill pygame display
                pygame.display.quit()
                # kill script execution
                quit()

        # get list possible moves along with the respective current and future fitness
        possible_moves_result = try_possible_moves(t, model)
        # if list is not empty
        if possible_moves_result:
            # best moves correspond to 0th position because of descending sort
            best_rotation, x_position, _, _ = possible_moves_result[0]

            # run an empty frame to show piece
            t.play_game(None)
            # to help in visualize piece before any action is taken
            sleep(0.1)

            # while current_rotation does not match the best rotation
            while t.current_piece.rotation != best_rotation:
                # keep rotating
                t.play_game(ROTATE_KEY)
                # to help in visualize piece for each action
                sleep(0.1)

            # while min x coord does not match the best x coord keep shifting accordingly
            while x_position != min([x for x, _ in t.current_piece.get_formatted_shape()]):
                # if it's toward right
                if x_position > min([x for x, _ in t.current_piece.get_formatted_shape()]):
                    # move right
                    t.play_game(RIGHT_KEY)
                # if it's toward left
                else:
                    # move left
                    t.play_game(LEFT_KEY)
                # to help in visualize piece for each action
                sleep(0.1)

            # pull down the piece to the bottom-most possible position
            t.play_game(DOWN_KEY)
            # play one frame of game
            t.play_game(None)
        # if the possible moves list is empty, means that no possible moves left
        else:
            # exit game
            t.game_over = True
            # kill pygame display
            pygame.display.quit()
            # kill script execution
            quit()


if __name__ == '__main__':
    main()
