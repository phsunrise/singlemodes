'''
This script must be executed inside the FOF folder
'''

import glob
import os
import sys
import numpy as np
import operator
import matplotlib.pyplot as plt
from matplotlib import cm
from fof_checkheader import checkheader

if os.path.split(os.getcwd())[-1] != 'FOF':
    print "Must run inside FOF folder! Exiting..."
    sys.exit(1)
    
masses_dict = {} # dictionary to save masses for files
for filename in glob.glob("groups_*.dat"):
    ## first check header, which should be the same as in fof_header.txt
    if not checkheader(filename):
        print "Header for file, ", filename, " is different. Skipping..."
        continue

    masses = []

    with open(filename, 'r') as f:
        for line in f:
            line = line.split()
            if len(line) < 1:
                continue

            try:
                for i, elt in enumerate(line):
                    line[i] = float(elt)
            except ValueError:
                continue

            masses.append(line[5]) # halo mass is stored in column 6
    ## END file loop; file closed

    if len(masses) > 0:
        basename = filename.split('.')[0].split('_')[1]
        masses_dict[basename] = masses
        # update minmass and maxmass
        try:
            if minmass > min(masses):
                minmass = min(masses)
        except NameError:
            minmass = min(masses)
        try:
            if maxmass < max(masses):
                maxmass = max(masses)
        except NameError:
            maxmass = max(masses)
## END directory loop; all files read

try:
    #bins = np.logspace(np.log10(massmin), np.log10(massmax), 50)
    bins = np.linspace(minmass, maxmass, 31)
except NameError:
    print "no halos!"
    f = open("NoHalos", 'w')
    f.close()
    sys.exit(0)

bins_midpoint = (len(bins)-1) * [0.]
for i in range(len(bins)-1):
    bins_midpoint[i] = (bins[i]+bins[i+1]) * 0.5

hist_dict = {}
for basename, masses in masses_dict.iteritems():
    hist, bin_edges = np.histogram(masses, bins=bins)
    hist_dict[basename] = hist
    # update mincount and maxcount 
    try:
        if mincount > min(hist):
            mincount = min(hist)
    except NameError:
        mincount = min(hist)
    try:
        if maxcount < max(hist):
            maxcount = max(hist)
    except NameError:
        maxcount = max(hist)

# sort basenames
sorted_basenames = sorted(hist_dict.keys())
nhists = len(hist_dict)

# plot individual histograms
for i, basename in enumerate(sorted_basenames):
    plt.figure()
    plt.bar(bins_midpoint, hist_dict[basename], \
            width=bins_midpoint[1]-bins_midpoint[0], \
            log=True, color=cm.jet(1.*i/nhists))
    plt.xlabel("Halo mass (solar masses)")
    plt.ylabel("Number of halos")
    plt.ylim(0.5, maxcount*pow(10,0.1))
    plt.savefig("halo_mass_%s.png" % basename)

# plot all historgrams together
plt.figure()
for i, basename in enumerate(sorted_basenames):
    plt.bar(bins_midpoint, hist_dict[basename], \
            width=bins_midpoint[1]-bins_midpoint[0], \
            log=True, color=cm.jet(1.*i/nhists), \
            label=basename, alpha=0.8, zorder=nhists-i)

plt.xlabel("Halo mass (solar masses)")
plt.ylabel("Number of halos")
plt.ylim(0.5, maxcount*pow(10,0.1))
plt.legend(loc="upper right")
plt.savefig("halo_mass.png")
