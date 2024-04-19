# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
CircuitPython I2S WAV file playback.
Plays a WAV file once.
"""
import audiocore
import board
import audiobusio
from audiopwmio import PWMAudioOut

# version i2s :
# audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2)

# version pwm :
audio = PWMAudioOut(board.GP18)

from audiopwmio import PWMAudioOut as AudioOut

wave_file = open("StreetChicken.wav", "rb")
wav = audiocore.WaveFile(wave_file)

print("Playing wav file!")
audio.play(wav)
while audio.playing:
    pass
print("Done!")

