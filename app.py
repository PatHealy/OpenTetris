from runners import PygameTetrisRunner, MultiplayerRunner, VsAIRunner, VsMPAIRunner
from single_player import SingleTrainer, SingleTester
from multiplayer import MultiplayerTrainer, MultiplayerTester
from led_board import LEDTrainer, LEDTester
import sys

if __name__ == '__main__':
	cell_size = 50
	if len(sys.argv) > 2:
		cell_size = int(sys.argv[2])

	if len(sys.argv) < 2:
		runner = PygameTetrisRunner()
		runner.play()
	elif sys.argv[1] == "play":
		runner = PygameTetrisRunner(cell_size=cell_size)
		runner.play()
	elif sys.argv[1] == "multiplayer":
		runner = MultiplayerRunner(cell_size=cell_size)
		runner.play()
	elif sys.argv[1] == "terminal":
		# from runners import TerminalTetrisRunner
		runner = TerminalTetrisRunner()
		runner.play()
	elif sys.argv[1] == "trainP1":
		trainer = SingleTrainer(cell_size=cell_size)
		trainer.train()
	elif sys.argv[1] == "testP1":
		tester = SingleTester(cell_size=cell_size)
		tester.play()
	elif sys.argv[1] == "testP1Stats":
		tester = SingleTester(cell_size=cell_size)
		tester.test()
	elif sys.argv[1] == "vsAI":
		runner = VsAIRunner(cell_size=cell_size)
		runner.play()
	elif sys.argv[1] == "vsMPAI":
		runner = VsMPAIRunner(cell_size=cell_size)
		runner.play()
	elif sys.argv[1] == "train2P":
		trainer = MultiplayerTrainer(cell_size=cell_size)
		trainer.train()
	elif sys.argv[1] == "test2P":
		tester = MultiplayerTester(cell_size=cell_size)
		tester.test()
	elif sys.argv[1] == "test2PStats":
		tester = MultiplayerTester(cell_size=cell_size)
		tester.test_stats()
	elif sys.argv[1] == "trainLEDboard":
		trainer = LEDTrainer(width=16, height=16)
		trainer.train()
	elif sys.argv[1] == "testLEDboard":
		tester = LEDTester(width=16, height=16)
		tester.play()
