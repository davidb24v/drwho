'''

Dr Who Box: RGB LED

'''

from __future__ import print_function
import RPi.GPIO as GPIO
import time
import threading
import math

class PulsatingLED(object):
    '''
    Vary brightness of an LED using PWM to apply a sine squared
    waveform: sin((theta+offset)*k)**2
    '''

    def __init__(self, pin, delay=0.01, k=1.0, offset=0.0, pwmFreq=100):
        self.pin = pin
        self.delay = delay
        self.count = 0
        self.running = False

        # Use numbering based on P1 header
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT, GPIO.LOW)
        self.pwm = GPIO.PWM(self.pin, 100)
        self.pwm.start(0)

        # Setup our data
        self.values = [math.sin((x + offset) * k * math.pi / 180.0) for x in range(0, 181)]
        self.values = [int(100 * x ** 2) for x in self.values]

    def start(self):
        if self.running:
            return
        self.count = 0
        self.running = True
        self.thread = threading.Thread(target=self.__play)
        self.thread.start()

    def stop(self):
        self.running = False

    def __play(self):
        while self.running:
            self.pwm.ChangeDutyCycle(self.values[self.count])
            self.count += 1
            if self.count == len(self.values):
                self.count = 0
            time.sleep(self.delay)
        self.pwm.start(0)
        return 0


