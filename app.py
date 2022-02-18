import sys

if __name__ == '__main__':
	if len(sys.argv) < 2:
		from runners.terminal.terminal_runner import TerminalTetrisRunner
		runner = TerminalTetrisRunner()
		runner.play()
	elif sys.argv[1] == "GUI":
		from runners.pygame.pygame_runner import PygameTetrisRunner
		runner = PygameTetrisRunner()
		runner.play()

