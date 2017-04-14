#for zipped runs:
# find on-source and off-source power spectra
# can plot them
# average all per run?
# write spectra to file


# run as ./python powerspec2.py 

# Run Ant On/Off Avg_Spectrum

#','.join(str(n) for n in mylist) will turn [0,1,2] to "0,1,2"
#[float(x) for x in "0,1,2".split(",")] can read "0,1,2"

import os, sys, csv, string, zipfile
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as ppl

from scipy.fftpack import fft
import scipy.signal as sig

#function to read the data:

def read_datazip(filename, daqtype, archive):

	myfile = archive.open(filename, "r")

	values = myfile.readlines()
	points = len(values)
 
	values_float = [float(x) for x in values[:points-2]]
	times=[x*1E-10 for x in range(0,points-2)]
 
	timenp = np.array(times)
	chan1np = np.array(values_float)
	return timenp, chan1np

def read_data(filename, daqtype):

    if (daqtype == "aom_daq"):
        myfile = open(filename, "r")

        values = myfile.readlines()
        points = len(values)
 
        values_float = [float(x) for x in values[:points-2]]
        times=[x*1E-10 for x in range(0,points-2)]
 
        timenp = np.array(times)
        chan1np = np.array(values_float)
        return timenp, chan1np
 
    elif (daqtype == "agilent"):
        filereader = csv.reader(open(filename), delimiter=',')
        time = []
        chan1 = []
        chan2 = []
        chan3 = []

        for i in range(22):
            filereader.next()

        for row in filereader:
            time.append(float(row[0]))
            chan1.append(float(row[1]))
            chan2.append(float(row[2]))
            chan3.append(float(row[3]))

        timenp = np.array(time)
        chan1np = np.array(chan1)
        chan2np = np.array(chan2)
        chan3np = np.array(chan3)
        return timenp, chan1np, chan2np, chan3np

    else:
        print "DAQ type %s unknown" % daqtype

#run = int(sys.argv[1])
#antenna = sys.argv[2]

#for antenna in ["1","3"]:
for antenna in ["1"]:
	for run in range(310,367): 
		zpath = "/Volumes/Macintosh HD 2/data_save/data_19_1/run_%i.zip" % (run)
		myzip = zipfile.ZipFile(zpath, 'r')

		#data_11_1/run_13/linac1 : elem 22
		#run_79/linac2 : elem 12?
		#run_100/linac2 : elem 13?
		subrunlist = []
		for elem in myzip.namelist():
			try:
		#		if (elem[15] == "0" ):
				if (elem[13] == antenna ):
					subrunlist.append(elem)
			except:
				continue

		print subrunlist
		if (len(subrunlist) == 0):
			print "No runs found"
			continue
		#myzip.close()       

		filenames = subrunlist
		nfiles = len(subrunlist)
		print "Number of files found: ", nfiles

		#filenames = ['oscil/data_save/run_105/linac1_0_beam_120V_105','oscil/data_save/run_105/linac2_0_beam_120V_105','oscil/data_save/run_105/linac3_0_beam_120V_105']
		filetype = 'aom_daq'

		spectra_onsource=[0 for i in range(129)]
		spectra_offsource=[0 for i in range(129)]
		nfiles = 0

		for filename in filenames:
		#	meas_times, values_flt1 = read_data(filename, filetype)
			meas_times, values_flt1 = read_datazip(filename, filetype, myzip)


			#resolution = 100 ps = 1E-10 s
			#N = 200003
			#lesson: multiply seconds time by 1E10 ok
			#rabbit 135000:160000
			#worm 142850:143050

			N = len(meas_times)
			T = 1.0/1.0E10
			w = sig.hamming(160000-135000)
			fs = 1.0/T

 			#On-Source
 			try:
				windowed1 = values_flt1[135000:160000]*w
			except ValueError:
				continue
				
			nfiles += 1
				
			f, Pwelch_spec = sig.welch(windowed1, fs, scaling='density')
			power = []
			for i in range(len(Pwelch_spec)):
				p = Pwelch_spec[i]*Pwelch_spec[i]*f[i]*3.90625000e+07
				power.append(p)	
			spectra_onsource = [spectra_onsource[j] + power[j] for j in range(129)]
		#	spectra.append(power)
	
			#Off-Source
			windowed1 = values_flt1[0:25000]*w
			f, Pwelch_spec = sig.welch(windowed1, fs, scaling='density')
			power = []
			for i in range(len(Pwelch_spec)):
				p = Pwelch_spec[i]*Pwelch_spec[i]*f[i]*3.90625000e+07
				power.append(p)	
			spectra_offsource = [spectra_offsource[j] + power[j] for j in range(129)]
		#	spectra.append(power)	


		myzip.close()
		if (nfiles == 0):
			print "No triggers processed"
			continue

		print "Number of files processed: ", nfiles

		spectra_onsource = [spectra_onsource[i]/nfiles for i in range(129)]
		spectra_offsource = [spectra_offsource[i]/nfiles for i in range(129)]

		spectra_onsource_str = ",".join(str(j) for j in spectra_onsource)
		spectra_offsource_str = ",".join(str(j) for j in spectra_offsource)


		if (antenna=="1"):
			f_on = open('utah_onsource_1.csv', 'a')
			f_off = open('utah_offsource_1.csv', 'a')
		else:
			f_on = open('utah_onsource_3.csv', 'a')
			f_off = open('utah_offsource_3.csv', 'a')

		filewriter_on = csv.writer(f_on, delimiter='\t')
		filewriter_on.writerow([run] + [antenna] + [1] + [nfiles]+[spectra_onsource_str])

		filewriter_off = csv.writer(f_off, delimiter='\t')
		filewriter_off.writerow([run] + [antenna] + [0] + [nfiles]+[spectra_offsource_str])

		f_on.close()
		f_off.close()

"""
ax = ppl.subplot(111)

#ppl.semilogy(f, Pwelch_spec,"k*", lw=2)
#ppl.xlabel('frequency [Hz]')
#ppl.ylabel('PSD')
#ax.set_title(filename + " Welch periodogram")

#ppl.semilogy(f, spectra[0],"k-",f, spectra[1],"k--",f, spectra[2],"b-",f, spectra[3],"b--",f, spectra[4],"r-",f, spectra[5],"r--", lw=2)
ppl.semilogy(f, spectra_onsource,"k-",f, spectra_offsource,"k--", lw=2)
ppl.xlabel('frequency [Hz]')
ppl.ylabel('power')
ax.set_title(filename + " power")
#ax.set_ylim([1E-15,1E-8])

ppl.grid()
ppl.show()
"""
