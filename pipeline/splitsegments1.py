import sys

with open(sys.argv[1]) as F:
    contents = F.readlines();
with open("trimmedseqs.fa",'w') as out:
    allFiles = [open("segment1.fa",'w'),open("segment2.fa",'w'),open("segment3.fa",'w'),open("segment4.fa",'w'),open("segment5.fa",'w'),open("segment6.fa",'w'),open("segment7.fa",'w'),open("segment8.fa",'w')]
    j = 0
    while j < len(contents):
        head = contents[j]
        j+=1
        seq = contents[j].strip()
        while True:
            j +=1
            if j == len(contents) or len(contents[j]) == 0:
                break
            if contents[j][0] != ">":
                seq += contents[j].strip()
       	    else:
                break
        if "N" in seq:
            continue
        if len(seq) > 400:
            out.write(head)
            out.write(seq[-400:])
            out.write("\n")
            for i in xrange(8):
                allFiles[i].write(head)
                if i == 0:
                    allFiles[i].write(seq[-50:])
                else: 
                    allFiles[i].write(seq[-(i+1)*50:-i*50])
                allFiles[i].write('\n')