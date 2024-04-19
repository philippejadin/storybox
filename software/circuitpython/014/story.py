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



# Init SD CARD
spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
cs = board.GP13
sd = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sd)
storage.mount(vfs, "/sd")
print(os.listdir("/sd"))


led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


# version pwm :
#audio = PWMAudioOut(board.GP18)

# version i2s :
audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2)


mixer = audiomixer.Mixer(voice_count=1, sample_rate=22050, channel_count=1,
bits_per_sample=16, samples_signed=True, buffer_size=4096)

audio.play(mixer)
mixer.voice[0].level = 0.6

led.value = True

keys = Keys((board.GP16, board.GP17, board.GP18, board.GP19), value_when_pressed=True, pull=True)


LEFT_EVENT = Event(0, True)  # Button 0 (GP16) pressed
RIGHT_EVENT = Event(1, True)  # Button 1 (GP17) pressed
PLAY_EVENT = Event(2, True)  # Button 2 (GP18) pressed
HOME_EVENT = Event(3, True)  # Button 2 (GP19) pressed


def play(filename):
    if filename[-3:] == "mp3": 
        print ("mp3 file")
        audio_file = audiomp3.MP3Decoder(open(filename, "rb"))
    elif filename[-3:] == "wav":
        print ("wav file")
        audio_file = audiocore.WaveFile(open(filename, "rb"))
    else:
        print ("file must end in .mp3 or .wav")

    try:
        if (os.stat(filename)):
            print("Playing " + filename)
            mixer.voice[0].play(audio_file)
    except OSError:
        print("file not found")


def stop():
    mixer.voice[0].stop()