'''
Draws the slice plot along z axis (density)
'''
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import tables 

## first obtain the number of datasets
n = 0
maxval = 0
minval = 0
while os.path.isdir("DD%04d" % n):
    # read density file
    f = tables.open_file("DD%04d/density_PSI.h5" % n, mode = 'r')
    density = np.array(f.get_node("/density"))
    f.close()

    # sum over z axis
    z_proj = np.sum(density, axis=0, dtype=np.float64)
    
    if n == 0:
        maxval = z_proj.max()
        minval = z_proj.min()
    else:
        if z_proj.max() > maxval:
            maxval = z_proj.max()
        if z_proj.min() < minval:
            minval = z_proj.min()
    n += 1
if maxval == 0:
    sys.exit("Error: maximum value = 0!")
elif minval == 0: # takes care of minval = 0 problem
    minval = maxval / 1.e4

## create subplots, 4 columns
fig, ax_array = plt.subplots(ncols=4, nrows=int(np.ceil(1.*n/4)), \
                    figsize=(20,20))
fig.suptitle("z Projection", fontsize=30)
## prepare individual plots
fig1, ax1 = plt.subplots(figsize=(10,10))

## loop over density fields
for i in xrange(n):
    # read density file
    f = tables.open_file("DD%04d/density_PSI.h5" % i, mode = 'r')
    density = np.array(f.get_node("/density"))
    f.close()

    # sum over z axis
    z_proj = np.sum(density, axis=0, dtype=np.float64)

    # plotting on subplots
    icol = i % 4
    irow = i / 4
    ax = ax_array[irow, icol]
    im = ax.imshow(z_proj, interpolation='none', \
            norm=LogNorm(vmin=minval, vmax=maxval))
    ax.set_title("DD%04d" % i)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    # individual plots 
    im = ax1.imshow(z_proj, interpolation='none', \
            norm=LogNorm(vmin=minval, vmax=maxval))
    ax1.set_title("DD%04d: z Projection" % i)
    div = make_axes_locatable(ax1)
    cax = div.append_axes("right", size="15%", pad=0.05)
    cbar = plt.colorbar(im, cax=cax)
    fig1.savefig("data%04d_projection_z.png" % i)

## adjust subplot area and add colorbar
fig.tight_layout()
fig.subplots_adjust(right=0.95)
cax = fig.add_axes([0.96, 0.1, 0.02, 0.8])
fig.colorbar(im, cax=cax)
fig.savefig("projection_z.pdf")
fig.savefig("projection_z.png")
