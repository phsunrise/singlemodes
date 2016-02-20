import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from fof_checkheader import checkheader
from halomassfunctions import PSMassFn, STMassFn

plt.figure(figsize=(20,20))

#fof_file = "FOF/groups_00312.dat"
#if not checkheader(fof_file):
#    print "Header for file, ", fof_file, " is different. Exiting..."
#    sys.exit(0)
#
#masses = []
#
#with open(fof_file, 'r') as f:
#    for line in f:
#        line = line.split()
#        if len(line) < 1:
#            continue
#
#        try:
#            for i, elt in enumerate(line):
#                line[i] = float(elt)
#        except ValueError:
#            continue
#
#        masses.append(line[5]) # halo mass is stored in column 6
### END file loop; file closed

data = np.genfromtxt("FOFhalos_link_0.2.txt", skip_header=3)
masses = data[:,1]

minmass = min(masses)
maxmass = max(masses)

bins = np.logspace(np.log10(minmass), np.log10(maxmass), 31)
binwidths = bins[1:] - bins[:-1]
# calculate dn/dM
hist = np.histogram(masses, bins=bins)[0]
for low, width, counts in zip(bins[:-1], binwidths, hist):
    print low, width, "counts=", counts, counts/width
hist = hist / binwidths / 300.**3

plt.semilogy(np.log10(bins[:-1]), hist, 'bo--', \
             label='counting')
plt.xlabel("log10(M/Msun)")
plt.ylabel("dn/dM")

## read power spectrum and use PS mass function
#f = np.load("spectrum0000.npz")
#powerSpec = np.zeros([len(f['l']), 2])
#powerSpec[:,0] = 2.*np.pi/f['l']
#powerSpec[:,1] = f['powerSpec']/101.**2
#f.close()

# read power spectrum file
powerSpec = np.genfromtxt("input_powerspec.txt", comments='#', usecols=(0,5))
# normalize power spectrum
powerSpec[:,1] = powerSpec[:,1] * (256)**3 * (2*np.pi)**3

# arrays to store mass functions
PS_t = []
ST_t = []
alphas = [0.3, 0.330, 0.37, 0.4, 0.5, 0.6]
for alpha in alphas:
    PS_t.append(np.zeros_like(binwidths))
    ST_t.append(np.zeros_like(binwidths))

rhomean = 3.965765e11   # unit: Msun/(Mpc/h)^3
kmin = min(powerSpec[:,0])
kmax = max(powerSpec[:,0])
kmin = 2*np.pi/300.
kmax = 2*np.pi/1.
print "kmin=", kmin, "kmax=", kmax
points = 500

# iterate
for i, M in enumerate(bins[:-1]):
    dM = bins[i+1]-bins[i]
    for i_alpha, alpha in enumerate(alphas):
        PS_t[i_alpha][i] = PSMassFn(powerSpec, M, dM,
                    rhomean=rhomean, hlink=0.2,
                    kmin=kmin, kmax=kmax, points=points,
                    window=('tukey_k', alpha))
        ST_t[i_alpha][i] = STMassFn(powerSpec, M, dM,
                    rhomean=rhomean, hlink=0.2,
                    kmin=kmin, kmax=kmax, points=points,
                    window=('tukey_k',alpha))

for i_alpha, alpha in enumerate(alphas):
    plt.semilogy(np.log10(bins[:-1]), PS_t[i_alpha], \
                 label='P-S tukey %.2f' % alpha)
    plt.semilogy(np.log10(bins[:-1]), ST_t[i_alpha], \
                 label='S-T tukey %.2f' % alpha)
plt.ylim(min(hist)/10., max(hist)*10.)

plt.legend(loc='lower left')
plt.savefig("halo_mass_tukey.png")
