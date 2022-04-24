import pygame
from core.game import TetrisRunner

class PygameTetrisRunner(TetrisRunner):
	def __init__(self, width=10, height=20, debug_mode=False):
		super().__init__(width, height, debug_mode=debug_mode)
		pygame.init()
		pygame.display.set_caption('Open Tetris')
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode([width * 50, (height+3) * 50])
		self.tick = 0

	def erase_board(self):
		self.screen.fill((0, 0, 0))

	def draw_grid(self):
		for i in range(self.width-1):
			pygame.draw.rect(self.screen, (100,100,100), pygame.Rect(i * 50 + 48, 0, 4, (self.height+3)*50))
		for i in range(self.height+2):
			pygame.draw.rect(self.screen, (100,100,100), pygame.Rect(0, i * 50 + 48, self.width*50, 4))

	def display_board(self):
		data = self.game.get_board()

		for y in range(len(data)):
			for x in range(len(data[y])):
				cell = data[y][x]
				pygame.draw.rect(self.screen, cell, pygame.Rect(x*50, (self.height-y+2)*50, 50, 50))

		self.draw_grid()

		pygame.display.flip()

	def get_input(self):
		success = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					success = self.game.move_piece('left')
					self.tick = 0
				elif event.key == pygame.K_w:
					self.tick = 0
					success = self.game.snap_piece()
				elif event.key == pygame.K_s:
					self.tick = 0
					success = self.game.move_piece('down')
				elif event.key == pygame.K_d:
					self.tick = 0
					success = self.game.move_piece('right')
				elif event.key == pygame.K_r:
					self.tick = 0
					success = self.game.rotate_piece()
				elif event.key == pygame.K_x:
					pygame.quit()
					exit()
		self.tick = self.tick + 1
		if self.tick > 5:
			keys = pygame.key.get_pressed()
			if keys[pygame.K_a]:
				success = self.game.move_piece('left')
				self.tick = 0
			elif keys[pygame.K_d]:
				success = self.game.move_piece('right')
				self.tick = 0
			elif keys[pygame.K_s]:
				success = self.game.move_piece('down')
				self.tick = 0
		if self.tick > 45:
			success = self.game.move_piece('down')
			self.tick = 0

		self.clock.tick(40)
		return success

	def play(self):
		super().play()
		pygame.quit()