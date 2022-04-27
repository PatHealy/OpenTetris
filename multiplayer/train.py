import os
import pickle
import neat

from core.utilities import try_possible_moves
from core.entities import Tetris
from runners.vs_ai_runner import VsAIRunner

class MultiplayerTrainer:
	def __init__(self, width=10, height=20, cell_size=50):
		self.width = width
		self.height = height
		self.pg = VsAIRunner(width, height, cell_size=cell_size)
		self.t_lines_cleared = 0
		self.o_lines_cleared = 0

	def display_game(self):
		self.pg.erase_board()
		self.pg.display_board(p1Name="MP AI")

	def train(self):
		# to keep track on generations
		self.gen_index = 0
		# to keep track of best solution over all generations
		self.max_fitness = 0

		# name of directory containing this file
		local_dir = os.path.dirname(__file__)
		# path to the config file
		config_path = os.path.join(local_dir, 'config.txt')
		# extract details from the config file
		config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
		                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
		                            config_path)

		# directory for storing checkpoints
		checkpoint_dir = os.listdir("multiplayer/checkpoints/")
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
			pop = neat.Checkpointer().restore_checkpoint("multiplayer/checkpoints/neat-checkpoint-" + str(checkpoint))
			# print which checkpoint is loaded
			print("Loaded last checkpoint: ", checkpoint)

		# uses print to output information about the run method
		pop.add_reporter(neat.StdOutReporter(True))
		# gathers and provides the most-fit genomes and info on genome and species fitness and species sizes.
		pop.add_reporter(neat.StatisticsReporter())
		# performs checkpointing, saving and restoring the simulation state.
		pop.add_reporter(neat.Checkpointer(generation_interval=1, time_interval_seconds=1200,
		                                   filename_prefix='multiplayer/checkpoints/neat-checkpoint-'))
		# find the winner genome by running the main_game method for 20 generations
		winner = pop.run(self.main_game, 20)

		# display the characteristics of the winner genome
		print('\n\nBest genome: {!s}'.format(winner))
		# create a file for winner model
		with open("./multiplayer/winner.pickle", 'wb') as model_file:
			# save the model
			pickle.dump(winner, model_file)

	def check_opponent_line_adds(self):
		p1_line_clears = self.pg.humanPlayer.board.lines_cleared - self.t_lines_cleared
		p2_line_clears = self.pg.aiPlayer.board.lines_cleared - self.o_lines_cleared

		if p1_line_clears == 2:
			self.pg.aiPlayer.add_opponent_lines(1)
		elif p1_line_clears == 3:
			self.pg.aiPlayer.add_opponent_lines(2)
		elif p1_line_clears == 4:
			self.pg.aiPlayer.add_opponent_lines(4)

		if p2_line_clears == 2:
			self.pg.humanPlayer.add_opponent_lines(1)
		elif p2_line_clears == 3:
			self.pg.humanPlayer.add_opponent_lines(2)
		elif p2_line_clears == 4:
			self.pg.humanPlayer.add_opponent_lines(4)


	def main_game(self, genomes, config):
		self.gen_index += 1
		gen = list()
		tetrises = list()
		opponents = list()
		models = list()
		for genome_id, genome in genomes:
			# append model corresponding to the genome
			models.append(neat.nn.FeedForwardNetwork.create(genome, config))
			# append a tetris instance for the genome
			tetrises.append(Tetris(self.width, self.height))
			opponents.append(Tetris(self.width, self.height))
			# initialize the fitness of the genome as 0
			genome.fitness = 0
			# append the genome to the list
			gen.append(genome)

		# run until all tetris instances are not over
		while len(models) > 0:
			# iterate through each instance of tetris, model and genome
			for t, o, m, g in zip(tetrises, opponents, models, gen):
				self.pg.humanPlayer = t
				self.pg.aiPlayer = o
				self.display_game()

				self.t_lines_cleared = self.pg.humanPlayer.board.get_lines_cleared()
				self.o_lines_cleared = self.pg.aiPlayer.board.get_lines_cleared()

				# get list possible moves along with the respective current and future fitness
				possible_moves_result = try_possible_moves(t, m, opponent=o.board)

				line_interrupted = False

				# if list is not empty
				if (not t.is_failed()) and possible_moves_result:
					# best moves correspond to 0th position because of descending sort
					best_rotation, x_position, _ = possible_moves_result[0]

					# while current_rotation does not match the best rotation
					while self.pg.humanPlayer.piece.shape != best_rotation.shape and not line_interrupted:
						# keep rotating
						rotated = self.pg.humanPlayer.rotate_piece()
						if not rotated:
							line_interrupted = True
							break
						self.pg.ai_move()
						self.check_opponent_line_adds()
						self.o_lines_cleared = self.pg.aiPlayer.board.get_lines_cleared()
						self.display_game()

					# while min x coord does not match the best x coord keep shifting accordingly
					while x_position != self.pg.humanPlayer.piece.center[0] and not line_interrupted:
						# if it's toward right
						if x_position > self.pg.humanPlayer.piece.center[0]:
							# move right
							moved = self.pg.humanPlayer.move_piece("right")
							if not moved:
								line_interrupted = True
							self.pg.ai_move()
							self.check_opponent_line_adds()
							self.o_lines_cleared = self.pg.aiPlayer.board.get_lines_cleared()
							self.display_game()
						# if it's toward left
						else:
							# move left
							moved = self.pg.humanPlayer.move_piece("left")
							if not moved:
								line_interrupted = True
							self.pg.ai_move()
							self.check_opponent_line_adds()
							self.o_lines_cleared = self.pg.aiPlayer.board.get_lines_cleared()
							self.display_game()
					# pull down the piece to the bottom-most possible position
					snapped = self.pg.humanPlayer.snap_piece()
					if not snapped:
						line_interrupted = True
					self.pg.ai_move()
					self.check_opponent_line_adds()
					self.t_lines_cleared = self.pg.humanPlayer.board.get_lines_cleared()
					self.o_lines_cleared = self.pg.aiPlayer.board.get_lines_cleared()
					self.display_game()
				# if the possible moves list is empty, means that no possible moves left

				# assign the fitness as score, implying that higher score means more fitness
				g.fitness = self.pg.humanPlayer.get_score()

				# if current fitness is better than global max_fitness
				if g.fitness > self.max_fitness:
					# re-assign global max_fitness
					self.max_fitness = g.fitness

					# empty the directory with the last global high scorer model
					max_fit_model_dir = os.listdir("./multiplayer/max_fit_model/")
					# iterate through each file
					for file_name in max_fit_model_dir:
						# delete each file
						os.remove("./multiplayer/max_fit_model/" + file_name)

					# create a file for global high scorer model
					with open("./multiplayer/max_fit_model/max_fit_model_" + str(t.get_score()) + ".pickle",
					          'wb') as model_file:
						# save the model
						pickle.dump(g, model_file)

				# if game is over
				if self.pg.humanPlayer.is_failed():
					# get global index from the populations
					removed_index = [genome_id for genome_id, genome in genomes if genome == g][0]
					# print stats for reference
					print("Model Killed: {}, Models Left: {}, Generation: {}, Fitness: {}".format
					      (removed_index, len(models) - 1, self.gen_index - 1, t.get_score()))
					# remove the tetris instance
					tetrises.pop(tetrises.index(t))
					opponents.pop(opponents.index(o))
					# remove model instance
					models.pop(models.index(m))
					# remove genome instance
					gen.pop(gen.index(g))