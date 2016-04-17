from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

import sys
import numpy
import random
from sklearn.externals import joblib
from sklearn import cross_validation

def GCFeat(seq):
    nGC = [0,0,0,0,0,0,0,0]
    for seg in xrange(8):
        nGC[seg] += seq[seg*50:(seg+1)*50].count("G") + seq[seg*50:(seg+1)*50].count("C")
    return [1.0 * n / len(seq) for n in nGC] #len(seq) has to be 400

def readMatrix(fname):
    #print fname
    with open(fname) as F:
        M = []
        line = F.readline()
        while line != "":
            M.append(line.strip().split())
            line = F.readline()
    return M
    
def computeMaxScore(PSSM, seq, letters={"A":0,"C":1,"T":2,"G":3}):
    scores = []
    for start in xrange(len(seq)-len(PSSM[0])):
        score = 0.0
        for nt in xrange(len(PSSM[0])):
            score += int(PSSM[letters[seq[start+nt]]][nt])  
        scores.append(score)  
    return max(scores)  
    
#####    
        
with open("negative.fa") as F:
    neg=F.readlines()
nneg = len(neg)/2
with open("trimmedseqs.fa") as F:
    pos=F.readlines()
npos= len(pos)/2
S = random.sample(range(nneg),npos)
neg = [neg[i*2+1] for i in S]
nmotifs = 4 #sys.argv[1]

#Calculate Features
allPSSMFiles = ["segment"+str(i)+"-"+str(j) for i in xrange(1,9) for j in xrange(nmotifs)]
allPSSMs = [readMatrix(f) for f in allPSSMFiles]
PosFeatures = [GCFeat(seq) for seq in pos if seq[0] != '>'] #GCFeat returns a list of all 8
NegFeatures = [GCFeat(seq) for seq in neg if seq[0] != '>']

for M in allPSSMs:
    for i in xrange(npos): 
        PosFeatures[i].append(computeMaxScore(M,pos[i*2+1]))
        NegFeatures[i].append(computeMaxScore(M,neg[i]))
print "Features calculated"
#X: each sample is a row, each column is a feature
X = numpy.array(list(PosFeatures) + list(random.sample(NegFeatures,npos)), dtype=numpy.float)
#y: labels
y = [1 for x in xrange(npos)] + [0 for x in xrange(npos)]    
y = numpy.array(y)       

clf = DecisionTreeClassifier(criterion="entropy",max_depth=4)

# Random forest classifier
for i in xrange(5,40):
    rf = RandomForestClassifier(criterion="entropy", max_depth=i)
    # clf.fit(X,y)
    rf.fit(X, y)
    scores = cross_validation.cross_val_score(rf, X, y, cv=5)
    print "This is the score for max-depth of " + str(i)
    print scores
    print sum(scores)/5

scores = cross_validation.cross_val_score(clf, X, y, cv=5)




#clf.fit(X,y)
#joblib.dump(clf, 'classifier') 

#Later:
#clf = joblib.load('classifier') 