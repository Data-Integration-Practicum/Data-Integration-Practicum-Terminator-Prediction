from sklearn.ensemble import RandomForestClassifier

import numpy as np

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