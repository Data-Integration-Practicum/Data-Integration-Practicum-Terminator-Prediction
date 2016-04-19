#! /bin/bash
if [ "$1" != "" && "$2" != "" ]; then
	`mkdir $2`
	#Writes the file "trimmedseqs.fa" with all the segments, and the files
	#"segment[1-8].fa" with the individual 50bp segments.
	`python splitsegments1.py $1 $2`
else
echo "Enter input sequence file name as first parameter and short name as second parameter."
fi
