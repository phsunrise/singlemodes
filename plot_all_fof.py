import os

dir256 = "/scratch/users/phsun/256"
os.chdir(dir256)

i = 1
while os.path.isdir("256_%d" % i):
    print "current directory: ", i
    if os.path.isdir("256_%d/FOF" % i):
        os.chdir("256_%d/FOF" % i)
        os.system("python $repo/halomass_hist.py")
    else:
        print "no FOF"

    os.chdir(dir256)
    i += 1
