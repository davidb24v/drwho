from sonicRGB import SonicRGB
import time
import RPi.GPIO as GPIO

m = SonicRGB(pwmFrequency=500)

m.play('mp3/tardis.mp3')
#m.play('../Runaway.mp3')

time.sleep(1)
GPIO.cleanup()
