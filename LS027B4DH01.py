import utime
from micropython import const

class LS027B4DH01():
    tsSCS = const(3)
    thSCS = const(1)
    twSCSL = const(1)

    def __init__(self):
        self.scs = None
        self.extcomin = None
        self.disp = None
        self.spi = None
        self.data = bytearray(12482)
        self.font = None

        self.data_reset()

    def character(self, x, y, character):
        if self.font is None:
        	return
        
        font_bytearray = self.font.get(character)
        
        for index, byte in enumerate(font_bytearray):
            byte_number = index % self.font.byte_length
            line_number = int(index / self.font.byte_length)
            x2 = int(x / 8) + byte_number
            y2 = (y + line_number) * 52
            data_index = 2 + y2 + x2
            self.data[data_index] = byte

    def clear_all(self):
        self.disp.off()
        self.scs.on()
        utime.sleep_us(self.tsSCS)
        self.spi.write(b'\x04\x00')
        utime.sleep_us(self.thSCS)
        self.scs.off()
        utime.sleep_us(self.twSCSL)
        self.disp.on()

    def data_reset(self):
        self.data[0] = 0x01
        for y in range(240):
            y2 = y * 52
            self.data[y2 + 1] = y + 1
            for x in range(50):
                self.data[2 + y2 + x] = 0xFF

    def data_update_all_line(self):
        self.scs.on()
        utime.sleep_us(self.tsSCS)
        self.spi.write(self.data)
        utime.sleep_us(self.thSCS)
        self.scs.off()
        utime.sleep_us(self.twSCSL)

    def data_update_multi_line(self, line, array_2d):
        buffer = bytearray(len(array_2d) * 52 + 2)
        buffer[0] = 1
        buffer[1] = line
        
        for y, row in enumerate(array_2d):
            y2 = y * 52
            buffer[y2 + 1] = line + y
            for x, data in enumerate(row):
                buffer[2 + y2 + x] = data
        
        self.scs.on()
        utime.sleep_us(self.tsSCS)
        self.spi.write(buffer)
        utime.sleep_us(self.thSCS)
        self.scs.off()
        utime.sleep_us(self.twSCSL)

    def data_update_one_line(self, line, array_50byte):
        buffer = bytearray(54)
        buffer[0] = 1
        buffer[1] = line
        for i, data in enumerate(array_50byte):
            buffer[i+2] = data
        self.scs.on()
        utime.sleep_us(self.tsSCS)
        self.spi.write(buffer)
        utime.sleep_us(self.thSCS)
        self.scs.off()
        utime.sleep_us(self.twSCSL)

    def display_mode(self):
        self.scs.on()
        utime.sleep_us(self.tsSCS)
        self.spi.write(b'\x00\x00')
        utime.sleep_us(self.thSCS)
        self.scs.off()
        utime.sleep_us(self.twSCSL)

    def dot(self, x, y):
        index = 2 + int(x / 8) + y * 52
        byte = ~self.data[index] | ( 1 << (x % 8) )
        byte = ~byte
        self.data[index] = byte

    def initialize(self):
        self.disp.off()
        utime.sleep_us(500)
        self.scs.off()
        self.clear_all()
        utime.sleep_ms(5)
        self.disp.on()
        
    def line(self, x1, y1, x2, y2):

        delta_x = abs(x2 - x1)
        delta_y = abs(y2 - y1)

        if delta_x == 0:
            for y in range(delta_y):
                self.dot(x1, y1 + y)
            return
        
        if delta_y == 0:
            for x in range(delta_x):
                self.dot(x1 + x, y1)
            return
        
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1

        if delta_x > delta_y:
            x3 = x1
            if x3 > x2:
                x3 = x2
            x_array = [ x3 + x for x in range(delta_x) ]
            y_array = [ int(a * x + b) for x in x_array ]
        else:
            y3 = y1
            if y3 > y2:
                y3 = y2
            y_array = [ y3 + y for y in range(delta_y) ]
            x_array = [ int((y - b) / a) for y in y_array ]

        for x, y in zip(x_array, y_array):
            self.dot(x, y)

    def set_one_byte(self, byte_x, byte_y, byte):
        self.data[2 + byte_x + byte_y * 52] = byte

    def string(self, x, y, string):
        for x2, character in enumerate(string):
            self.character(x + x2 * self.font.byte_length * 8, y, character)
