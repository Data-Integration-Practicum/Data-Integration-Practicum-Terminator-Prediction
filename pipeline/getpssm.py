import sys
import string
with open(sys.argv[1]) as F:
    contents = F.readlines();
name = sys.argv[2]
nmotifs = sys.argv[3]
ln = 0
for m in xrange(nmotifs):
    while not string.startswith(contents[ln],"log-odds matrix:"):
        ln += 1
    with open(name+"-"+str(m), 'w') as F:
        while contents[ln][0] != "-":
            F.write(contents[ln])
            ln += 1
    ln += 1
    