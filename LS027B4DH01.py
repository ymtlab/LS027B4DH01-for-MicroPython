import utime

class LS027B4DH01():
    def __init__(self):
        self.scs = None
        self.extcomin = None
        self.disp = None
        self.spi = None
        self.data = bytearray( (1+1+50) * 241 + 2 )
        self.font = {}

        self.data_reset()

    def character(self, x, y, character):
        font_bytearray = self.font.get(character)
        
        if font_bytearray == None:
        	return
        
        for index, byte in enumerate(font_bytearray):
            byte_number = index % self.byte_length
            line_number = int(index / self.byte_length)
            x2 = int(x / 8) + byte_number
            y2 = (y + line_number) * 52
            data_index = 2 + y2 + x2
            self.data[data_index] = byte

    def clear_all(self):
        self.disp.off()
        self.scs.on()
        utime.sleep_us(3)
        self.spi.write(b'\x04\x00')
        utime.sleep_us(3)
        self.scs.off()
        utime.sleep_us(5)
        self.disp.on()

    def data_reset(self):
        for i in range(len(self.data)):
            self.data[i] = 0xFF
        self.data[0] = 0x01
        self.data[1] = 0x01
        for i in range(2, 241):
            self.data[i * 52 + 1] = i

    def dot(self, x, y):
        index = 2 + int(x / 8) + y * 52
        byte = ~self.data[index] | (1 << (x % 8))
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
                self.dot(x1, y + y1)
            return
        
        a = (y2 - y1) / (x2 - x1)

        if delta_x > delta_y:
            x_array = [ i for i in range(x1, x2)]
            y_array = [ int(a * x + y1) for x in x_array ]
        else:
            y_array = [ i for i in range(y1, y2)]
            x_array = [ int( (y - y1) / a ) for y in y_array ]

        for x, y in zip(x_array, y_array):
            self.dot(x, y)

    def set_one_byte(self, x, y, byte):
        self.data[2 + x + y * 52] = byte

    def string(self, x, y, string):
        for x2, character in enumerate(string):
            self.character(x + x2 * self.byte_length * 8, y, character)

    def update_all_line(self):
        self.scs.on()
        utime.sleep_us(4)
        self.spi.write(self.data)
        utime.sleep_us(4)
        self.scs.off()
        utime.sleep_us(4)

    def update_one_line(self, line, data_array):
        self.scs.on()
        self.spi.write(b'\x01') # send mode
        self.spi.write( bytearray([line]) ) # send gate line address
        self.spi.write(data_array) # send data
        self.spi.write(b'\x00\x00') # dummy data
        self.scs.off()
