import neat
import os
from utilities import *
import sys
sys.path.insert(0, './core')
from entities import *

#Fitness function to determine best genome
def eval_genomes(genome, config):

    #iterate through genomes
    #for genome_id, genome in genomes:        
    
    #set intial fitness
    fitness = 0

    #create neural network
    net = neat.nn.FeedForwardNetwork.create(genome, config)


    #Play the game
    #as long as game is active - move, rotate, & drop pieces
    

    #Heuristics from Utilities.py increase or decrease fitness
    #Example: score
        #game.get_score()
        #fitness += score
    
    

#Using configuration file, create the population and iterate through generations
def run(config_file):

    #Load the configuration
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    #Create the initial population
    pop = neat.Population(config)

    #Output generation progress to the terminal
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    #Run X number of generations
    fittest = pop.run(eval_genomes, 100)

    #Display the fittest genome
    print('\nBest Genome:\n{!s}'.format(fittest))

    #Compare fittest genome to training data
    #fittest_genome = neat.nn.FeedForwardNetwork.create(fittest, config)

    #pop.run(eval_genomes, 10)
    
#Load configuration file then call run
if __name__=="__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-tetris')

    #change inputs, outputs, population, etc depending on modifications to fitness function
    run(config_path)
