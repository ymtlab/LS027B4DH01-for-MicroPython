import utime
from machine import Pin, SPI
from LS027B4DH01 import LS027B4DH01
from font_16 import font_16

class Font():
    def __init__(self):
        self.byte_length = 2
        self.font = font_16

    def get(self, character):
        return self.font.get(character)

def main():
    
    # LCD
    lcd = LS027B4DH01()
    lcd.spi = SPI(
        2, #vspi = id = 2
        baudrate=2_000_000, #1MHz
        polarity=0, phase=0, bits=8, firstbit=SPI.LSB,
        sck=Pin(18), mosi=Pin(23), miso=Pin(19)
    )
    lcd.scs      = Pin(32, Pin.OUT)
    lcd.extcomin = Pin(33, Pin.OUT)
    lcd.disp     = Pin(25, Pin.OUT)
    lcd.initialize()
    lcd.disp.on()
    lcd.font = Font()

    lcd.string(50, 50, 'hello world')
    lcd.data_update_all_line()
    utime.sleep(1)

    while True:
        
        # update one line test
        for i in range(5):
            lcd.data_update_one_line(120, [0x00] * 50)
            utime.sleep_ms(200)

            lcd.data_update_one_line(120, [0xFF] * 50)
            utime.sleep_ms(200)

        # update multi line test
        for i in range(5):
            lcd.data_update_multi_line(160, [ [0x00] * 50 for i in range(5) ])
            utime.sleep_ms(200)
            lcd.data_update_multi_line(160, [ [0xFF] * 50 for i in range(5) ])
            utime.sleep_ms(200)

        # draw line test 1
        for i in range(5):
            lcd.data_reset()
            lcd.data_update_all_line()
            utime.sleep_ms(200)

            lcd.line(   0,   0,   0, 239)
            lcd.line( 399,   0, 399, 239)
            lcd.line(   0,   0, 399,   0)
            lcd.line(   0, 239, 399, 239)
            
            lcd.line(  80,  40,  80, 180)
            lcd.line( 300,  40, 300, 180)
            lcd.line(  80,  40, 300,  40)
            lcd.line(  80, 180, 300, 180)
            
            lcd.data_update_all_line()
            utime.sleep_ms(200)

        # draw line test 2
        for i in range(5):
            lcd.data_reset()
            lcd.data_update_all_line()
            utime.sleep_ms(200)

            lcd.line(   0,   0, 399, 239)
            lcd.line(   0, 239, 399,   0)
            
            lcd.line(   0,   0, 199, 239)
            lcd.line( 200, 239, 399,   0)

            lcd.data_update_all_line()
            utime.sleep_ms(200)
            
        # draw line test 3
        lcd.string(50, 50, 'hello world')
        lcd.data_update_all_line()
        for i in range(240):
            lcd.data_update_one_line(i, [0x00] * 50)
        for i in range(240):
            lcd.data_update_one_line(i, [0xFF] * 50)

if __name__ == "__main__":
    main()
