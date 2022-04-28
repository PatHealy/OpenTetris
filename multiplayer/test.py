import os
import pickle
import neat

from core.utilities import try_possible_moves
from core.entities import Tetris
from runners.vs_ai_runner import VsAIRunner

class MultiplayerTester:
	def __init__(self, width=10, height=20, cell_size=50):
		self.width = width
		self.height = height
		self.pg = VsAIRunner(width, height, cell_size=cell_size)
		self.t_lines_cleared = 0
		self.o_lines_cleared = 0
		self.human_watchable = True

		with open("./multiplayer/winner.pickle", 'rb') as genome_file:
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
		self.pg.display_board(p1Name="MP AI")
		if self.human_watchable:
			self.pg.clock.tick(30)

	def test(self):
		while True:
			self.play()
			self.pg.display_winner("MP AI")
			self.pg.wait_for_input()
			self.pg.new_game()

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


	def play(self):
		self.display_game()
		self.t_lines_cleared = self.pg.humanPlayer.board.get_lines_cleared()
		self.o_lines_cleared = self.pg.aiPlayer.board.get_lines_cleared()

		# get list possible moves along with the respective current and future fitness
		possible_moves_result = try_possible_moves(self.pg.humanPlayer, self.model, opponent=self.pg.aiPlayer.board)

		line_interrupted = False
		# if list is not empty
		while (not self.pg.humanPlayer.is_failed()) and possible_moves_result:
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

			possible_moves_result = try_possible_moves(self.pg.humanPlayer, self.model,
			                                           opponent=self.pg.aiPlayer.board)

		while not self.pg.aiPlayer.is_failed():
			self.pg.ai_move()
			self.display_game()

		return self.pg.humanPlayer.get_score(), self.pg.humanPlayer.board.get_lines_cleared(), (self.pg.humanPlayer.get_score() > self.pg.aiPlayer.board.get_score())

	def test_stats(self, trials=100):
		self.human_watchable = False
		scores = []
		lcs = []
		wins = []
		for i in range(trials):
			print("Playing game " + str(i))
			score, line_clear, win = self.play()
			scores.append(score)
			lcs.append(line_clear)
			wins.append(win)
			if win:
				print("The agent won!")
			else:
				print("The agent lost.")
			self.pg.new_game()

		print("======== PERFORMANCE SUMMARY ===========")
		print("Over " + str(trials) + " trials")
		print("Average score: " + str(sum(scores) / float(trials)))
		print("Average line clears: " + str(sum(lcs) / float(trials)))
		print("Win percentage: " + str(100*sum(wins)/float(trials)) + "%")
		print("=================================")
		self.human_watchable = True