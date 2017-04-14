
RUN=$1
RUNDIR=run_$RUN
DATA_FOLDER=data
BKP_ROOT=/Volumes/Macintosh\ HD\ 2/data_save
DAY_FOLDER=data_19_1


mkdir ${DATA_FOLDER}/$RUNDIR

mv ${DATA_FOLDER}/linac*_$RUN ${DATA_FOLDER}/$RUNDIR 
mv ${DATA_FOLDER}/timestamps_$RUN ${DATA_FOLDER}/$RUNDIR 

cd ${DATA_FOLDER}
zip -rq $RUNDIR $RUNDIR 
cd ..

if [[ -e ${BKP_ROOT}/${DAY_FOLDER}/${RUNDIR}.zip  ]]; then
	echo "Already exists in backup folder, will not move. "
else #why doesn't ${BKP_ROOT} work here??? mv complains
	mv ${DATA_FOLDER}/${RUNDIR}.zip /Volumes/Macintosh\ HD\ 2/data_save/${DAY_FOLDER}
fi

mv ${DATA_FOLDER}/$RUNDIR ~/.Trash/

echo Done with Run $RUN 