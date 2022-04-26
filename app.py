from runners import PygameTetrisRunner, MultiplayerRunner, TerminalTetrisRunner, VsAIRunner
from single_player import SingleTrainer, SingleTester
from multiplayer import MultiplayerTrainer
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
	elif sys.argv[1] == "testP1":
		tester = SingleTester()
		tester.play()
	elif sys.argv[1] == "vsAI":
		runner = VsAIRunner()
		runner.play()
	elif sys.argv[1] == "train2P":
		trainer = MultiplayerTrainer()
		trainer.train()
