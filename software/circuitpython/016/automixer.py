"""
"""

import audiocore
import board
import audiobusio
import busio
import digitalio
import audiomp3
import audiomixer
import sdcardio
import storage
import os
import time
from keypad import Keys, Event
import gc



# Init SD CARD
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)
cs = board.GP17
sd = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sd)
storage.mount(vfs, "/sd")
print(os.listdir("/sd"))


audio = audiobusio.I2SOut(board.GP20, board.GP21, board.GP22)

filename = "/sd/chaperon_rouge/story.mp3"
filename = "/sd/mille_et_une_nuits/story.mp3"
filename = "/sd/hurtmemono64.mp3"


decoder = audiomp3.MP3Decoder(open(filename, "rb"))
print (decoder.sample_rate)
print (decoder.channel_count)
print (decoder.bits_per_sample)

#while 1:
#    pass

mixer = audiomixer.Mixer(voice_count=1,
        sample_rate=decoder.sample_rate,
        channel_count=decoder.channel_count,
        bits_per_sample=decoder.bits_per_sample,
        samples_signed=True)
audio.play(mixer)
mixer.voice[0].play(decoder)
mixer.voice[0].level = 0.3

while mixer.voice[0].playing:
    pass
