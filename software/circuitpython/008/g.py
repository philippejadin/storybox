"""
Jouer un son mp3 quand on appuie sur un bouton en i2s
brancher un ampli i2s sur les roches GP0 GP1 et GP2
brancher un bouton sur broche GP15
"""

import audiocore
import board
import audiobusio
import busio
from audiopwmio import PWMAudioOut
import digitalio
import audiomp3
import audiomixer
import sdcardio
import storage
import os


# Use the board's primary SPI bus
# spi = board.SPI()
# Or, use an SPI bus on specific pins:
spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
# For breakout boards, you can choose any GPIO pin that's convenient:
cs = board.GP13
sd = sdcardio.SDCard(spi, cs)
vfs = storage.VfsFat(sd)
storage.mount(vfs, "/sd")
print(os.listdir("/sd"))



# version pwm :
#audio = PWMAudioOut(board.GP18)

# version i2s :
audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2)

# version mp3 :
audio_file = audiomp3.MP3Decoder(open("/sd/long.mp3", "rb"))

# version wav :
#audio_file = audiocore.WaveFile(open("/sd/long.wav", "rb"))


mixer = audiomixer.Mixer(voice_count=1, sample_rate=22050, channel_count=1,
bits_per_sample=16, samples_signed=True)

audio.play(mixer)
mixer.voice[0].level = 0.5




button = digitalio.DigitalInOut(board.GP16)
button.switch_to_input(pull=digitalio.Pull.DOWN)


print("-----------------------------------------")
print("Appuyez sur le bouton pour écouter le son")

while True:
    if button.value:
        print("Lecture du fichier audio")
        #audio.play(audio_file)
        mixer.voice[0].play(audio_file);
        #while audio.playing:
        #    pass
        #print("C'est fait!")


