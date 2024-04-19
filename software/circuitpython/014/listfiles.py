import sdcardio
import storage
import os
import time
import busio
import board

# Init SD CARD
spi = busio.SPI(board.GP6, MOSI=board.GP7, MISO=board.GP4)
cs = board.GP5
sd = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sd)
storage.mount(vfs, "/sd")
print(os.listdir("/sd"))
