import os
import pickle
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

# to keep track on generations
gen_index = 0
# to keep track of best solution over all generations
max_fitness = 0


# driver method
def main_game(genomes, config):
    global gen_index, max_fitness


    gen_index += 1

    gen = list()

    tetrises = list()

    models = list()

    for genome_id, genome in genomes:
        # append model corresponding to the genome
        models.append(neat.nn.FeedForwardNetwork.create(genome, config))
        # append a tetris instance for the genome
        tetrises.append(Tetris())
        # initialize the fitness of the genome as 0
        genome.fitness = 0
        # append the genome to the list
        gen.append(genome)

    # run until all tetris instances are not over
    while len(models) > 0:
        # iterate through each instance of tetris, model and genome
        for t, m, g in zip(tetrises, models, gen):
            # get list possible moves along with the respective current and future fitness
            possible_moves_result = try_possible_moves(t, m)
            # if list is not empty
            if possible_moves_result:
                # best moves correspond to 0th position because of descending sort
                best_rotation, x_position, _, _ = possible_moves_result[0]

                # while current_rotation does not match the best rotation
                while t.current_piece.rotation != best_rotation:
                    # keep rotating
                    t.play_game(ROTATE_KEY)

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

                # pull down the piece to the bottom-most possible position
                t.play_game(DOWN_KEY)
                # play one frame of game
                t.play_game(None)
            # if the possible moves list is empty, means that no possible moves left
            else:
                # exit game
                t.game_over = True

            # assign the fitness as score, implying that higher score means more fitness
            g.fitness = t.score

            # if current fitness is better than global max_fitness
            if g.fitness > max_fitness:
                # re-assign global max_fitness
                max_fitness = g.fitness

                # empty the directory with the last global high scorer model
                max_fit_model_dir = os.listdir("./max_fit_model/")
                # iterate through each file
                for file_name in max_fit_model_dir:
                    # delete each file
                    os.remove("./max_fit_model/" + file_name)

                # create a file for global high scorer model
                with open("max_fit_model/max_fit_model_" + str(t.score) + ".pickle", 'wb') as model_file:
                    # save the model
                    pickle.dump(g, model_file)

            # if game is over 
            if t.check_game_over() or t.game_over:
                # get global index from the populations
                removed_index = [genome_id for genome_id, genome in genomes if genome == g][0]
                # print stats for reference
                print("Model Killed: {}, Models Left: {}, Generation: {}, Fitness: {}".format
                      (removed_index, len(models) - 1, gen_index - 1, t.score))
                # remove the tetris instance
                tetrises.pop(tetrises.index(t))
                # remove model instance
                models.pop(models.index(m))
                # remove genome instance
                gen.pop(gen.index(g))


# method to run the genetic algorithm over the driver method
def run(config_file):
    # extract details from the config file
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # directory for storing checkpoints
    checkpoint_dir = os.listdir("checkpoints/")
    # if directory is empty
    if not checkpoint_dir:
        # start new population
        pop = neat.Population(config)
    # if directory is not empty
    else:
        # initialize empty list
        checkpoint_list = list()
        # iterate through each file
        for checkpoint in checkpoint_dir:
            # append to list the indices of the checkpoints
            checkpoint_list.append(checkpoint[16:])
        # descending sort the checkpoint list and get the max value
        checkpoint = sorted(checkpoint_list, reverse=True)[0]
        # restore population from last checkpoint
        pop = neat.Checkpointer().restore_checkpoint("checkpoints/neat-checkpoint-" + str(checkpoint))
        # print which checkpoint is loaded
        print("Loaded last checkpoint: ", checkpoint)

    # uses print to output information about the run method
    pop.add_reporter(neat.StdOutReporter(True))
    # gathers and provides the most-fit genomes and info on genome and species fitness and species sizes.
    pop.add_reporter(neat.StatisticsReporter())
    # performs checkpointing, saving and restoring the simulation state.
    pop.add_reporter(neat.Checkpointer(generation_interval=1, time_interval_seconds=1200,
                                       filename_prefix='checkpoints/neat-checkpoint-'))
    # find the winner genome by running the main_game method for 20 generations
    winner = pop.run(main_game, 20)

    # display the characteristics of the winner genome
    print('\n\nBest genome: {!s}'.format(winner))
    # create a file for winner model
    with open("winner.pickle", 'wb') as model_file:
        # save the model
        pickle.dump(winner, model_file)


if __name__ == '__main__':
    # name of directory containing this file
    local_dir = os.path.dirname(__file__)
    # path to the config file
    config_path = os.path.join(local_dir, 'config.txt')
    # call run method with config file path
    run(config_path)
