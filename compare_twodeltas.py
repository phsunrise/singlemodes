import numpy as np
import os

os.chdir("/scratch/users/phsun/256")
ds1 = 22 
ds2 = 32 
peak = 10.
delta = 0.1
fout = open("ds_%dvs%d_l_%.1f_deltal_%.1f.txt" % (ds1, \
                                    ds2, peak, delta), 'w')

i = 0
while os.path.isfile("256_%d/spectrum%04d.npz" % (ds1, i)):
    f1 = np.load("256_%d/spectrum%04d.npz" % (ds1, i))
    f2 = np.load("256_%d/spectrum%04d.npz" % (ds2, i))
    
    print "spectrum%04d" % i
    fout.write("spectrum%04d\n" % i)
    for l, p1, p2 in zip(f1['l'], f1['powerSpec'], f2['powerSpec']):
        if abs(l-peak)/peak < delta/2:
            diff = abs((p1-p2)/(p1+p2)*200.)
            print "%2.3f, %3.6f, %3.6f, difference=%3.2f%%" % (l, p1, \
                                                                p2, diff)
            fout.write("%2.3f, %3.6f, %3.6f, difference=%3.2f%%\n" % (l, \
                                                                p1, p2, diff))

    f1.close()
    f2.close()
    print '\n'
    fout.write("\n")
    i += 1

fout.close()
