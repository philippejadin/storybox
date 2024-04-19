# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
CircuitPython single MP3 playback example for Raspberry Pi Pico.
Plays a single MP3 once.
"""
import board
import audiomp3
import audiopwmio
import time
import digitalio
import audiobusio

#audio = audiopwmio.PWMAudioOut(board.GP0)
audio = audiobusio.I2SOut(board.GP20, board.GP21, board.GP22)

decoder = audiomp3.MP3Decoder(open("1.mp3", "rb"))

button = digitalio.DigitalInOut(board.GP15)
button.switch_to_input(pull=digitalio.Pull.DOWN)

button2 = digitalio.DigitalInOut(board.GP10)
button2.switch_to_input(pull=digitalio.Pull.DOWN)

time.sleep(5)


while True:
    if button.value:
        audio.play(decoder)
        # while audio.playing:
        #    pass
        time.sleep(0.1)
    if button2.value:
        audio.stop()
        #button.value = False

# Ecrit ton programme ici ;-)
