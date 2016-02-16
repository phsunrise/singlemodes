"""
This script will be executed under the directory "/scratch/users/phsun/256",
which contains subdirectories "256_1", "256_2", etc.
"""

import os
import glob
import numpy as np

os.chdir("/scratch/users/phsun/256")
fout = open("parameters.txt", "w")
param_dict = {"dataset":0, "lspike1":1, "lspike2":2, "lspike3":3, \
              "force_pnorm":4, "delta_l":5, "FOF":6, "init_delta_rho":7, \
              "final_delta_rho":8}
    # column numbers for parameters

# write header
params = len(param_dict) * [""]
for key, column in param_dict.iteritems():
    params[column] = '{:>16}'.format(key)
fout.write(''.join(params))
fout.write('\n')

a = len(param_dict) * [""] # list to save parameters for each file

i = 1
while os.path.isdir("256_%d" % i):
    f = open("256_%d/deltafunctions_ics_test.conf" % i, "r")
    a[param_dict["dataset"]] = '{:>16}'.format(str(i))

    for line in f:
        line = line.split()
        if len(line) < 3:
            continue
        
        line[2] = '{:>16}'.format(line[2])
        if line[0] == 'lspike1':
            a[param_dict["lspike1"]] = line[2]
        elif line[0] == 'lspike2':
            a[param_dict["lspike2"]] = line[2]
        elif line[0] == 'lspike3':
            a[param_dict["lspike3"]] = line[2]
        elif line[0] == 'force_pnorm':
            line[2] = '%.1e' % float(line[2])
            line[2] = '{:>16}'.format(line[2]) 
            a[param_dict["force_pnorm"]] = line[2]
        elif line[0] == 'delta_l_over_l':
            a[param_dict["delta_l"]] = line[2]
    # END read parameter file
    f.close()

    # halo file exists?
    if len(glob.glob("256_%d/FOFhalos_link_*.txt" % i)) > 0:
        a[param_dict["FOF"]] = ' ' * 15 + 'Y'
    else:
        a[param_dict["FOF"]] = ' ' * 15 + 'N'
    
    # density fluctuations
    f = np.load("256_%d/max_delta_rho.npz" % i)
    delta_rho = f["delta_rho"]
    a[param_dict["init_delta_rho"]]='{:>16}'.format("%.3f" % delta_rho[1])
    a[param_dict["final_delta_rho"]]='{:>16}'.format("%.3f" % delta_rho[-1])
    f.close()

    fout.write(''.join(a))
    fout.write('\n')

    i += 1

fout.close()
