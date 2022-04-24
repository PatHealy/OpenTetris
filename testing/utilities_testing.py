import sys
sys.path.insert(0, '../')
sys.path.insert(0, '../core')
from runners.pygame_runner import PygameTetrisRunner
from core.utilities import *

# Test debug mode, which prints out most utilities
runner = PygameTetrisRunner(debug_mode=True)

# debug mode will print utility output on play
runner.play()


