
"""
CircuitPython single MP3 playback example for Raspberry Pi Pico.
Plays a single MP3 once.
"""
import board
import busio
import audiomp3
import audiopwmio
import time
import digitalio
import sdcardio
import storage

import os


audio = audiopwmio.PWMAudioOut(board.GP0)

button = digitalio.DigitalInOut(board.GP15)
button.switch_to_input(pull=digitalio.Pull.DOWN)



# Use the board's primary SPI bus
# spi = board.SPI()
# Or, use an SPI bus on specific pins:
spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)

# For breakout boards, you can choose any GPIO pin that's convenient:
cs = board.GP13


sd = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sd)
storage.mount(vfs, "/sd")
os.listdir("/sd")


#decoder = audiomp3.MP3Decoder(open("/sd/01.mp3", "rb"))

decoder = audiomp3.MP3Decoder(open("/metronomy.mp3", "rb"))


def print_directory(path, tabs=0):
    for file in os.listdir(path):
        stats = os.stat(path + "/" + file)
        filesize = stats[6]
        isdir = stats[0] & 0x4000

        if filesize < 1000:
            sizestr = str(filesize) + " by"
        elif filesize < 1000000:
            sizestr = "%0.1f KB" % (filesize / 1000)
        else:
            sizestr = "%0.1f MB" % (filesize / 1000000)

        prettyprintname = ""
        for _ in range(tabs):
            prettyprintname += "   "
        prettyprintname += file
        if isdir:
            prettyprintname += "/"
        print('{0:<40} Size: {1:>10}'.format(prettyprintname, sizestr))

        # recursively print directory contents
        if isdir:
            print_directory(path + "/" + file, tabs + 1)


print("Fichiers sur la carte SD:")
print("====================")
print_directory("/sd")



print("Fichiers sur la pico:")
print("====================")
print_directory("")



while True:
    if button.value:
        audio.play(decoder)
        # while audio.playing:
        #    pass
        time.sleep(0.1)

