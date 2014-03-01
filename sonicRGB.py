'''

Sonic RGB LED for "Dr Who" themed sound & light box

Based on a very cut down version of :

    # http://www.lightshowpi.com/
    #
    # Author: Todd Giles (todd@lightshowpi.com)
    # Author: Chris Usey (chris.usey@gmail.com)
    # Author: Ryan Jennings
    # Jan 12 2014 - latest additions / mutilations by Scott Driscoll
    # CuriousInventor.com | https://plus.google.com/+ScottDriscoll
    #
    # Licensed under the BSD license.  See full license in LICENSE file.

'''

from __future__ import print_function
import RPi.GPIO as GPIO
import time
from multiprocessing import Process
import wave
import decoder
import numpy as np
import alsaaudio as audio
import os
import threading

# Number of frequency channels
GPIOLEN = 3

# How much data to read at once (must be 2**n)
CHUNK_SIZE = 2048

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


class SonicRGB(object):

    number = 0

    def __init__(self, red, green, blue, commonCathode=False,
                 pwmFrequency=100, cutoffs=None):
        self.red = red
        self.green = green
        self.blue = blue
        self.commonCathode = commonCathode
        self.pwmFrequency = pwmFrequency
        self.cutoffs = cutoffs
        if commonCathode:
            self.ON = 0
        else:
            self.ON = 100
        self.OFF = 100 - self.ON

        self.playing = None

        # Use numbering based on P1 header
        GPIO.setup(self.red, GPIO.OUT)
        GPIO.setup(self.green, GPIO.OUT)
        GPIO.setup(self.blue, GPIO.OUT)

        GPIO.output(self.red, GPIO.HIGH)
        GPIO.output(self.green, GPIO.HIGH)
        GPIO.output(self.blue, GPIO.HIGH)

        # PWM
        self.pwm = []
        self.pwm.append(GPIO.PWM(self.red, self.pwmFrequency))
        self.pwm.append(GPIO.PWM(self.green, self.pwmFrequency))
        self.pwm.append(GPIO.PWM(self.blue, self.pwmFrequency))
        for p in self.pwm:
            p.start(self.OFF)

        # id of current player
        self.curId = None

        # Flag for restaring current track
        self._restart = False

    def play(self, id, track, finished):

        # If we're already playing a track, interrupt it and wait
        # for everything to be cleared
        if self.playing:
            self._restart = True
            return

        # id of caller
        self.curId = id

        # Set up audio
        if track.lower().endswith('.wav'):
            self.musicFile = wave.open(track, 'r')
        else:
            self.musicFile = decoder.open(track)

        self.sample_rate = self.musicFile.getframerate()
        self.num_channels = self.musicFile.getnchannels()

        self.output = audio.PCM(audio.PCM_PLAYBACK, audio.PCM_NORMAL)
        self.output.setchannels(self.num_channels)
        self.output.setrate(self.sample_rate)
        self.output.setformat(audio.PCM_FORMAT_S16_LE)
        self.output.setperiodsize(CHUNK_SIZE)

        self.frequency_limits = self._calculate_channel_frequency(50, 15000)

        # Start playing...
        self.playing = True
        self.thread = threading.Thread(target=self._play, args=[finished])
        self.thread.start()

    def _play(self, finished):
        for p in self.pwm:
            p.ChangeDutyCycle(self.OFF)

        data = self.musicFile.readframes(CHUNK_SIZE)
        while data != '':
            try:
                self.output.write(data)
            except:
                break

            values = self._calculate_levels(data, self.sample_rate,
                                            self.frequency_limits)

            if self.commonCathode:
                for p, val in zip(self.pwm, values):
                    p.ChangeDutyCycle(int(100 - val))
            else:
                for p, val in zip(self.pwm, values):
                    p.ChangeDutyCycle(int(val))

            if self._restart:
                try:
                    self.musicFile.rewind()
                except:
                    pass
                self._restart = False
            data = self.musicFile.readframes(CHUNK_SIZE)

        self.musicFile.close()
        for p in self.pwm:
            p.ChangeDutyCycle(self.OFF)
        finished()
        self.playing = False
        self.curId = None
        return 0

    def busy(self, id):
        if self.curId:
            return self.curId != id
        else:
            return False

    def restart(self):
        self._restart = True

    def _calculate_levels(self, data, sample_rate, frequency_limits):
        '''Calculate frequency response for each channel

        Initial FFT code inspired from the code posted here:
        http://www.raspberrypi.org/phpBB3/viewtopic.php?t=35838&p=454041

        Optimizations from work by Scott Driscoll:
        http://www.instructables.com/id/Raspberry-Pi-Spectrum-Analyzer-with-RGB-LED-Strip-/
        '''

        # create a numpy array. This won't work with a mono file, stereo only.
        data_stereo = np.frombuffer(data, dtype=np.int16)

        if (self.num_channels == 2):
            # data has two channels and 2 bytes per channel
            data = np.empty(len(data) / 4)
            # pull out the even values, just using left channel
            data[:] = data_stereo[::2]
        else:
            data = data_stereo

        # if you take an FFT of a chunk of audio, the edges will look like
        # super high frequency cutoffs. Applying a window tapers the edges
        # of each end of the chunk down to zero.
        window = np.hanning(len(data))
        data = data * window

        # Apply FFT - real data
        fourier = np.fft.rfft(data)

        # Remove last element in array to make it the same size as CHUNK_SIZE
        fourier = np.delete(fourier, len(fourier) - 1)

        # Calculate the power spectrum
        power = np.abs(fourier) ** 2

        result = [0 for i in range(GPIOLEN)]
        for i in range(GPIOLEN):
            # take the log10 of the resulting sum to approximate how human ears
            # perceive sound levels
            result[i] = np.sum(power[self._piff(frequency_limits[i][0], sample_rate):
                                     self._piff(frequency_limits[i][1], sample_rate):1])
        result = np.clip(result, 1.0, 1.0e20)
        mag = 0.01 * np.sqrt(np.dot(result, result))
        result = result / mag
        # print(result)
        #result = np.clip(100 * result / np.max(result), 0, 100)
        return result

    def _piff(self, val, sample_rate):
        '''Return the power array index corresponding to a particular frequency.'''
        return int(CHUNK_SIZE * val / sample_rate)

    def _calculate_channel_frequency(self, min_frequency, max_frequency):
        '''Calculate frequency values for each channel'''

        if self.cutoffs:
            f0, f1, f2, f3 = self.cutoffs
            return [[f0, f1], [f1, f2], [f2, f3]]

        # How many channels do we need to calculate the frequency for
        channel_length = GPIOLEN

        octaves = (np.log(max_frequency / min_frequency)) / np.log(2)
        octaves_per_channel = octaves / channel_length
        frequency_limits = []
        frequency_store = []

        frequency_limits.append(min_frequency)
        for i in range(1, GPIOLEN + 1):
            frequency_limits.append(
                frequency_limits[-1] * 2 ** octaves_per_channel)
        for i in range(0, channel_length):
            frequency_store.append(
                (frequency_limits[i], frequency_limits[i + 1]))

        return frequency_store
