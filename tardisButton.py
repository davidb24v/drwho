'''

Button for "Dr Who" themed sound & light box


'''


from __future__ import print_function
import RPi.GPIO as GPIO
import os
import time
import inspect
from glob import glob
from indicators import Indicators
import asyncore
import pyinotify

# watched events
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

FILETYPES = ['*.wav', '*.mp[1234]', '*.m4[ab]' ,'*.ogg', '*.flac', '*.oga', '*.aac']
PATTERNS = []
for ft in FILETYPES:
    PATTERNS.append(ft)
    PATTERNS.append(ft.upper())

class TardisButton(object):

    __number = 0

    def __init__(self, pin, player, latching=False, dir=None):
        self.pin = pin
        self.player = player
        GPIO.setup(pin, GPIO.IN)

        # enumerate this instance
        TardisButton.__number += 1
        self.__name = str(TardisButton.__number)

        # Grab a light
        self.light = Indicators()
        self.light.on()

        # which file to play next
        self.__next = 0

        # Where do we find our data files?
        if dir:
            self.__dir = dir
        else:
            dir = os.path.dirname(os.path.abspath(
                                  inspect.getfile(inspect.currentframe())))
            self.__dir = os.path.join(dir, 'Sounds', self.__name)

        # Scan for data files
        self._getFiles()

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

        # Switch off our light
        self.light.off()

        # Watch Manager
        self.wm = pyinotify.WatchManager()  

        class EventHandler(pyinotify.ProcessEvent):
            def process_IN_CREATE(self, event):
                print("Creating:", dir(event), event.pathname)

            def process_IN_DELETE(self, event):
                print("Removing:", event.pathname)

        self.notifier = pyinotify.AsyncNotifier(wm, EventHandler())
        self.wdd = wm.add_watch(self.__dir, mask, rec=True)


    # Look for files
    def _getFiles(self):
        result = []
        for pattern in PATTERNS:
            for f in glob(os.path.join(self.__dir, pattern)):
                result.append(f)
        self.__files = result
        self.__files.sort()

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
                self.light.on()
                self.player.play(
                    self.__name, self.__files[self.playing], self.__done)
                self.__next += 1
                if self.__next == len(self.__files):
                    self.__next = 0

    def test(self):
        self.__event()

    def __done(self):
        self.playing = -1
        self.light.off()
