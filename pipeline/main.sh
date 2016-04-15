#! /bin/bash

if [ "$1" != "" && "$2" != ""]; then
	NMOTIFS=4
	
	#Split the input sequences into segments
    `python splitsegments1.py $1`
	#Writes the file "trimmedseqs.fa" with all the segments, and the files
	#"segment[1-8].fa" with the individual 50bp segments.
	listOfSegments="segment1 segment2 segment3 segment4 segment5 segment6 segment7 segment8"
	
	#Make the PSSMs
	for f in $listOfSegments
	do
		`mkdir meme_out/$f`
		`./meme/bin/meme $f.fa -p 6 -dna -mod oops -nmotifs $NMOTIFS -maxw 12 -oc meme_out/$f`
		`python getpssm.py meme_out/$f/meme.txt $f $NMOTIFS`
		#Writes the PSSMs as segment1-0, segment1-1 .... segment8-($NMOTIFS-1)
	done
	
	#Evaluate the PSSMs and GC content
	`python makeclassifier.py $NMOTIFS`
	
	#Deploy the classifier on genome sequences 
	
else
    echo "Enter input sequence file name as first parameter and input genome sequence file name as second parameter."
fi
