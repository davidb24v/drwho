'''

Dr Who Box: Power LED

'''

import RPi.GPIO as GPIO
import time

# Define PINS
POWER_LED = 12

# Use numbering based on P1 header
GPIO.setmode(GPIO.BOARD)

GPIO.setup(POWER_LED, GPIO.OUT)

GPIO.output(POWER_LED, GPIO.HIGH)

# Wait forever...
try:
    while True:
        time.sleep(1)
except:
    GPIO.cleanup()
