from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(criterion="entropy", n_estimators = 300, max_depth = 100)

# Calculate the feature of the newly passed in sequence

def getNewFeature(seq):
	feat = GCFeat(seq)

	for M in allPSSMs:
		feat.append(computeMaxScore(M, seq))

	return feat

# Input the GO annotation and get the corresponding PSSM back
def getPSSM(go):
	allPSSMFiles = ["./" + go + "/segment" + str(i) + "-" + str(j) \
					for i in xrange(1,9) for j in xrange(nmotifs)]
	allPSSMs = [readMatrix(f) for f in allPSSMFiles]

	return allPSSM

def trainModel(go):
	with open("negative.fa") as F:
	neg=F.readlines()

	nneg = len(neg)/2

	with open("./" + go + "/trimmedseqs.fa") as F:
	    pos=F.readlines()

	npos= len(pos)/2
	S = random.sample(range(nneg),npos)
	neg = [neg[i*2+1] for i in S]
	nmotifs = 4 #sys.argv[1]

	for M in allPSSMs:
	    for i in xrange(npos): 
	        PosFeatures[i].append(computeMaxScore(M,pos[i*2+1]))
	        NegFeatures[i].append(computeMaxScore(M,neg[i]))
	print "Train features calculated"

	#X: each sample is a row, each column is a feature
	X = numpy.array(list(PosFeatures) + list(random.sample(NegFeatures,npos)), dtype=numpy.float)
	#y: labels
	y = [1 for x in xrange(npos)] + [0 for x in xrange(npos)]  

	y = numpy.array(y)

	rf.fit(X, y)

def getPrediction(feat):
	rf.predict(feat)



