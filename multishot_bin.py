#!/usr/bin/env python

#to automatically collect data from an instrument to output file "outfile":
# python -u visatest.py > outfile

import time, csv, string

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

#agilent.write()
agilent.write("*CLS")
agilent.write("*RST")

agilent.write(":VIEW CHAN1")
#agilent.write(":VIEW CHAN2")
agilent.write(":VIEW CHAN3")
#agilent.write(":VIEW CHAN4")

agilent.write(":TIMEBASE:SCALE 1E-6")
agilent.write(":TIMEBASE:DELAY 1.25E-6")
agilent.write(":TIMEBASE:REFERENCE CENTER")

agilent.write(":CHANNEL1:RANGE 0.04")
agilent.write(":TRIGGER:SWEEP TRIG")
agilent.write(":TRIGGER:LEVEL CHAN1, 0.0027")

#agilent.write(":CHANNEL2:RANGE 0.04")
#agilent.write(":TRIGGER:LEVEL CHAN2,-0.04")

agilent.write(":CHANNEL3:RANGE 1.0")
#agilent.write(":TRIGGER:LEVEL CHAN3,-0.04")

agilent.write(":CHANNEL4:RANGE 1.0")
#agilent.write(":TRIGGER:LEVEL CHAN4, 2.0")

agilent.write(":TRIGGER:MODE EDGE")
agilent.write(":TRIGGER:EDGE:SLOPE POSITIVE")
agilent.write(":TRIGGER:EDGE:SOURCE CHAN1")

agilent.write(":SYSTEM:HEADER OFF")
agilent.write(":ACQUIRE:MODE RTIME")
agilent.write(":WAVEFORM:FORMAT BIN")

#converter=u's'   for ascii query

nruns = 10
start = time.time()
for run in range(nruns):
	time1 = time.time()
	agilent.write(":DIGITIZE")
	
	agilent.write(":WAVEFORM:SOURCE CHANNEL1")
	values = agilent.query_binary_values(":WAVEFORM:DATA?") #has /n at end

#	points = len(values)
#	print(points)
	
	filename = "sineout1_%i" % run
	f = open(filename, "w")
	for value in values:
		f.write("%s\n" % value)
	f.close()

	agilent.write(":WAVEFORM:SOURCE CHANNEL2")
	values = agilent.query_binary_values(":WAVEFORM:DATA?") #has /n at end
	
	filename = "sineout2_%i" % run
	f = open(filename, "w")
	for value in values:
		f.write("%s\n" % value)
	f.close()

	agilent.write(":WAVEFORM:SOURCE CHANNEL3")
	values = agilent.query_binary_values(":WAVEFORM:DATA?") #has /n at end
	
	filename = "sineout3_%i" % run
	f = open(filename, "w")
	for value in values:
		f.write("%s\n" % value)
	f.close()
	
	agilent.write(":WAVEFORM:SOURCE CHANNEL4")
	values = agilent.query_binary_values(":WAVEFORM:DATA?") #has /n at end
	
	filename = "sineout4_%i" % run
	f = open(filename, "w")
	for value in values:
		f.write("%s\n" % value)
	f.close()

	time2 = time.time()
	print time2-time1, " s"
elapsed = time.time() - start
print "Total time: ", elapsed
print "Time per shot: ", elapsed/10.0, " s"
