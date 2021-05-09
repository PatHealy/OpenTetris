#!/usr/bin/env python
from samplebase import SampleBase

class TetrisGrid(SampleBase):
    def __init__(self, *args, **kwargs):
        super(TetrisGrid, self).__init__(*args, **kwargs)

    def run(self):
        offset_canvas = self.matrix.CreateFrameCanvas()
        while True:
            grid = []
            for x in range(16):
                row = []
                for y in range(16):
                    if x%2 == y%2:
                        row.append((0,0,0))
                    else:
                        row.append((255,255,255))
                grid.append(row)

            for x in range(self.matrix.width):
                for y in range(self.matrix.height):
                    c = grid[(int(x))/4][(int(y))/4]
                    offset_canvas.SetPixel(x, x, 255, 255, 255)
            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)


# Main function
if __name__ == "__main__":
    tetris_grid = TetrisGrid()
    if (not tetris_grid.process()):
        tetris_grid.print_help()
