from sonicRGB import SonicRGB
import time
import RPi.GPIO as GPIO
from pulsatingLED import PulsatingLED
from tardisButton import TardisButton
import sys

# Define PINS
RED = 7
GREEN = 24
BLUE = 26

m = SonicRGB(red=7, green=24, blue=26,
             pwmFrequency=500, cutoffs=[50, 500, 2000, 15000])

b1 = TardisButton(11, m)
b2 = TardisButton(13, m)
b3 = TardisButton(12, m)
b4 = TardisButton(16, m)
b5 = TardisButton(18, m)

br = 100
w = PulsatingLED(15, brightness=br/4, delay=0.01)
r = PulsatingLED(19, offset=30.0, brightness=br, delay=0.025)
g = PulsatingLED(21, offset=60.0, brightness=br, delay=0.005)
b = PulsatingLED(23, offset=90.0, brightness=br, delay=0.01)

w.start()
r.start()
g.start()
b.start()

time.sleep(300)

w.stop()
r.stop()
g.stop()
b.stop()

GPIO.cleanup()

sys.exit()

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
