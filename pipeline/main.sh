#! /bin/bash
if [ "$1" != "" ] && [ "$2" != "" ]; then
	NMOTIFS=4	
	listOfSegments="segment1 segment2 segment3 segment4 segment5 segment6 segment7 segment8"	
	#Make the PSSMs
	for f in $listOfSegments
	do `mkdir $1/$f`
		`$2 $1/$f.fa -dna -mod oops -nmotifs $NMOTIFS -maxw 12 -oc $1/$f`
		#Writes the PSSMs as segment1-0, segment1-1 .... segment8-($NMOTIFS-1)
		`python getpssm.py $1 $f $NMOTIFS`
	done
	`mkdir ./classifiers`
	`python trainModel.py $1`
else
    echo "Enter short name as first parameter and MEME location (e.g. /meme/bin/meme) as second parameter."
fi
