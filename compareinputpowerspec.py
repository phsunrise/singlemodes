import os
import sys
sys.path.insert(0, "/home/phsun/PyPSI")
import PyPSI as psi
import matplotlib.pyplot as plt
import numpy as np
import tables

ic_data = np.genfromtxt("input_powerspec.txt", comments='#', usecols=(0,5), names=['k', 'power'])

f = tables.open_file("density0000.h5", mode='r')
density = np.array(f.get_node("/density"))
f.close()

power, k = psi.powerSpectrum(density, \
        dims=(300., 300., 300.), bins = 256)
l = 2*np.pi/k

fig, ax = plt.subplots() 
ax.loglog(l, power, label="enzo0000")
ax.loglog(2*np.pi/ic_data['k'], ic_data['power'], label="music_input")
ax.set_xlabel("l (Mpc/h)")
ax.set_ylabel("power")
legend = plt.legend(loc = 'upper right', shadow = True)
fig.savefig("spectrum_init.png")
