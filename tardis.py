from sonicRGB import SonicRGB
import time
import RPi.GPIO as GPIO
from pulsatingLED import PulsatingLED
from tardisButton import TardisButton
from indicators import Indicators
from volume import Volume
import subprocess
import sys
import os
import glob
import inspect
import inotifyx

# Setup a watch
fd = inotifyx.init()

# Where are we?
dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# Initial volume (from file if exists, else 80)
vol = Volume(dir)

# RGB display and music player
m = SonicRGB(red=7, green=24, blue=26,
             pwmFrequency=500, cutoffs=[50, 500, 2000, 15000])

# The 5 music selection buttons
b1 = TardisButton(11, m)
b2 = TardisButton(13, m)
b3 = TardisButton(12, m)
b4 = TardisButton(16, m)
b5 = TardisButton(18, m)

# Setup some watches...
# Sound files
mask = inotifyx.IN_CLOSE_WRITE | inotifyx.IN_CREATE | \
       inotifyx.IN_DELETE | inotifyx.IN_MODIFY | inotifyx.IN_MOVE | \
       inotifyx.IN_MOVED_TO

for b in range(1,6):
    inotifyx.add_watch(fd, os.path.join(dir, "Sounds", str(b)), mask)

# Volume
inotifyx.add_watch(fd, os.path.join(dir, "Sounds", "Volume", "Level.txt"),  mask)


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

# Create a list to hold the objects that respond to file events
evList = []
evList.append(None)
evList += [b1, b2, b3, b4, b5]
evList.append(vol)

# All activity is event driven, watch for file
# system changes
lastch = None
try:
    while True:
        events = inotifyx.get_events(fd, 0.1)
        for event in events:
            ev = str(event)
            ch = ev[0]
            if lastch:
                if ch != lastch:
                    evList[int(lastch)].fileEvent()
                    lastch = ch
            else:
                lastch = ch
        if not events:
            if lastch:
                evList[int(lastch)].fileEvent()
                lastch = None


except Exception, e:
    # Stop pulsating
    w.stop()
    r.stop()
    g.stop()
    b.stop()

    # Stop the music
    m.stop()

    # Attempt to clean up
    GPIO.cleanup()
