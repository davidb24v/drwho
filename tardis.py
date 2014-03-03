from sonicRGB import SonicRGB
import time
import RPi.GPIO as GPIO
from pulsatingLED import PulsatingLED
from tardisButton import TardisButton
import sys
import asyncore

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
w = PulsatingLED(15, brightness=br, delay=0.01)
r = PulsatingLED(19, offset=30.0, brightness=br, delay=0.025)
g = PulsatingLED(21, offset=60.0, brightness=br, delay=0.005)
b = PulsatingLED(23, offset=90.0, brightness=br, delay=0.01)

w.start()
r.start()
g.start()
b.start()


try:
    asyncore.loop()

except:
    w.stop()
    r.stop()
    g.stop()
    b.stop()

    GPIO.cleanup()
