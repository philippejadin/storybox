"""
Jouer un son mp3 quand on appuie sur un bouton en i2s
brancher un ampli i2s sur les roches GP0 GP1 et GP2
brancher un bouton sur broche GP15

"""



import time
import story



# play start sound
story.play("/sd/intro.wav")



while True:
    event = story.keys.events.get()
    # event will be None if nothing has happened.
    if event == story.PLAY_EVENT:
        story.play("/sd/intro.wav")
    if event == story.HOME_EVENT:
        story.stop()
    story.led.value = not story.led.value
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


