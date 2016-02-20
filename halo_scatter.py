import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(20,20))
ax = fig.add_subplot(111, projection='3d')

data = np.genfromtxt("FOFhalos_link_0.3.txt", skip_header=3,\
                     usecols=(1,6,7,8))
masses = data[:,0]
cmx = data[:,1]
cmy = data[:,2]
cmz = data[:,3]

minmass = min(masses)
maxmass = max(masses)

mask = (np.log(masses/minmass)/np.log(maxmass/minmass) > 0.9)

colors = (np.log(masses/minmass))/(np.log(maxmass/minmass))
ax.scatter(cmx[mask], cmy[mask], cmz[mask], c=colors[mask], cmap='jet')

plt.savefig("halo_scatter.png")


plt.figure(figsize=(20,20))
mask = np.logical_and(cmz>0.48, cmz<0.52)
plt.scatter(cmx[mask], cmy[mask], c=colors[mask], cmap='jet')
plt.savefig("halo_scatter_4.png")
