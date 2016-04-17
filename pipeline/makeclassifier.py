from sklearn.tree import DecisionTreeClassifier
import sys
import numpy
import random
from sklearn.externals import joblib

def GCFeat(seq):
    nGC = [0,0,0,0,0,0,0,0]
    for seg in xrange(8):
        nGC[seg] += seq[seg*50:(seg+1)*50].count("G") + seq[seg*50:(seg+1)*50].count("C")
    return [1.0 * n / len(seq) for n in nGC] #len(seq) has to be 400

def readMatrix(fname):
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
            score += PSSM[letters[seq[start+nt]]][nt]  
        scores.append(score)  
    return max(scores)  
    
#####    
        
with open("negative.fa") as F:
    neg = F.readlines()
nneg = len(neg)/2

with open("trimmedseqs.fa") as F:
    pos=F.readlines()
npos= len(pos)/2
nmotifs = int(sys.argv[1])

#Calculate Features
allPSSMFiles = ["segment"+str(i)+"-"+str(j) for i in xrange(1,9) for j in xrange(nmotifs)]
allPSSMs = [readMatrix(f) for f in allPSSMFiles]
PosFeatures = [GCFeat(seq) for seq in pos if seq[0] != '>'] #GCFeat returns a list of all 8
NegFeatures = [GCFeat(seq) for seq in neg if seq[0] != '>']

for M in allPSSMs:
    for i in xrange(npos/2): 
        PosFeatures[i].append(computeMaxScore(M,pos[i*2+1]))
    for i in xrange(nneg/2): 
        NegFeatures[i].append(computeMaxScore(M,neg[i*2+1]))

#X: each sample is a row, each column is a feature
X = numpy.array(PosFeatures + random.sample(NegFeatures,npos))
#y: labels
y = [1 for x in xrange(npos)] + [0 for x in xrange(npos)]           

clf = DecisionTreeClassifier()
clf.fit(X,y)

joblib.dump(clf, 'classifier') 

#Later:
#clf = joblib.load('classifier') 