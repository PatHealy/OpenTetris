# AI to play OpenTetris
# Largely adapted from https://medium.com/acing-ai/how-i-build-an-ai-to-play-dino-run-e37f37bdf153
import sys
from sty import fg, bg, ef, rs, RgbFg
from entities import Tetris
import os

class AITerminalDriver:
	def __init__(self, width=10, height=20):
		self.width = width
		self.height = height
		self.game = Tetris(self.width, self.height)
		self.print_board()
		self.clear_ticker = 0
		for n in range(self.height + 3):
			print()

	def new_game(self):
		self.game = Tetris(self.width, self.height)
		self.delete_last_lines(50)
		self.erase_board()

	def slide_up_lines(self, n):
		CURSOR_UP_ONE = '\033[F' #'\x1b[1A'
		ERASE_LINE = '\033[K' #'\x1b[2K'
		for _ in range(n):
			sys.stdout.write(CURSOR_UP_ONE)

	def delete_last_lines(self,n):
		CURSOR_UP_ONE = '\033[F' #'\x1b[1A'
		ERASE_LINE = '\033[K' #'\x1b[2K'
		sys.stdout.write(CURSOR_UP_ONE)
		for _ in range(n):
			sys.stdout.write(CURSOR_UP_ONE)
			sys.stdout.write(ERASE_LINE)

	def erase_board(self):
		if self.clear_ticker > 500:
			self.clear_ticker = 0
			os.system('clear')
		else:
			self.slide_up_lines(self.height + 4)
		self.clear_ticker = self.clear_ticker + 1
		#self.delete_last_lines(50)

	def print_board(self):
		data = self.game.get_board()
		for i in range(len(data)):
			line = ''
			for cell in data[len(data) - 1 - i]:
				line = line + fg(cell[0], cell[1], cell[2]) + '@' + fg.rs
			print(line)

	def get_board(self):
		board = self.game.get_board()
		piece_coordinates = self.game.piece.get_coordinates()

		this_board = [[0 for x in range(self.width)] for y in range(self.height + 3)]

		for y in range(self.height+3):
			for x in range(self.width):
				if not board[y][x] == (0,0,0):
					this_board[y][x] = 1

		for c in piece_coordinates:
			this_board[c[1]][c[0]] = 2

		return this_board

	def get_score(self):
		return self.game.get_score()

	def rotate(self):
		self.game.rotate_piece()

	def snap(self):
		self.game.snap_piece()

	def move(self, direction):
		self.game.move_piece(direction)

	def is_failed(self):
		return self.game.is_failed()
