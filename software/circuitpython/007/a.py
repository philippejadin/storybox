
"""
Jouer un son wav à l'allumage en PWM sur la broche GP18
brancher un casque sur GND et broche GP18
"""

import audiocore
import board
import audiobusio
from audiopwmio import PWMAudioOut

# version pwm :
# audio = PWMAudioOut(board.GP18)

# version i2s
audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2)

wave_file = open("StreetChicken.wav", "rb")
wav = audiocore.WaveFile(wave_file)

print("Lecture du fichier audio")
audio.play(wav)
while audio.playing:
    pass
print("Fait!")

