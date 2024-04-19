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
import audiomp3

audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2)
mp3 = open("01.mp3", "rb")
sound = audiomp3.MP3Decoder(mp3)


print("Playing wav file!")
audio.play(sound)
while audio.playing:
    pass
print("Done!")

