"""
Jouer un son mp3 quand on appuie sur un bouton en i2s
brancher un ampli i2s sur les roches GP0 GP1 et GP2
brancher un bouton sur broche GP15

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



led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True


keys = Keys((board.GP10, board.GP11, board.GP12, board.GP13), value_when_pressed=True, pull=True)


while True:
    event = keys.events.get()
    if event:
        print(event)
    led.value = not led.value
    time.sleep(0.02)


