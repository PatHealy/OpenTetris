import pygame
from core.entities import Tetris

import os
import pickle
import neat

from core.utilities import try_possible_moves

class VsMPAIRunner:
	def __init__(self, width=10, height=20, debug_mode=False, cell_size=50):
		self.width = width
		self.height = height
		self.debug_mode = debug_mode
		self.cell_size=cell_size
		self.humanPlayer = Tetris(self.width, self.height, debug_mode=debug_mode)
		self.aiPlayer = Tetris(self.width, self.height, debug_mode=debug_mode)
		pygame.init()
		pygame.display.set_caption('Open Tetris')
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode([(2 * width + 1) * self.cell_size, (height + 3) * self.cell_size])
		self.tick = 0
		self.ai_tick = 0

		# open the winner genome file
		with open("./multiplayer/winner.pickle", 'rb') as genome_file:
			# load the winner genome to the genome variable
			genome = pickle.load(genome_file)

		# name of directory containing this file
		local_dir = os.path.dirname(__file__)
		# path to the config file
		config_path = './multiplayer/config.txt'
		# extract details from the config file
		config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
		                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
		                            config_path)
		# model corresponding to the winning genome
		self.model = neat.nn.FeedForwardNetwork.create(genome, config)

	def new_game(self):
		self.humanPlayer = Tetris(self.width, self.height, debug_mode=self.debug_mode)
		self.aiPlayer = Tetris(self.width, self.height, debug_mode=self.debug_mode)
		self.tick = 0
		self.ai_tick = 0
		self.erase_board()

	def erase_board(self):
		self.screen.fill((0, 0, 0))

	def draw_grid(self, xOffset):
		for i in range(self.width-1):
			pygame.draw.rect(self.screen, (100,100,100), pygame.Rect(i * self.cell_size + self.cell_size - 2 + xOffset, 3*self.cell_size, 4, (self.height+3)*self.cell_size))
		for i in range(self.height+2):
			if i > 1:
				pygame.draw.rect(self.screen, (100,100,100), pygame.Rect(xOffset, i * self.cell_size + self.cell_size - 2, self.width*self.cell_size, 4))

	def display_board(self, p1Name="Human"):
		p1_data = self.humanPlayer.get_board()
		p2_data = self.aiPlayer.get_board()

		for y in range(len(p1_data)):
			for x in range(len(p1_data[y])):
				cell = p1_data[y][x]
				pygame.draw.rect(self.screen, cell, pygame.Rect(x * self.cell_size, (self.height - y + 2) * self.cell_size, self.cell_size, self.cell_size))

		for y in range(len(p2_data)):
			for x in range(len(p2_data[y])):
				cell = p2_data[y][x]
				pygame.draw.rect(self.screen, cell, pygame.Rect(x * self.cell_size + self.width * self.cell_size + self.cell_size, (self.height - y + 2) * self.cell_size, self.cell_size, self.cell_size))

		pygame.draw.rect(self.screen, (150, 150, 150), pygame.Rect(self.width * self.cell_size, 0, self.cell_size, self.cell_size * (self.height+3)))
		self.draw_grid(0)
		self.draw_grid(self.width * self.cell_size + self.cell_size)

		pygame.display.flip()

		pygame.display.set_caption("Open Tetris | " + p1Name + " Score: " + str(self.humanPlayer.get_score()) + ", "
		                           + str(self.humanPlayer.board.get_lines_cleared()) + " lines cleared | MP AI Score: "
		                           + str(self.aiPlayer.get_score()) + ", "
		                           + str(self.aiPlayer.board.get_lines_cleared())
		                           + " lines cleared")

	def display_winner(self, p1Name="Human"):
		announcement = p1Name + " Wins!"
		if self.aiPlayer.get_score() > self.humanPlayer.get_score():
			announcement = "AI Wins!"
		print(announcement)
		pygame.display.set_caption(announcement
									+ " | Open Tetris | " + p1Name + " Score: " + str(self.humanPlayer.get_score()) + ", "
		                           + str(self.humanPlayer.board.get_lines_cleared()) + " lines cleared | MP AI Score: "
		                           + str(self.aiPlayer.get_score()) + ", "
		                           + str(self.aiPlayer.board.get_lines_cleared())
		                           + " lines cleared")

	def wait_for_input(self):
		tick = 0
		while tick < 160:
			tick += 1
			self.clock.tick(40)

		for event in pygame.event.get():
			pass
		events = 0
		while events == 0:
			for event in pygame.event.get():
				events += 1
			self.clock.tick(40)

	def ai_choose_move(self):
		possible_moves_result = try_possible_moves(self.aiPlayer, self.model, opponent=self.humanPlayer.board)
		# if list is not empty
		if possible_moves_result:
			# best moves correspond to 0th position because of descending sort
			self.aiPlayer.goalRotation, self.aiPlayer.goalX, _ = possible_moves_result[0]
			return True
		return False

	def ai_move(self):
		if not self.aiPlayer.is_failed():
			if self.aiPlayer.goalRotation is None:
				self.ai_choose_move()
			if self.aiPlayer.piece.shape != self.aiPlayer.goalRotation.shape:
				success = self.aiPlayer.rotate_piece()
				if not success:
					self.ai_choose_move()
			elif self.aiPlayer.goalX != self.aiPlayer.piece.center[0]:
				if self.aiPlayer.goalX > self.aiPlayer.piece.center[0]:
					success = self.aiPlayer.move_piece("right")
				else:
					success = self.aiPlayer.move_piece("left")
				if not success:
					self.ai_choose_move()
			else:
				self.aiPlayer.snap_piece()
				self.aiPlayer.goalRotation = None
				self.aiPlayer.goalX = None

	def get_input(self):
		humanMove = False
		p1_total_lines_cleared = self.humanPlayer.board.lines_cleared
		p2_total_lines_cleared = self.aiPlayer.board.lines_cleared

		if not self.humanPlayer.is_failed():
			#Get event inputs (keydowns)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_a:
						humanMove = self.humanPlayer.move_piece('left')
						self.tick = 0
					elif event.key == pygame.K_w:
						self.tick = 0
						humanMove = self.humanPlayer.snap_piece()
					elif event.key == pygame.K_s:
						self.tick = 0
						humanMove = self.humanPlayer.move_piece('down')
					elif event.key == pygame.K_d:
						self.tick = 0
						humanMove = self.humanPlayer.move_piece('right')
					elif event.key == pygame.K_r:
						self.tick = 0
						humanMove = self.humanPlayer.rotate_piece()

			self.tick = self.tick + 1

			#Player 1 ticks
			if self.tick > 5:
				keys = pygame.key.get_pressed()
				if keys[pygame.K_a]:
					humanMove = self.humanPlayer.move_piece('left')
					self.tick = 0
				elif keys[pygame.K_d]:
					humanMove = self.humanPlayer.move_piece('right')
					self.tick = 0
				elif keys[pygame.K_s]:
					humanMove = self.humanPlayer.move_piece('down')
					self.tick = 0
			if self.tick > 45:
				humanMove = self.humanPlayer.move_piece('down')
				self.tick = 0

		if not self.aiPlayer.is_failed():
			self.ai_tick += 1
			if self.ai_tick > 20:
				self.ai_tick = 0
				self.ai_move()

		p1_line_clears = self.humanPlayer.board.lines_cleared - p1_total_lines_cleared
		p2_line_clears = self.aiPlayer.board.lines_cleared - p2_total_lines_cleared

		if not self.aiPlayer.is_failed():
			if p1_line_clears == 2:
				self.aiPlayer.add_opponent_lines(1)
			elif p1_line_clears == 3:
				self.aiPlayer.add_opponent_lines(2)
			elif p1_line_clears == 4:
				self.aiPlayer.add_opponent_lines(4)

		if not self.humanPlayer.is_failed():
			if p2_line_clears == 2:
				self.humanPlayer.add_opponent_lines(1)
			elif p2_line_clears == 3:
				self.humanPlayer.add_opponent_lines(2)
			elif p2_line_clears == 4:
				self.humanPlayer.add_opponent_lines(4)

			self.clock.tick(40)

	def play(self):
		while True:
			while not (self.humanPlayer.is_failed() and self.aiPlayer.is_failed()):
				self.display_board()
				self.get_input()
				self.erase_board()
			self.erase_board()
			self.display_board()
			self.display_winner()
			self.wait_for_input()
			self.new_game()
