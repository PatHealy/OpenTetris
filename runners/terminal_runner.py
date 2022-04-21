import sys
from sty import fg, bg, ef, rs, RgbFg
from core.game import TetrisRunner

class TerminalTetrisRunner(TetrisRunner):

	def __init__(self, width=10, height=20):
		super().__init__(width, height)

	def delete_last_lines(self,n):
		CURSOR_UP_ONE = '\033[F' #'\x1b[1A'
		ERASE_LINE = '\033[K' #'\x1b[2K'
		for _ in range(n):
			sys.stdout.write(CURSOR_UP_ONE)
			sys.stdout.write(ERASE_LINE)

	def erase_board(self):
		self.delete_last_lines(self.height + 3)

	def display_board(self):
		data = self.game.get_board()
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
		super().play()

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

if __name__ == '__main__':
	runner = TerminalTetrisRunner()
	runner.play()
