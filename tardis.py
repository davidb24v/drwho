from sonicRGB import SonicRGB
import time
import RPi.GPIO as GPIO
from pulsatingLED import PulsatingLED
from tardisButton import TardisButton
from indicators import Indicators
import subprocess
import sys

# Pump up da volume...
subprocess.call(["amixer", "set", "PCM", "100%"])

# RGB display and music player
m = SonicRGB(red=7, green=24, blue=26,
             pwmFrequency=500, cutoffs=[50, 500, 2000, 15000])

# The 5 music selection buttons
b1 = TardisButton(11, m)
b2 = TardisButton(13, m)
b3 = TardisButton(12, m)
b4 = TardisButton(16, m)
b5 = TardisButton(18, m)


# The 10mm LEDs: White, Red, Green, Blue
br = 100
w = PulsatingLED(15, offset=0.0, brightness=br, delay=0.01)
r = PulsatingLED(19, offset=30.0, brightness=br, delay=0.01)
g = PulsatingLED(21, offset=60.0, brightness=br, delay=0.01)
b = PulsatingLED(23, offset=90.0, brightness=br, delay=0.01)

# Monitor the shutdown button
# Define PINS
SHUTDOWN_BUTTON = 22
SHUTDOWN_IN_PROGRESS = False
GPIO.setmode(GPIO.BOARD)
GPIO.setup(SHUTDOWN_BUTTON, GPIO.IN)

def shutdown(channel):
    global SHUTDOWN_IN_PROGRESS
    global m
    if SHUTDOWN_IN_PROGRESS:
        return

    SHUTDOWN_IN_PROGRESS = True

    # Kill the music and set RGB panels to red
    m.stop()
    m.redAlert()

    # Turn off indicators (since they won't go off later)
    Indicators.allOff()

    # Turn on all 10mm LEDs
    w.on()
    r.on()
    g.on()
    b.on()

    subprocess.call(["/sbin/shutdown", "-h", "now"])

# Add an event for the shutdown button
GPIO.add_event_detect(SHUTDOWN_BUTTON, GPIO.RISING, callback=shutdown)

# Start the pulsating effect
w.start()
r.start()
g.start()
b.start()

# All activity is event driven...
try:
    while True:
        time.sleep(1)

except:
    # Stop pulsating
    w.stop()
    r.stop()
    g.stop()
    b.stop()

    # Stop the music
    m.stop()

    # Attempt to clean up
    GPIO.cleanup()
