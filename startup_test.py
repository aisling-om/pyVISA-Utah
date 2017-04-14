#!/usr/bin/env python

#to automatically collect data from an instrument to output file "outfile":
# python -u visatest.py > outfile

import time, csv, string, sys

import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as ppl

import visa
rm = visa.ResourceManager()

print (rm.list_resources())
#agilent = rm.open_resource("USB0::0x0957::0x17A4::MY52012809::INSTR")
agilent = rm.open_resource("USB0::0x0957::0x900E::MY52090105::INSTR")
print(agilent.query("*IDN?"))

#agilent.timeout = 25000 # 25 s in ms, never tested

label=sys.argv[1]
tx = int(sys.argv[2])
if (tx==1):
	changains = [0.4,0.4,0.4,8.0]
else:
	changains = [0.8,0.08,0.08,8.0]

#agilent.write()
agilent.write("*CLS")
agilent.write("*RST")

agilent.write(":VIEW CHAN1")
agilent.write(":VIEW CHAN2")
agilent.write(":VIEW CHAN3")
agilent.write(":VIEW CHAN4")

agilent.write(":TIMEBASE:SCALE 2E-6")
agilent.write(":TIMEBASE:DELAY 4E-6")
agilent.write(":TIMEBASE:REFERENCE CENTER")

agilent.write(":TRIGGER:MODE EDGE")
agilent.write(":TRIGGER:SWEEP TRIG")
agilent.write(":TRIGGER:EDGE:SOURCE CHAN4")
agilent.write(":TRIGGER:EDGE:SLOPE POSITIVE")

agilent.write(":CHANNEL4:RANGE %f" % changains[3])
agilent.write(":TRIGGER:LEVEL CHAN4, 2.0")

agilent.write(":CHANNEL1:RANGE %f" % changains[0])
#agilent.write(":TRIGGER:LEVEL CHAN1,-0.04")

agilent.write(":CHANNEL2:RANGE %f" % changains[1])
#agilent.write(":TRIGGER:LEVEL CHAN2,-0.04")

agilent.write(":CHANNEL3:RANGE %f" % changains[2])
#agilent.write(":TRIGGER:LEVEL CHAN3,-0.04")

#converter=u's'   for ascii query

#agilent.write(":SYSTEM:HEADER OFF")
agilent.write(":ACQUIRE:MODE RTIME")
agilent.write(":WAVEFORM:FORMAT ASCII")
