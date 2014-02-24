'''

Button for "Dr Who" themed sound & light box


'''


from __future__ import print_function
import RPi.GPIO as GPIO
import os
import inspect
from glob import glob

GPIO.setmode(GPIO.BOARD)

class TardisButton(object):
    
    __number = 0

    def __init__(self, pin, player, latching=False, dir=None):
        self.pin = pin
        self.player = player
        GPIO.setup(pin, GPIO.IN)

        # enumerate this instance
        TardisButton.__number += 1
        self.__name = str(TardisButton.__number)

        # which file to play next
        self.__next = 0

        # Where do we find our data files?
        if dir:
            self.__dir = dir
        else:
            dir = os.path.dirname(os.path.abspath(
                                  inspect.getfile(inspect.currentframe())))
            self.__dir = os.path.join(dir, 'Sounds', self.__name)

        # Look for files
        files = []
        def getFiles(dir, patterns):
            result = []
            for pattern in patterns:
                for f in glob(os.path.join(dir, pattern)):
                    result.append(f)
            return result

        # Look for wav and mp3 files, allow for a certain crap OS to cock about with case
        self.__files = getFiles(self.__dir, ['*.wav', '*.mp3', '*.WAV', '*.MP3'])
        self.__files.sort()

        # are we active
        self.enable()

        # Add a callback
        if latching:
            type = GPIO.BOTH
        else:
            type = GPIO.RISING
        GPIO.add_event_detect(pin, type, callback=self.__event)

        # which track are we playing
        self.playing = -1

    def enable(self):
        self.__active = len(self.__files) > 0

    def disable(self):
        self.__active = False

    def __event(self, channel):
        if not self.__active:
            return
        if self.playing >= 0:
            self.player.restart()
        else:
            if not self.player.busy(self.__name):
                self.playing = self.__next
                self.player.play(self.__name, self.__files[self.playing], self.__done)
                self.__next += 1
                if self.__next == len(self.__files):
                    self.__next = 0

    def test(self):
        self.__event()

    def __done(self):
        self.playing = -1

