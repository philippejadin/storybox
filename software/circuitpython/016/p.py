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


led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

# version pwm :
#audio = PWMAudioOut(board.GP18)

# version i2s :
audio = audiobusio.I2SOut(board.GP20, board.GP21, board.GP22)
keys = Keys((board.GP10, board.GP11, board.GP12, board.GP13), value_when_pressed=True, pull=True)


LEFT_EVENT = Event(0, True)
RIGHT_EVENT = Event(1, True)
PLAY_EVENT = Event(2, True)
HOME_EVENT = Event(3, True)

mixer = audiomixer.Mixer(voice_count=1, sample_rate=22050, channel_count=1, bits_per_sample=16, samples_signed=True)
mixer.voice[0].level = 0.3


decoder = audiomp3.MP3Decoder(open("/sd/intro.mp3", "rb"))



def play(filename):
    print("playing " + filename)
    if audio.playing:
        audio.stop()
    decoder.file = open(filename, "rb")
    audio.play(decoder)
    #while audio.playing:
    #    pass
    #decoder.deinit()
    time.sleep(2)
    memory()



def memory():
    gc.collect()
    print( "Available memory after GC: {} bytes".format(gc.mem_free()) )


# play start sound
play("/sd/intro.mp3")



while True:
    event = keys.events.get()
    # event will be None if nothing has happened.
    if event == PLAY_EVENT:
        play("/sd/chaperon_rouge/menu.mp3")
    if event == HOME_EVENT:
        play("/sd/chaperon_rouge/story.mp3")
    if event == LEFT_EVENT:
        play("/sd/mille_et_une_nuits/story.mp3")
    if event == RIGHT_EVENT:
        play("/sd/hurtme.mp3")


    led.value = not led.value
    time.sleep(0.2)


while True:
    #story.led.value = not story.led.value
    time.sleep(0.02)


while True:
    event = keys.events.get()
    # event will be None if nothing has happened
    if event == PLAY_EVENT:
        mixer.voice[0].play(audio_file)
    if event == HOME_EVENT:
        mixer.voice[0].stop()
    led.value = not led.value
    time.sleep(0.02)


