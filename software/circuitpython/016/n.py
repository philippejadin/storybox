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


# version pwm :
#audio = PWMAudioOut(board.GP18)

# version i2s :
audio = audiobusio.I2SOut(board.GP20, board.GP21, board.GP22)


mixer = audiomixer.Mixer(voice_count=1, sample_rate=44100, channel_count=1,
bits_per_sample=16, samples_signed=True, buffer_size=16384)

audio.play(mixer)
mixer.voice[0].level = 0.3

led.value = True

keys = Keys((board.GP10, board.GP11, board.GP12, board.GP13), value_when_pressed=True, pull=True)


LEFT_EVENT = Event(0, True)
RIGHT_EVENT = Event(1, True)
PLAY_EVENT = Event(2, True)
HOME_EVENT = Event(3, True)



def play(filename):
    global wavdecoder
    global mp3decoder
    try:
        if (os.stat(filename)):
            print("Playing " + filename)
    except OSError:
        print("file not found")

    memory()
    if filename[-3:] == "mp3":
        decoder = audiomp3.MP3Decoder(open("1.mp3", "rb"))
        mixer.voice[0].play(decoder)
        while mixer.voice[0].playing:
            pass
        decoder.deinit()
    elif filename[-3:] == "wav":
        print ("wav file")
        decoder = audiocore.WaveFile(open("/sd/intro.wav", "rb"))
        mixer.voice[0].play(decoder)
        while mixer.voice[0].playing:
            pass
        decoder.deinit()
    else:
        print ("file must end in .mp3 or .wav")
    print("finished playing")
    memory()



def stop():
    mixer.voice[0].stop()



def memory():
    #print( "Available memory before GC: {} bytes".format(gc.mem_free()) )
    gc.collect()
    print( "Available memory after GC: {} bytes".format(gc.mem_free()) )


# play start sound
play("/sd/intro.wav")



while True:
    event = keys.events.get()
    # event will be None if nothing has happened.
    if event == PLAY_EVENT:
        play("/sd/chaperon_rouge/menu.wav")
    if event == HOME_EVENT:
        play("/sd/chaperon_rouge/story.mp3")
    if event == LEFT_EVENT:
        play("/sd/mille_et_une_nuits/story.mp3")


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


