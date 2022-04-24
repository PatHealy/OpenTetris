from runners import PygameTetrisRunner, MultiplayerRunner, TerminalTetrisRunner
from single_player import SingleTrainer
import sys

if __name__ == '__main__':
	if len(sys.argv) < 2:
		runner = PygameTetrisRunner()
		runner.play()
	elif sys.argv[1] == "multiplayer":
		runner = MultiplayerRunner()
		runner.play()
	elif sys.argv[1] == "terminal":
		runner = TerminalTetrisRunner()
		runner.play()
	elif sys.argv[1] == "trainP1":
		trainer = SingleTrainer()
		trainer.train()
