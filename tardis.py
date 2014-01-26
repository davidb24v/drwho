'''

Dr Who Sound and Light

'''

from __future__ import print_function
import RPi.GPIO as GPIO
import time
import subprocess
import os

# Use numbering based on P1 header
GPIO.setmode(GPIO.BOARD)

# Define PINS
STATUS_LED = [15, 16]

BUTTONS = [11, 13]

# Initialise pins
# LEDs
GPIO.setup(STATUS_LED[0], GPIO.OUT, GPIO.LOW)
GPIO.setup(STATUS_LED[1], GPIO.OUT, GPIO.LOW)
# Buttons
for button in BUTTONS:
    GPIO.setup(button, GPIO.IN)

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
        with open(os.devnull, 'w') as DEVNULL:
            subprocess.check_call(['omxplayer', MP3[index]],
                                  stdout=DEVNULL,
                                  stderr=DEVNULL)
    except:
        pass
    idle()

# Main "event loop" for testing
idle()
try:
    time.sleep(300)
except:
    pass
finally:
    # Release GPIO resources
    time.sleep(0.1)
    GPIO.cleanup()
    print("\nOk")
