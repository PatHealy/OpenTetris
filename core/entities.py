# Objects related to the game of tetris
import random
import operator

from core.utilities import *


class Piece:
	def __init__(self, width, height, previous_shape):
		self.types = {
			'I': ((0,-1), (0,1), (0,2)), # vertical line
			'_': ((-1,0), (1,0), (2,0)), # horizontal line

			'O': ((0,1), (1,0), (1,1)), # square

			'uT': ((0,1), (1,0), (-1,0)), # upside-down T
			'-|': ((-1,0), (0,-1), (0,1)), # T on its right side
			'T': ((0,-1), (1,0), (-1,0)), # T
			'|-': ((1,0), (0,1), (0,-1)), # T on its left side

			'S': ((-1,0), (0,1), (1,1)), # S
			'h': ((0,1), (1,0), (1,-1)), # S on its side\

			'Z': ((1,0), (0,1), (-1,1)), # Z
			'nl': ((-1,0), (-1,-1), (0,1)), # Z on its side

			':__': ((1,0), (-1,0), (-1,1)), # J on its right side
			'r': ((0,1), (1,1), (0,-1)), # Upside down J
			'--,': ((1,0), (1,-1), (-1,0)), #J on its left side
			'J': ((0,1), (0,-1), (-1,-1)), # J

			'__:': ((-1,0), (1,0), (1,1)), # L on its left side
			'`|': ((0,1), (0,-1), (-1,1)), # L upside down
			',--': ((1,0), (-1,0), (-1,-1)), # L on its right side
			'L': ((0,-1), (1,-1), (0,1)) # L
		}
		self.edges = {
			'I': '_',
			'_': 'I',

			'O': 'O',

			'uT': '-|',
			'-|': 'T',
			'T': '|-',
			'|-': 'uT',

			'S': 'h',
			'h':'S',

			'Z': 'nl',
			'nl': 'Z',

			':__': 'J',
			'r': ':__',
			'--,': 'r',
			'J': '--,',

			'__:': '`|',
			'`|': ',--',
			',--': 'L',
			'L': '__:'
		}

		starters = ['_', 'O', 'uT', 'S', 'Z', ':__', '__:']
		colors = [(0, 240, 240), (240, 240, 0), (160, 0, 240), (0, 240, 0), (240, 0, 0), (0, 0, 240), (240, 160, 0)]

		shape_index = random.randint(0, len(starters)-1)
		while shape_index == previous_shape:
			shape_index = random.randint(0, len(starters) - 1)
		self.shape_index = shape_index
		self.shape = starters[shape_index]
		self.color = colors[shape_index]
		self.width = width
		self.height = height
		self.center = (width//2, height + 1)

	def rotate(self):
		self.shape = self.edges[self.shape]

	def move(self,direction):
		if direction == 'down':
			self.center = tuple(map(operator.add, self.center, (0,-1)))
		elif direction == 'up':
			self.center = tuple(map(operator.add, self.center, (0,1)))
		elif direction == 'left':
			self.center = tuple(map(operator.add, self.center, (-1,0)))
		elif direction == 'right':
			self.center = tuple(map(operator.add, self.center, (1,0)))

		return self.get_coordinates()

	def get_color(self):
		return self.color

	def get_coordinates(self):
		coordinates = []
		coordinates.append((self.center[0], self.center[1]))

		for c in self.types[self.shape]:
			coordinates.append(tuple(map(operator.add, self.center, c)))

		return coordinates

	def get_copy(self):
		tmp = Piece(self.width, self.height, -1)
		tmp.shape_index = self.shape_index
		tmp.shape = self.shape
		tmp.color = self.color
		tmp.center = self.center
		return tmp

class Board:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.data = [[(0,0,0) for x in range(width)] for y in range(height + 4)]
		self.score = 0
		self.lines_cleared = 0

	def get_data(self):
		data_copy = [[(self.data[y][x][0], self.data[y][x][1], self.data[y][x][2]) for x in range(self.width)] for y in range(self.height + 4)]
		return data_copy

	def fail_board(self):
		for i in range(len(self.data)):
			for j in range(len(self.data[i])):
				if self.data[i][j] == (0,0,0):
					self.data[i][j] = (50,0,0)

	def is_failed(self):
		for cell in self.data[self.height]:
			if not (cell == (0,0,0)):
				self.fail_board()
				return True
		return False

	def check_for_line_clear(self):
		lines_cleared = 0
		for i in range(len(self.data)):
			clear = True
			for cell in self.data[i]:
				if cell == (0,0,0) or cell == (255,255,255):
					clear = False
			if clear:
				lines_cleared = lines_cleared + 1
				self.data[i] = [(255,255,255) for x in range(self.width)]
		self.lines_cleared = self.lines_cleared + lines_cleared
		self.score = self.score + 100*lines_cleared**2

	def remove_cleared_lines(self):
		i = 0
		while i < len(self.data):
			if self.data[i][0] == (255,255,255):
				j = i
				while j < len(self.data) - 1:
					self.data[j] = [x for x in self.data[j + 1]]
					j = j + 1
			else:
				i += 1

	def number_of_diffs(self, oldd, newd):
		diffs = 0
		for i in range(len(oldd)):
			for j in range(len(oldd[0])):
				if not (oldd[i][j] == newd[i][j]):
					diffs += 1
		return diffs

	def add_piece(self, piece, debug=False):
		coordinates = piece.get_coordinates()
		color = piece.get_color()

		for c in coordinates:
			if not self.data[c[1]][c[0]] == (0,0,0):
				return False
		for c in coordinates:
			self.data[c[1]][c[0]] = (color[0], color[1], color[2])

		self.check_for_line_clear()
		return True

	def get_score(self):
		return 0 + self.score

	def get_lines_cleared(self):
		return 0 + self.lines_cleared

	def get_copy(self):
		tmp = Board(self.width, self.height)
		tmp.data = self.get_data()
		tmp.score = self.score
		tmp.lines_cleared = self.lines_cleared
		return tmp

class Tetris:
	def __init__(self, width, height, debug_mode=False):
		self.width = width
		self.height = height
		self.board = Board(width, height)
		self.piece = Piece(width, height, -1)
		self.debug_mode = debug_mode
		#goal coordinates used by AI
		self.goalX = None
		self.goalRotation = None

	def is_overlap(self):
		board_data = self.board.get_data()
		try:
			for c in self.piece.get_coordinates():
				if c[0] >= self.width:
					# print("Off stage right")
					return True
				elif c[0] < 0:
					# print("Off stage left")
					return True
				elif c[1] < 0:
					# print("Off bottom")
					return True
				if not board_data[c[1]][c[0]] == (0,0,0):
					# print("Occupied space")
					return True
			# print("Valid piece")
		except IndexError:
			return True
		return False

	def move_piece(self, direction, snapping=False):
		if self.is_failed():
			if self.debug_mode:
				print("Failed move")
			return False
		self.board.remove_cleared_lines()
		opposites = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
		self.piece.move(direction)

		if self.is_overlap():
			while self.is_overlap():
				self.piece.move(opposites[direction])
			if direction == 'down' and not snapping:
				self.snap_piece()
			return False
		return True

	def rotate_piece(self):
		if self.is_failed():
			return False
		self.board.remove_cleared_lines()

		self.piece.rotate()

		if self.is_overlap():
			self.piece.rotate()
			self.piece.rotate()
			self.piece.rotate()
			return False

		return True

	def snap_piece(self):
		if self.is_failed():
			return False
		self.board.remove_cleared_lines()

		while self.move_piece('down', snapping=True):
			pass

		success = self.board.add_piece(self.piece, debug=self.debug_mode)
		self.piece = Piece(self.width, self.height, self.piece.shape_index)

		if self.debug_mode:
			params = ModelParams(generate=True, board=self.board)
			params.print_summary()
		return success

	def is_failed(self):
		return self.board.is_failed()

	def get_board(self):
		data = self.board.get_data()

		#make the current piece visible
		color = self.piece.get_color()
		for c in self.piece.get_coordinates():
			data[c[1]][c[0]] = color

		return data

	def get_score(self):
		return self.board.get_score()

	def add_opponent_lines(self, nlines):
		for i in range(nlines):
			row = [(70, 70, 70) for x in range(self.width)]
			row[random.randint(0, self.width-1)] = (0,0,0)
			self.board.data = [row] + self.board.data[:-1]

	def get_copy(self):
		tmp = Tetris(self.width, self.height, debug_mode=self.debug_mode)
		tmp.board = self.board.get_copy()
		tmp.piece = self.piece.get_copy()
		return tmp
