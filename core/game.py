from core.entities import Tetris

class TetrisRunner:

	def __init__(self, width=10, height=20, debug_mode=False):
		self.width = width
		self.height = height
		self.game = Tetris(self.width, self.height, debug_mode=debug_mode)

	def new_game(self):
		self.game = Tetris(self.width, self.height)
		self.erase_board()

	def erase_board(self):
		"""Set the game board display to empty"""
		pass

	def display_board(self):
		"""Display tetrominos in the game board display. Ignores empty space."""
		pass

	def get_input(self):
		""""""
		pass

	def play(self):
		while True:
			while not self.game.is_failed():
				self.display_board()
				self.get_input()
				self.erase_board()
			self.display_board()
			self.get_input()
			self.new_game()