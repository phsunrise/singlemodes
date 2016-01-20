import os
import sys
import yt
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, "/home/phsun/PyPSI")
import PyPSI as psi

fig, ax = plt.subplots()

i = 0
while os.path.isdir("DD%04d" % i):
    ds = yt.load("DD%04d/data%04d" % (i, i))
    all_data_level_0 = ds.covering_grid(level = 0, 
                  left_edge = [0, 0, 0], dims = ds.domain_dimensions)

    density = all_data_level_0["deposit", "all_cic"]
    #print density
    """
    density_ps = np.abs(np.fft.fftn(density))
    density_ps *= density_ps
    print density_ps[128, 128, :]

    density_ac = np.fft.ifftn(density_ps).real
    density_ac /= density_ac[0, 0, 0]
    print density_ac[0,0,:]

    dist = np.minimum(np.arange(256), np.arange(256, 0, -1))
    dist *= dist
    dist_3d = np.sqrt(dist[:, None, None] + dist[:, None] + dist)
    distances, _ = np.unique(dist_3d, return_inverse = True)
    values = np.bincount(_, weights=density_ac.ravel()) / np.bincount(_)

    plt.plot(distances[1:], values[1:])
    plt.savefig("spectrum.png")
    """

    power, k = psi.powerSpectrum(density, dims=(300., 300., 300.), bins = 256)

    ax.loglog(2*np.pi/k, power, label="%04d" % i)
    ax.set_xlabel("l (Mpc/h)")
    ax.set_ylabel("power")

    #from pprint import pprint
    #pprint(zip(k, power))

    i += 1
    
legend = plt.legend(loc = 'upper right', shadow = True)
fig.savefig("spectrum_cic.png")
