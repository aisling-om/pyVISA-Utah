#!/usr/bin/env python

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

agilent.timeout = 25000 # 25 s in ms

label=sys.argv[1]
tx=int(sys.argv[2])
if (tx==1):
	changains = [3.2,3.2,3.2,8.0]
else:
	changains = [0.8,0.16,0.4,8.0]

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

nruns = 100
start = time.time()

filename_root="data/linac"

runfile = open("LinacRunNumber", "r")
runnum = runfile.readline()
runnum.rstrip('\n')
runfile.close()

new_runnum = [str(int(runnum)+1)]
runfile = open("LinacRunNumber", "w")
runfile.writelines(new_runnum)
runfile.close()

print "================================="
print "BEGINNING RUN", runnum
print "================================="

filename = "data/timestamps_%s" % (runnum)
timefile = open(filename, "w")

for run in range(nruns):
#while True:
	time1 = time.time()
	now_time = time.localtime()
	
	agilent.write(":DIGITIZE")
	
	agilent.write(":WAVEFORM:SOURCE CHANNEL1")
	values = agilent.query_ascii_values(":WAVEFORM:DATA?", converter='s') #has /n at end

#	points = len(values)
#	print(points)
	
	filename = filename_root + "1_%i_%s_%s" % (run, label, runnum)
	f = open(filename, "w")
	for value in values:
		f.write("%s\n" % value)
	f.close()

	agilent.write(":WAVEFORM:SOURCE CHANNEL2")
	values = agilent.query_ascii_values(":WAVEFORM:DATA?",converter='s') #has /n at end
	
	filename = filename_root + "2_%i_%s_%s" % (run, label, runnum)
	f = open(filename, "w")
	for value in values:
		f.write("%s\n" % value)
	f.close()

	agilent.write(":WAVEFORM:SOURCE CHANNEL3")
	values = agilent.query_ascii_values(":WAVEFORM:DATA?",converter='s') #has /n at end
	
	filename = filename_root + "3_%i_%s_%s" % (run, label, runnum)
	f = open(filename, "w")
	for value in values:
		f.write("%s\n" % value)
	f.close()

	agilent.write(":WAVEFORM:SOURCE CHANNEL4")
	values = agilent.query_ascii_values(":WAVEFORM:DATA?",converter='s') #has /n at end
	
	filename = filename_root + "4_%i_%s_%s" % (run, label, runnum)
	f = open(filename, "w")
	for value in values:
		f.write("%s\n" % value)
	f.close()

	timefile.write("%s,%s,%s,%s,%s,%s,%s,%s\n" % (run,time1,now_time[0],now_time[1],now_time[2],now_time[3],now_time[4],now_time[5])) #year, month, day, hour, minute, second

	time2 = time.time()
	print "Shot ", run,": ", time2-time1, " s"

timefile.close()
agilent.close()

print "================================="
print "ENDING RUN", runnum
print "================================="


elapsed = time.time() - start
print "Total time: ", elapsed
print "Time per shot: ", elapsed/float(nruns), " s"
