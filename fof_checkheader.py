import sys

def checkheader(filename):
    f = open(filename, 'r')
    fh = open("/home/phsun/singlemodes/fof_header.txt", 'r')

    for i in xrange(4): # skip the first 4 lines 
        f.readline()

    for lineh in fh:
        line = f.readline()
        if line != lineh:
            print "This file:"
            print line
            print "Original header:"
            print lineh
            f.close()
            fh.close()

            return False
            
    f.close()
    fh.close()
    return True

if __name__ == "__main__":
    if checkheader(sys.argv[1]):
        print "same"
    else:
        print "not the same"
