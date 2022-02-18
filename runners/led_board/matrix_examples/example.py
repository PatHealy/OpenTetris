import smbus
import time

from panel import Panel

bus = smbus.SMBus(1)
ADDR = 0x04

WHITE_PIXEL = [0x1, 0x1, 0x1]
BLACK_PIXEL = [0x0, 0x0, 0x0]

panel = Panel(bus, ADDR)

panel.fill_rect([0,0], [32,32], WHITE_PIXEL)

'''
for x in range(32):
    for y in range(32):
        panel.draw_pixel([x,y], BLACK_PIXEL)
'''
