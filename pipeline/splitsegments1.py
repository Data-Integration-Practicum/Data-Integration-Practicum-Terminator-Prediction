import sys

with open(sys.argv[1]) as F:
    contents = F.readlines();
name = sys.argv[2]
with open(name + "/trimmedseqs.fa",'w') as out:
    allFiles = [open(name + "/segment1.fa",'w'),open(name + "/segment2.fa",'w'),open(name + "/segment3.fa",'w'),open(name + "/segment4.fa",'w'),open(name + "/segment5.fa",'w'),open(name + "/segment6.fa",'w'),open(name + "/segment7.fa",'w'),open(name + "/segment8.fa",'w')]
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