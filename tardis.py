'''

Dr Who Sound and Light

'''

from __future__ import print_function
import RPi.GPIO as GPIO
import time
import subprocess
import os
from pyblinkm import BlinkM

# Use numbering based on P1 header
GPIO.setmode(GPIO.BOARD)

# Define PINS
STATUS_LED = [15, 16]

POWER_LED = 12

BUTTONS = [11, 13]

# Initialise pins
# LEDs
GPIO.setup(STATUS_LED[0], GPIO.OUT, GPIO.LOW)
GPIO.setup(STATUS_LED[1], GPIO.OUT, GPIO.LOW)
GPIO.setup(POWER_LED, GPIO.OUT)
# Buttons
for button in BUTTONS:
    GPIO.setup(button, GPIO.IN)

# PWM
POWER = GPIO.PWM(POWER_LED, 50.0)
POWER.start(100)

# Status LED handling
STATUS = 0


def showStatus():
    GPIO.output(STATUS_LED[0], STATUS)
    GPIO.output(STATUS_LED[1], 1 - STATUS)


def toggleStatus():
    global STATUS
    STATUS = 1 - STATUS
    showStatus()


def idle():
    global STATUS
    STATUS = 0
    showStatus()


def busy():
    global STATUS
    STATUS = 1
    showStatus()

# Callbacks for Buttons

def button(channel):
    global BUTTON_PRESSED
    if STATUS != 0:
        return
    index = BUTTONS.index(channel)
    play(index)

# Add events for buttons
# The software debounce option sucks, do it properly
GPIO.add_event_detect(BUTTONS[0], GPIO.RISING, callback=button)
GPIO.add_event_detect(BUTTONS[1], GPIO.RISING, callback=button)


# The MP3 files
MP3 = ['mp3/tardis.mp3', 'mp3/dalekchorus1a.mp3']

def play(index):
    busy()
    try:
        blinkm.reset
        blinkm.set_fade_speed(255)
        r = 255*index
        g = 0
        b = 255*(1-index)
        blinkm.fade_to(r, g, b)
        with open(os.devnull, 'w') as DEVNULL:
            subprocess.check_call(['omxplayer', MP3[index]],
                                  stdout=DEVNULL,
                                  stderr=DEVNULL)
        blinkm.reset()
        blinkm.set_fade_speed(2)
        blinkm.fade_to(0, 0, 0)
    except:
        pass
    idle()

# BlinkM
blinkm = BlinkM(bus=1, addr=6)

blinkm.reset()
blinkm.set_fade_speed(5)

blinkm.fade_to(0,0,255)

time.sleep(0.5)
blinkm.set_fade_speed(3)
blinkm.fade_to(0,0,0)

# Main "event loop" for testing
idle()
try:
    time.sleep(300)
except:
    pass
finally:
    # Release GPIO resources
    blinkm.reset()
    blinkm.fade_to(0,0,0)
    time.sleep(0.1)
    POWER.stop()
    GPIO.cleanup()
    print("\nOk")
