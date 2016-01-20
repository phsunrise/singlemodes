import os
import sys
sys.path.insert(0, "/home/phsun/PyPSI")
import PyPSI as psi
import matplotlib.pyplot as plt
import numpy as np
import tables 

fig, ax = plt.subplots() 

f = tables.open_file("density0000.h5", mode = 'r')
density = np.array(f.get_node("/density"))
f.close()

## calculate power spectrum
power, k = psi.powerSpectrum(density, \
        dims=(300., 300., 300.), bins = 256)
l = 2*np.pi/k

## plot spectrum
ax.loglog(l, power, label = "0000")

## save to file
np.savez_compressed("spectrum0000.npz", power=power, l=l)

ax.set_xlabel("l (Mpc/h)")
ax.set_ylabel("power")
legend = plt.legend(loc = 'upper right', shadow = True)
fig.savefig("spectrum_PSI_0000.png")
