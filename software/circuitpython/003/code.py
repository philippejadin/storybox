import board
import busio
import sdcardio
import storage
import os


# Use the board's primary SPI bus
#spi = board.SPI()
# Or, use an SPI bus on specific pins:
spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)

# For breakout boards, you can choose any GPIO pin that's convenient:
cs = board.GP13


sd = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sd)
storage.mount(vfs, "/sd")
os.listdir("/sd")

with open("/sd/test.txt", "w") as f:
    f.write("Hello world!\r\n")

