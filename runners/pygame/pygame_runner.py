import pygame
from core.game import TetrisRunner

class PygameTetrisRunner(TetrisRunner):
	def __init__(self, width=10, height=20):
		super().__init__(width, height)
		pygame.init()
		pygame.display.set_caption('Open Tetris')
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode([width * 50, (height+3) * 50])
		self.tick = 0

	def erase_board(self):
		self.screen.fill((0, 0, 0))

	def display_board(self):
		data = self.game.get_board()
		for y in range(len(data)):
			for x in range(len(data[y])):
				cell = data[y][x]
				pygame.draw.rect(self.screen, cell, pygame.Rect(x*50, (self.height-y+2)*50, 50, 50))
		pygame.display.flip()

	def get_input(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

		success = False
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			self.tick = 0
			success = self.game.snap_piece()
		elif keys[pygame.K_a]:
			self.tick = 0
			success = self.game.move_piece('left')
		elif keys[pygame.K_s]:
			self.tick = 0
			success = self.game.move_piece('down')
		elif keys[pygame.K_d]:
			self.tick = 0
			success = self.game.move_piece('right')
		elif keys[pygame.K_r]:
			self.tick = 0
			success = self.game.rotate_piece()
		elif keys[pygame.K_x]:
			pygame.quit()
			exit()
		else:
			self.tick = self.tick + 1
			if self.tick > 5:
				self.tick = 0
				success = self.game.move_piece('down')
		self.clock.tick(7)
		return success

	def play(self):
		super().play()
		pygame.quit()

if __name__ == '__main__':
	runner = PygameTetrisRunner()
	runner.play()