import os
import sys
sys.path.insert(0, "/home/phsun/PyPSI")
import PyPSI as psi
from powerSpectrum import powerSpectrum
import matplotlib.pyplot as plt
import numpy as np
import tables
import yt

fig, ax = plt.subplots() 

i = 0
while os.path.isdir("DD%04d" % i):
    f = tables.open_file("DD%04d/density_PSI.h5" % i, mode = 'r')
    density = np.array(f.get_node("/density"))
    f.close()

    ## get redshift
    ds = yt.load("DD%04d/data%04d" % (i,i))
    z = ds.current_redshift

    ## calculate power spectrum
    l_list = np.logspace(np.log10(np.ceil(2.*300./256)), \
                    np.log10(280.), 100)
    powerSpec = powerSpectrum(density, \
            dims=(300., 300., 300.), l_list=l_list)

    ## plot spectrum
    ax.loglog(l_list, powerSpec*(1+z)**2, label = "%04d" % i)

    ## save to file
    np.savez_compressed("spectrum%04d.npz" % i, \
                    powerSpec=powerSpec, l=l_list)

    i += 1

ax.set_xlabel("l (Mpc/h)")
ax.set_ylabel("power*(1+z)^2")
legend = plt.legend(loc = 'upper right', shadow = True)
fig.savefig("spectrum_PSI.png")
