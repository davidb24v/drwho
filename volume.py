'''

Set the alsa mixer volume level

'''

import os
import glob
import subprocess

class Volume(object):

    def __init__(self, wd):
        self.wd = wd
        self.setVolume(create=True)

    def setVolume(self, create=False):
        file = os.path.join(self.wd, "Sounds", "Volume", "Level.txt")
        if glob.glob(file):
            try:
                vol = open(file, 'rb')
                data = vol.readline().strip()
                volume = int(data)
            except:
                volume = 80
            finally:
                vol.close()
        else:
            volume = 80
            if create:
                if not os.path.isdir(os.path.join(self.wd, "Volume")):
                    try:
                        subprocess.call(['mkdir', self.wd, "Volume"])
                    except:
                        pass
                try:
                    vol = open(file, "wb")
                    vol.write(str(volume) + "\n")
                    vol.close()
                except:
                    pass
        subprocess.call(["amixer", "set", "PCM", "{}%".format(volume)])

    def fileEvent(self):
        self.setVolume()
