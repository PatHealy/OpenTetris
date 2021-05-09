import sys
from sty import fg, bg, ef, rs, RgbFg
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

class TerminalTetrisRunner:

	def __init__(self):
		self.tetris_grid = TetrisGrid()
		self.width = 16
		self.height = 16
		self.game = Tetris(self.width, self.height)

	def new_game(self):
		self.game = Tetris(self.width, self.height)
		self.erase_board()

	def delete_last_lines(self,n):
		CURSOR_UP_ONE = '\033[F' #'\x1b[1A'
		ERASE_LINE = '\033[K' #'\x1b[2K'
		for _ in range(n):
			sys.stdout.write(CURSOR_UP_ONE)
			sys.stdout.write(ERASE_LINE)

	def erase_board(self):
		self.delete_last_lines(self.height + 3)

	def print_board(self):
		data = self.game.get_board()
		self.tetris_grid.set_grid(data)
		for i in range(len(data)):
			line = ''
			for cell in data[len(data) - 1 - i]:
				line = line + fg(cell[0], cell[1], cell[2]) + '@' + fg.rs
			print(line)

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

	def play(self):
		print("WASD to move, R to rotate, X to quit")
		while True:
			while not self.game.is_failed():
				self.print_board()
				self.get_input()
				self.erase_board()
			self.print_board()
			self.get_input()
			self.new_game()

class TetrisGrid(SampleBase):
	def __init__(self, *args, **kwargs):
		super(TetrisGrid, self).__init__(*args, **kwargs)
		self.tet_grid = []
			for x in range(16):
				row = []
				for y in range(16):
					if x%2 == y%2:
						row.append((0,0,0))
					else:
						row.append((255,255,255))
				self.tet_grid.append(row)

	def set_grid(self, gr):
		self.tet_grid = gr

	def run(self):
		offset_canvas = self.matrix.CreateFrameCanvas()
		while True:
			for x in range(self.matrix.width):
				for y in range(self.matrix.height):
					c = self.tet_grid[(int(x))/4][(int(y))/4]
					offset_canvas.SetPixel(x, y, c[0], c[1], c[2])
			offset_canvas = self.matrix.SwapOnVSync(offset_canvas)


# Main function
# if __name__ == "__main__":
#     tetris_grid = TetrisGrid()
#     if (not tetris_grid.process()):
#         tetris_grid.print_help()


if __name__ == '__main__':
	runner = TerminalTetrisRunner()
	runner.play()
