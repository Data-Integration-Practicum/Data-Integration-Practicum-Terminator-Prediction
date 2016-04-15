import sys
import string
with open(sys.argv[1]) as F:
    contents = F.readlines();
name = sys.argv[2]
nmotifs = int(sys.argv[3])
ln = 0
for m in xrange(nmotifs):
    while not contents[ln].startswith("log-odds matrix:"):
        ln += 1
    with open(name+"-"+str(m), 'w') as F:
        ln += 1
        while contents[ln][0] != "-":
            F.write(contents[ln])
            ln += 1
    ln += 1
    