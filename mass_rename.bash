SWEEP=206

#linac1_1_air_120V_206

for RUN in {0..99}
do
	FILE1="data/linac1_${RUN}_air_120V_${SWEEP}"
	NEWFILE1="data/linac1_${RUN}_ice_120V_${SWEEP}"
	mv ${FILE1} ${NEWFILE1}

	FILE2="data/linac2_${RUN}_air_120V_${SWEEP}"
	NEWFILE2="data/linac2_${RUN}_ice_120V_${SWEEP}"
	mv ${FILE2} ${NEWFILE2}

	FILE3="data/linac3_${RUN}_air_120V_${SWEEP}"
	NEWFILE3="data/linac3_${RUN}_ice_120V_${SWEEP}"
	mv ${FILE3} ${NEWFILE3}
	
	FILE4="data/linac4_${RUN}_air_120V_${SWEEP}"
	NEWFILE4="data/linac4_${RUN}_ice_120V_${SWEEP}"
	mv ${FILE4} ${NEWFILE4}
done