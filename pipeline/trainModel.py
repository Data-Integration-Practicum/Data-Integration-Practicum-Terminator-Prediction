from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

from featureHelpers import *

import numpy as np
import random
import sys

class PredictModel():
	rf = RandomForestClassifier(criterion="entropy", n_estimators = 300, max_depth = 100)

	def __init__(self, GO):
		self.GO = GO

		# Get PSSMs
		allPSSMFiles = ["./" + self.GO + "/segment" + str(i) + "-" + str(j) \
						for i in xrange(1,9) for j in xrange(4)]

		self.allPSSMs = [readMatrix(f) for f in allPSSMFiles]

		# GCFeat returns a list of all 8
		self.PosFeatures = [GCFeat(seq) for seq in pos if seq[0] != '>']
		self.NegFeatures = [GCFeat(seq) for seq in neg if seq[0] != '>']

		self.__trainModel()

	# Calculate the feature of the newly passed in sequence		
	def getPrediction(self, seq):
		feat = GCFeat(seq)

		for M in self.allPSSMs:
			feat.append(computeMaxScore(M, seq))

		return rf.predict(feat)[0]

	# Run this before get prediction
	def __trainModel(self):
		with open("negative.fa") as F:
			neg = F.readlines()
			nneg = len(neg)/2

		with open("./" + self.GO + "/trimmedseqs.fa") as F:
		    pos=F.readlines()

		npos= len(pos)/2
		S = random.sample(range(nneg),npos)
		neg = [neg[i*2+1] for i in S]
		nmotifs = 4 #sys.argv[1]

		for M in self.allPSSMs:
		    for i in xrange(npos): 
		        PosFeatures[i].append(computeMaxScore(M,pos[i*2+1]))
		        NegFeatures[i].append(computeMaxScore(M,neg[i]))
		print "Train features calculated"

		#X: each sample is a row, each column is a feature
		X = np.array(list(PosFeatures) + list(random.sample(NegFeatures,npos)), dtype=np.float)
		#y: labels
		y = np.array([1 for x in xrange(npos)] + [0 for x in xrange(npos)])

		combined = zip(X, y)
		random.shuffle(combined)
		X, y = zip(*combined)

		rf.fit(X, y)

GO = sys.argv[1]

model = PredictModel(GO)

joblib.dump(model, 'classifier' + '_' + GO)
