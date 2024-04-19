
"""
Jouer un son wav quand on appuie sur un bouton en PWM sur la broche GP18
brancher un casque sur GND et broche GP18
brancher un bouton sur broche
"""

import audiocore
import board
import audiobusio
from audiopwmio import PWMAudioOut
import digitalio

# version pwm :
audio = PWMAudioOut(board.GP18)

wave_file = open("StreetChicken.wav", "rb")
wav = audiocore.WaveFile(wave_file)


button = digitalio.DigitalInOut(board.GP15)
button.switch_to_input(pull=digitalio.Pull.DOWN)

print("Appuyez sur le bouton pour écouter le son")

while True:
    if button.value:
        print("Lecture du fichier audio")
        audio.play(wav)
        while audio.playing:
            pass
        print("C'est fait!")

