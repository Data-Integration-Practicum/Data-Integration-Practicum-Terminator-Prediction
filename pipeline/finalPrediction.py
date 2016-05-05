#! /usr/bin/env python

from Bio import SeqIO
from trainModel import Model
import pandas as pd
import pickle
import sys
import re

"""
    This is file takes a GO term and a file name of genome to be tested
    as imput, and gives the final prediction
"""
# Classifier's file name
GO = sys.argv[1]
# The file name of the genome to be predicted (should be .fa file)
genomeFile = sys.argv[2]

fileName = genomeFile.split('/')[-1][:-3]

# Specifying the maximum length of bp in a file
maximumFileBP = 100000

try:
    model = pickle.load(open('./classifiers/' + GO, "r"))
except IOError:
    print "The classifier of " + sys.argv[1] \
    + "is not existed under the folder ./classifiers."

columns = ['ID', 'Offset', 'Nearby Sequence']
results = pd.DataFrame(columns=columns)

for seq_record in SeqIO.parse(genomeFile, "fasta"):
    count = 0

    sequence = str(seq_record.seq)
    sequenceSegments = re.split(r'N+', sequence)
    
    offsets = [0] + [m.end(0) for m in re.finditer(r'N+', sequence)]

    fileNum = range(1, len(sequence)/maximumFileBP + 2)

    print "offset calc done"

    posSegPair = zip(offsets, sequenceSegments)

    for offset, segment in posSegPair:
        j = 0

        print seq_record.id + " has been processed for " + str(offset) + " bp"
        print "Currently, " + str(count) + " segments are predicted as TTS"

        while j + 400 < len(segment):

            if (offset + j) / maximumFileBP == fileNum[0]:
                partCount = str(fileNum.pop(0))
                print "Outputing result file of part " + partCount
                results.to_csv('./results/' + GO + '_TTS_' + fileName + '_part-' + partCount + '.csv')
                print "Done!"
                results = pd.DataFrame(columns=columns)

            currSeq = str(segment[j:j+400])
            
            prediction = model.predict(currSeq)
            
            if prediction == 1:
                ## add seq_record.id, offset(i+300), nearby sequence(str(seq_record[i+300:i+400])), to results dataframe
                curDF = [seq_record.id, j+offset+300, str(segment[j+300:j+400])]
                results.loc[len(results)] = curDF
                count = count + 1
                    
            j = j + 50

# Output the prediction result
results.to_csv('./results/' + GO + '_TTS_' + fileName + '.csv')