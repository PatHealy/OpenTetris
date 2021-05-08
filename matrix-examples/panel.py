import smbus

class Panel:
    def __init__(self, i2c_bus, i2c_id):
        self.i2c_addr = i2c_id
        self.i2c_bus = i2c_bus

    def draw_pixel(self, coords, colors):
        self.i2c_bus.write_i2c_block_data(self.i2c_addr,
                                          0x0,
                                          [0xaf]+coords+colors)

    def fill_rect(self, start_coords, end_coords, colors):
        self.i2c_bus.write_i2c_block_data(self.i2c_addr,
                                          0x0,
                                          [0xad]+start_coords+end_coords+colors)

    def clear_screen(self):
        self.fill_screen([0,0,0])

    def fill_screen(self, colors):
        self.fill_rect([0,0], [32,32], colors)
