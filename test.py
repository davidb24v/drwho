from sonicRGB import SonicRGB
import time
import RPi.GPIO as GPIO
from pulsatingLED import PulsatingLED

# Define PINS
RED = 7
GREEN = 24
BLUE = 26

m = SonicRGB(red=7, green=24, blue=26,
             pwmFrequency=500, commonCathode=False,
             cutoffs=[50, 500, 2000, 15000])

r = PulsatingLED(19, brightness=50)
g = PulsatingLED(21, offset=45.0, brightness=50)
b = PulsatingLED(23, offset=90.0, brightness=50)

r.start()
g.start()
b.start()

while False:
    m.play('wav/450Hz.wav')
    m.play('wav/800Hz.wav')
    m.play('wav/2kHz.wav')
    break

#m.play('../sherrifFatman.mp3')
#time.sleep(5)

#m.play('../Runaway.mp3')
#time.sleep(1)

m.play('mp3/theme.mp3')
time.sleep(1)
m.play('mp3/tardis1.mp3')
time.sleep(1)

#m.play('mp3/spacenoise.mp3')
#time.sleep(1)
#m.play('mp3/tardis.mp3')
#time.sleep(1)
#m.play('mp3/scream.mp3')
#time.sleep(1)
#m.play('mp3/dalekchorus1a.mp3')
#time.sleep(1)

#m.play('../sherrifFatman.mp3')
#time.sleep(1)
#m.play('../Runaway.mp3')
#time.sleep(1)

r.stop()
g.stop()
b.stop()
GPIO.cleanup()
