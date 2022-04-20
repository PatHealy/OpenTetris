import sys
sys.path.insert(0, '../')
sys.path.insert(0, '../core')
from runners.pygame.pygame_runner import PygameTetrisRunner

runner = PygameTetrisRunner(debug_mode=True)
runner.play()
