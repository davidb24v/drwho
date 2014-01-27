'''

Dr Who Box: Blue Effects LED

'''

from __future__ import print_function
import RPi.GPIO as GPIO
import time
from multiprocessing import Process
import math

# Define PINS
LED = 18

# Use numbering based on P1 header
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(LED, GPIO.OUT, GPIO.LOW)


def pulsateLed():
    pwm = GPIO.PWM(LED, 100)
    pwm.start(0)
    values = [math.sin(x * math.pi / 180.0) for x in range(0, 181)]
    values = [int(100 * x ** 3) for x in values]
    increasing = True
    count = 0
    delay = 0.02
    pwm.start(0)

    while True:
        pwm.ChangeDutyCycle(values[count])

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
    p = Process(target=pulsateLed)
    p.start()
    while True:
        time.sleep(1)
        print(time.asctime(), 'and python is running!')
except:
    GPIO.cleanup()
    p.terminate()
