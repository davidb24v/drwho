from sonicRGB import SonicRGB
import time
import RPi.GPIO as GPIO

m = SonicRGB(pwmFrequency=500)

#m.play('../sherrifFatman.mp3')
#time.sleep(5)

#m.play('../Runaway.mp3')
#time.sleep(1)
m.play('mp3/theme.mp3')
time.sleep(1)
m.play('mp3/tardis1.mp3')
time.sleep(1)
m.play('mp3/spacenoise.mp3')
time.sleep(1)
m.play('mp3/tardis.mp3')
time.sleep(1)
m.play('mp3/scream.mp3')
time.sleep(1)
m.play('mp3/dalekchorus1a.mp3')
#time.sleep(1)
#m.play('../sherrifFatman.mp3')
#time.sleep(5)
#m.play('../Runaway.mp3')

time.sleep(1)
GPIO.cleanup()
