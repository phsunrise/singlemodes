'''
This script compares the power spectrum in DD0000 with
that generated by MUSIC
'''

import os
import sys
sys.path.insert(0, "/home/phsun/PyPSI")
from powerSpectrum import powerSpectrum
import matplotlib.pyplot as plt
import numpy as np
import tables

ic_data = np.genfromtxt("input_powerspec.txt", comments='#', usecols=(0,5), names=['k', 'power'])

f = tables.open_file("DD0000/density_PSI.h5", mode='r')
density = np.array(f.get_node("/density"))
f.close()

l_list = np.logspace(np.log10(np.ceil(2.*300./256)), np.log10(300.), 100)
powerSpec = powerSpectrum(density, \
        dims=(300., 300., 300.), l_list=l_list)
print powerSpec

fig, ax = plt.subplots() 
ax.loglog(l_list, powerSpec, label="enzo0000")
ax.loglog(2*np.pi/ic_data['k'], ic_data['power']*256**3*(2*np.pi)**3, label="music_input")
ax.set_xlim(1.e0, 1.e3)
ax.set_ylim(1.e-4, 1.e10)
ax.set_xlabel("l (Mpc/h)")
ax.set_ylabel("power")
legend = plt.legend(loc = 'upper right', shadow = True)
fig.savefig("spectrum_init.png")
