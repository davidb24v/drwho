rr'''

Dr Who Box: Power LED

'''

import RPi.GPIO as GPIO
import subprocess
import time

# Define PINS
SHUTDOWN_BUTTON = 22

# Use numbering based on P1 header
GPIO.setmode(GPIO.BOARD)

GPIO.setup(SHUTDOWN_BUTTON, GPIO.IN)

# Flag to indicate that shutdown is in progress
SHUTDOWN_IN_PROGRESS = False

def button(channel):
    global SHUTDOWN_IN_PROGRESS
    if SHUTDOWN_IN_PROGRESS:
        return
    SHUTDOWN_IN_PROGRESS = True
    subprocess.call(["/sbin/shutdown", "-h", "now"])

# Add events for buttons
# The software debounce option sucks, do it properly
GPIO.add_event_detect(SHUTDOWN_BUTTON, GPIO.RISING, callback=button)


# Wait forever...
try:
    while True:
        time.sleep(1)
except:
    GPIO.cleanup()
