#! /usr/bin/env python

from sklearn.ensemble import RandomForestClassifier
from featureHelpers import *
import numpy as np
import random
import pickle
import sys

# This is the file that is used for getting classifier, given the 
# specific GO term the user input

# The GO term as the only parameter that is passed in
GO = sys.argv[1]

rf = RandomForestClassifier(criterion="entropy", \
	 n_estimators = 300, max_depth = 100, class_weight={0:100, 1:1})

#####################
# Get Train samples #
#####################
with open("negative.fa") as F:
	neg = F.readlines()
	nneg = len(neg)/2

with open(GO + "/trimmedseqs.fa") as F:
    pos=F.readlines()

npos= len(pos)/2
S = random.sample(range(nneg),npos)
neg = [neg[i*2+1] for i in S]
nmotifs = 4 #sys.argv[1]

#############
# Get PSSMs #
#############

allPSSMFiles = [GO + "/" + "segment" + str(i) + "/segment" + str(i) + "-" + str(j) \
			   for i in xrange(1,9) for j in xrange(nmotifs)]
allPSSMs = [readMatrix(f) for f in allPSSMFiles]

# GCFeat returns a list of all 8
PosFeatures = [GCFeat(seq) for seq in pos if seq[0] != '>']
NegFeatures = [GCFeat(seq) for seq in neg if seq[0] != '>']


###############
# Train model #
###############
for M in allPSSMs:
    for i in xrange(npos): 
        PosFeatures[i].append(computeMaxScore(M,pos[i*2+1]))
        NegFeatures[i].append(computeMaxScore(M,neg[i]))
print "Train features calculated"

#X: each sample is a row, each column is a feature
X = np.array(list(PosFeatures) + list(random.sample(NegFeatures,npos)), dtype=np.float)
#y: labels
y = np.array([1 for x in xrange(npos)] + [0 for x in xrange(npos)])

# Randomize the data points, might not be neccesary, only for parameter adjustion use 
combined = zip(X, y)
random.shuffle(combined)
X, y = zip(*combined)

rf.fit(X, y)

# Generate the Model class
class Model():
	# Calculate the feature of the newly passed in sequence
	def __init__(self):
		self.rf = rf
		self.PSSMs = allPSSMs

	def predict(self, seq):
		feat = GCFeat(seq)

		for M in self.PSSMs:
			feat.append(computeMaxScore(M, seq))

		return self.rf.predict(np.array(feat).reshape(1, -1))[0]


model = Model()

# Save it into the classifier folder for future use
pickle.dump(model, open('./classifiers/' + GO, "w"))
