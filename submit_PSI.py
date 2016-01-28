'''
This script must be run under a directory that contains the "DDXXXX"
enzo data folders. It will:
1. loop over all "DDXXXX" folders
2. create a .sbatch script under each folder, which
   will run $HOME/singlemodes/voxelize.py with the argument
   that points to the dataset.
3. submit the .sbatch script under the folder
'''

import sys
import os

currentpath = os.getcwd()

i = 0
while os.path.isdir("DD%04d" % i):
    os.chdir("DD%04d" % i)
    print "current path: ", os.getcwd()

    # write the batch script file
    f = open("submit_PSI_%04d.sbatch" % i, 'w')
    
    f.write("#!/bin/bash\n")
    f.write("\n")
    f.write("#SBATCH --job-name=PSI%04d\n" % i)
    f.write("#SBATCH --output=sme.out\n")
    f.write("#SBATCH --error=sme.err\n")
    f.write("#SBATCH --time=1:00:00\n")
    f.write("#SBATCH --qos=iric\n")
    f.write("#SBATCH --mem=60000\n")
    f.write("#SBATCH --partition=iric\n")
    f.write("\n")
    f.write("python $HOME/singlemodes/voxelize.py data%04d\n" % i)

    f.close()

    # run the batch script
    os.system("sbatch submit_PSI_%04d.sbatch" % i)

    # return to original path
    os.chdir(currentpath)

    i += 1
