# LS027B4DH01 library for MicroPython on the ESP32

## Function
* draw one line
* draw multi line
* draw dot
* draw 2 point line
* draw character
* draw string
* display clear

## how to use

### init
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

### draw one line
lcd.data_update_one_line(120, [0x00] * 50)

### draw multi line
lcd.data_update_multi_line(160, [ [0x00] * 50 for i in range(5) ])

### draw dot
lcd.data_reset()
lcd.dot(100, 100)
lcd.data_update_all_line()

### draw 2 point line
lcd.data_reset()
lcd.line(   0,   0,   0, 239)
lcd.data_update_all_line()

### draw character
lcd.character(10, 50, ')

### draw string
lcd.string(50, 50, 'hello world')

### display clear
lcd.clear_all()
