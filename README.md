# drwho

Bits and pieces towards a Dr Who themed sound and light box



Includes Adafruit_I2C and Adafruit_MCP230xx are (C) Adafruit - see files for details

Includes parts of the decoder library from http://www.brailleweb.com:

Copyright (C) 2010-2011 by Dalen Bernaca

YOU ARE ALLOWED TO USE AND DISTRIBUTE THIS PROGRAM FREELY

YOU ARE ALLOWED TO MODIFY THIS PROGRAM IN ONE CONDITION:
THAT YOU SEND YOUR MODIFIED VERSION TO THE AUTHOR BY E-MAIL
WITH SHORT EXPLANATION REGARDING THE MODIFICATION(S)
IF YOUR MODIFICATION(S) INCREASE THE QUALITY OF THE PROGRAM
THEY WILL BE TAKEN IN VIEW FOR THE NEW OFFICIAL VERSION

Author: Dalen Bernaca
        dbernaca@blue-merlin.hr
Version: 1.5XB

THE AUTHOR IS NOT RESPONSIBLE FOR ANY DAMAGE INFLICTED BY MISSUSE/ABUSE OF THIS SOFTWARE
ANY OTHER PROGRAM WITH SAME/SIMILAR NAME AND PURPOSE WHICH IS NOT PROCURED FROM
http://www.brailleweb.com/
IS NOT THE OFFICIAL VERSION WHATEVER MAY BE WRITTEN IN THE SOURCE CODE AND
SHOULD BE TREATED WITH ENORMOUS CARE
THE AUTHOR IS NOT ACCOUNTABLE FOR SUCH SOURCE CODE


Includes modified code from:

  http://www.lightshowpi.com/
 
  Author: Todd Giles (todd@lightshowpi.com)
  Author: Chris Usey (chris.usey@gmail.com)
  Author: Ryan Jennings
  Jan 12 2014 - latest additions / mutilations by Scott Driscoll
  CuriousInventor.com | https://plus.google.com/+ScottDriscoll
 
  Licensed under the BSD license.


## Setup the Pi

Edit /etc/modprobe.d/raspi-blacklist.conf and comment out the line:
> blacklist i2c-bcm2708

Edit /etc/modules and add:
> i2c-bcm2708

> i2c-dev

Reboot.

### Install packages

>sudo apt-get install python-setuptools python-dev python-pip \

>                     python-smbus i2c-tools python-alsaaudio \

>                     python-inotifyx


> wget http://www.brailleweb.com/downloads/decoder-1.5XB-Unix.zip

> unzip decoder-1.5XB-Unix.zip

> cd decoder-1.5XB-Unix

> cd mutagen-1.19

> sudo python setup.py install

> cd

### Get this software
> git clone git@github.com:davidb24v/drwho.git

### Integrate into system

Edit /etc/rc.local and add the line

> python /home/pi/drwho/tardis.py

