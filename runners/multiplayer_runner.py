import pygame
from core.entities import Tetris

class MultiplayerRunner:
	def __init__(self, width=10, height=20, debug_mode=False, cell_size=50):
		self.width = width
		self.height = height
		self.debug_mode = debug_mode
		self.cell_size=cell_size
		self.player1 = Tetris(self.width, self.height, debug_mode=debug_mode)
		self.player2 = Tetris(self.width, self.height, debug_mode=debug_mode)
		pygame.init()
		pygame.display.set_caption('Open Tetris')
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode([(2 * width + 1) * self.cell_size, (height + 3) * self.cell_size])
		self.p1tick = 0
		self.p2tick = 0

	def new_game(self):
		self.clock.tick_busy_loop(120)
		pygame.display.set_caption('Open Tetris')
		self.player1 = Tetris(self.width, self.height, debug_mode=self.debug_mode)
		self.player2 = Tetris(self.width, self.height, debug_mode=self.debug_mode)
		self.erase_board()

	def erase_board(self):
		self.screen.fill((0, 0, 0))

	def draw_grid(self, xOffset):
		for i in range(self.width-1):
			pygame.draw.rect(self.screen, (100,100,100), pygame.Rect(i * self.cell_size + self.cell_size - 2 + xOffset, 0, 4, (self.height+3)*self.cell_size))
		for i in range(self.height+2):
			pygame.draw.rect(self.screen, (100,100,100), pygame.Rect(xOffset, i * self.cell_size + self.cell_size - 2, self.width*self.cell_size, 4))

	def display_board(self):
		p1_data = self.player1.get_board()
		p2_data = self.player2.get_board()

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

	def display_winner(self):
		announcement = "Player 1 Wins!"
		if self.player1.is_failed():
			announcement = "Player 2 Wins!"
		print(announcement)
		pygame.display.set_caption(announcement)

	def get_input(self):
		p1success = False
		p2success = False
		p1_total_lines_cleared = self.player1.board.lines_cleared
		p2_total_lines_cleared = self.player2.board.lines_cleared

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.KEYDOWN:
				#Get player 1 input
				if event.key == pygame.K_a:
					p1success = self.player1.move_piece('left')
					self.p1tick = 0
				elif event.key == pygame.K_w:
					self.p1tick = 0
					p1success = self.player1.snap_piece()
				elif event.key == pygame.K_s:
					self.p1tick = 0
					p1success = self.player1.move_piece('down')
				elif event.key == pygame.K_d:
					self.p1tick = 0
					p1success = self.player1.move_piece('right')
				elif event.key == pygame.K_r:
					self.p1tick = 0
					p1success = self.player1.rotate_piece()
				#Get Player 2 input
				if event.key == pygame.K_LEFT:
					p2success = self.player2.move_piece('left')
					self.p2tick = 0
				elif event.key == pygame.K_UP:
					self.p2tick = 0
					p2success = self.player2.snap_piece()
				elif event.key == pygame.K_DOWN:
					self.p2tick = 0
					p2success = self.player2.move_piece('down')
				elif event.key == pygame.K_RIGHT:
					self.p2tick = 0
					p2success = self.player2.move_piece('right')
				elif event.key == pygame.K_RCTRL:
					self.p2tick = 0
					p2success = self.player2.rotate_piece()
				if event.key == pygame.K_x:
					pygame.quit()
					exit()

		self.p1tick = self.p1tick + 1
		self.p2tick = self.p2tick + 1

		#Player 1 ticks
		if self.p1tick > 5:
			keys = pygame.key.get_pressed()
			if keys[pygame.K_a]:
				p1success = self.player1.move_piece('left')
				self.p1tick = 0
			elif keys[pygame.K_d]:
				p1success = self.player1.move_piece('right')
				self.p1tick = 0
			elif keys[pygame.K_s]:
				p1success = self.player1.move_piece('down')
				self.p1tick = 0
		if self.p1tick > 45:
			p1success = self.player1.move_piece('down')
			self.p1tick = 0

		#Player 2 ticks
		if self.p2tick > 5:
			keys = pygame.key.get_pressed()
			if keys[pygame.K_LEFT]:
				p2success = self.player2.move_piece('left')
				self.p2tick = 0
			elif keys[pygame.K_RIGHT]:
				p2success = self.player2.move_piece('right')
				self.p2tick = 0
			elif keys[pygame.K_DOWN]:
				p2success = self.player2.move_piece('down')
				self.p2tick = 0
		if self.p2tick > 45:
			p2success = self.player2.move_piece('down')
			self.p2tick = 0

		p1_line_clears = self.player1.board.lines_cleared - p1_total_lines_cleared
		p2_line_clears = self.player2.board.lines_cleared - p2_total_lines_cleared

		if p1_line_clears == 2:
			self.player2.add_opponent_lines(1)
		elif p1_line_clears == 3:
			self.player2.add_opponent_lines(2)
		elif p1_line_clears == 4:
			self.player2.add_opponent_lines(4)

		if p2_line_clears == 2:
			self.player1.add_opponent_lines(1)
		elif p2_line_clears == 3:
			self.player1.add_opponent_lines(2)
		elif p2_line_clears == 4:
			self.player1.add_opponent_lines(4)

		self.clock.tick(40)
		return p1success, p2success

	def play(self):
		while True:
			while not (self.player1.is_failed() or self.player2.is_failed()):
				self.display_board()
				self.get_input()
				self.erase_board()
			self.display_winner()
			self.new_game()


if __name__ == '__main__':
	runner = MultiplayerRunner()
	runner.display_winner()
# runner.play()
