import digitalio
import board
import time


button = digitalio.DigitalInOut(board.GP15)
button.switch_to_input(pull=digitalio.Pull.DOWN)

while True :
    if button.value:
        print("Button HIGH")
    else:
        print("Button LOW")
    time.sleep(0.1)
