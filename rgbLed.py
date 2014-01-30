'''

Dr Who Box: RGB Effects LED

'''

from __future__ import print_function
import RPi.GPIO as GPIO
import time
from multiprocessing import Process
import math

# Define PINS
RED = 7
GREEN = 8
BLUE = 10

# Use numbering based on P1 header
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(RED, GPIO.OUT, GPIO.HIGH)
GPIO.setup(GREEN, GPIO.OUT, GPIO.HIGH)
GPIO.setup(BLUE, GPIO.OUT, GPIO.HIGH)


def rgbLed():
    red = GPIO.PWM(RED, 100)
    green = GPIO.PWM(GREEN, 100)
    blue = GPIO.PWM(BLUE, 100)

    red.start(100)
    green.start(100)
    blue.start(100)

    values = [math.sin(x * math.pi / 180.0) for x in range(0, 181)]
    values = [100-int(100 * x ** 3) for x in values]

    rValues = values
    gValues = values[45:] + values[0:45]
    bValues = values[135:] + values[0:135]

    increasing = True
    count = 0
    delay = 0.02

    while True:
        red.ChangeDutyCycle(rValues[count])
        green.ChangeDutyCycle(gValues[count])
        blue.ChangeDutyCycle(bValues[count])

        if increasing:
            count += 1
        else:
            count -= 1

        if (count >= len(values) - 1):
            increasing = False
        elif (count <= 0):
            increasing = True

        time.sleep(delay)


# Loop forever...
try:
    p = Process(target=rgbLed)
    p.start()
    while True:
        time.sleep(1)
        print(time.asctime(), 'and python is running!')
except:
    GPIO.cleanup()
    p.terminate()
