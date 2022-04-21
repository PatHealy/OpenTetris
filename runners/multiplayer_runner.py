import pygame
from core.entities import Tetris

class MultiplayerRunner:
	def __init__(self, width=10, height=20, debug_mode=False):
		self.width = width
		self.height = height
		self.debug_mode = debug_mode
		self.player1 = Tetris(self.width, self.height, debug_mode=debug_mode)
		self.player2 = Tetris(self.width, self.height, debug_mode=debug_mode)
		pygame.init()
		pygame.display.set_caption('Open Tetris')
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode([(2 * width + 1) * 50, (height + 3) * 50])
		self.p1tick = 0
		self.p2tick = 0

	def new_game(self):
		self.player1 = Tetris(self.width, self.height, debug_mode=self.debug_mode)
		self.player2 = Tetris(self.width, self.height, debug_mode=self.debug_mode)
		self.erase_board()

	def erase_board(self):
		self.screen.fill((0, 0, 0))

	def display_board(self):
		p1_data = self.player1.get_board()
		p2_data = self.player2.get_board()

		for y in range(len(p1_data)):
			for x in range(len(p1_data[y])):
				cell = p1_data[y][x]
				pygame.draw.rect(self.screen, cell, pygame.Rect(x * 50, (self.height - y + 2) * 50, 50, 50))

		for y in range(len(p2_data)):
			for x in range(len(p2_data[y])):
				cell = p2_data[y][x]
				pygame.draw.rect(self.screen, cell, pygame.Rect(x * 50 + self.width * 50 + 50, (self.height - y + 2) * 50, 50, 50))

		pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(self.width * 50, 0, 50, 50 * self.height))
		pygame.display.flip()

	def display_winner(self):
		announcement = "Player 1 Wins!"
		if self.player1.is_failed():
			announcement = "Player 2 Wins!"
		font = pygame.font.Font(None, 25)
		text = font.render(announcement, True, (255, 255, 255))
		text_rect = text.get_rect(center=(((2 * self.width + 1) * 50) / 2, ((self.height + 3) * 50) / 2))
		self.screen.blit(text, text_rect)

	def get_input(self):
		# success = False
		# for event in pygame.event.get():
		# 	if event.type == pygame.QUIT:
		# 		pygame.quit()
		# 		exit()
		# 	if event.type == pygame.KEYDOWN:
		# 		if event.key == pygame.K_a:
		# 			success = self.game.move_piece('left')
		# 			self.tick = 0
		# 		elif event.key == pygame.K_w:
		# 			self.tick = 0
		# 			success = self.game.snap_piece()
		# 		elif event.key == pygame.K_s:
		# 			self.tick = 0
		# 			success = self.game.move_piece('down')
		# 		elif event.key == pygame.K_d:
		# 			self.tick = 0
		# 			success = self.game.move_piece('right')
		# 		elif event.key == pygame.K_r:
		# 			self.tick = 0
		# 			success = self.game.rotate_piece()
		# 		elif event.key == pygame.K_x:
		# 			pygame.quit()
		# 			exit()
		# self.tick = self.tick + 1
		# if self.tick > 5:
		# 	keys = pygame.key.get_pressed()
		# 	if keys[pygame.K_a]:
		# 		success = self.game.move_piece('left')
		# 		self.tick = 0
		# 	elif keys[pygame.K_d]:
		# 		success = self.game.move_piece('right')
		# 		self.tick = 0
		# 	elif keys[pygame.K_s]:
		# 		success = self.game.move_piece('down')
		# 		self.tick = 0
		# if self.tick > 45:
		# 	success = self.game.move_piece('down')
		# 	self.tick = 0
		#
		# self.clock.tick(40)
		# return success
		pass

	def play(self):
		while True:
			while not self.player1.is_failed() or self.player2.is_failed():
				self.display_board()
				self.get_input()
				self.erase_board()
			self.display_board()
			self.get_input()
			self.new_game()


if __name__ == '__main__':
	runner = MultiplayerRunner()
	runner.display_winner()
# runner.play()
