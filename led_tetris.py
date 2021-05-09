from entities import Tetris
from matrix_examples.python.samples.samplebase import SampleBase

class _Getch:
	"""Gets a single character from standard input.  Does not echo to the
	screen."""
	def __init__(self):
		try:
			self.impl = _GetchWindows()
		except ImportError:
			self.impl = _GetchUnix()

	def __call__(self): return self.impl()

class _GetchUnix:
	def __init__(self):
		import tty, sys

	def __call__(self):
		import sys, tty, termios
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch

class _GetchWindows:
	def __init__(self):
		import msvcrt

	def __call__(self):
		import msvcrt
		return msvcrt.getch()


class GridTetrisRunner(SampleBase):
	def __init__(self):
		super(TetrisGrid, self).__init__(*args, **kwargs)
		self.width = 16
		self.height = 16
		self.game = Tetris(self.width, self.height)

	def new_game(self):
		self.game = Tetris(self.width, self.height)
		self.print_board()

	def print_board(self):
		data = self.game.get_board()
		for x in range(self.matrix.width):
				for y in range(self.matrix.height):
					c = data[int(x/4)][int(y/4)]
					offset_canvas.SetPixel(x, y, c[0], c[1], c[2])
			offset_canvas = self.matrix.SwapOnVSync(offset_canvas)

	def get_input(self):
		char = _Getch().__call__()
		success = False

		if char == 'w':
			success = self.game.snap_piece()
		elif char == 'a':
			success = self.game.move_piece('left')
		elif char == 's':
			success = self.game.move_piece('down')
		elif char == 'd':
			success = self.game.move_piece('right')
		elif char == 'r':
			success = self.game.rotate_piece()
		elif char == 'x':
			exit()

		return success

	def run(self):
		print("WASD to move, R to rotate, X to quit")
		offset_canvas = self.matrix.CreateFrameCanvas()
		while True:
			while not self.game.is_failed():
				self.print_board()
				self.get_input()
				#self.erase_board()
			self.print_board()
			self.get_input()
			self.new_game()



if __name__ == '__main__':
	runner = GridTetrisRunner()
	if (not runner.process()):
		runner.print_help()
	# runner.play()