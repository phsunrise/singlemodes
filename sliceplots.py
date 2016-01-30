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

## first obtain the number of datasets and max & min values
n = 0
maxval = 0
minval = 0
while os.path.isdir("DD%04d" % n):
    # read density file
    f = tables.open_file("DD%04d/density_PSI.h5" % n, mode = 'r')
    density = np.array(f.get_node("/density"))
    f.close()
    z_dim = density.shape[0]
    z_slice = density[int(z_dim/2),:,:]
    
    if n == 0:
        maxval = z_slice.max()
        minval = z_slice.min()
    else:
        if z_slice.max() > maxval:
            maxval = z_slice.max()
        if z_slice.min() < minval:
            minval = z_slice.min()
    n += 1
if maxval == 0:
    sys.exit("Error: maximum value = 0!")
elif minval == 0: # takes care of minval = 0 problem
    minval = maxval / 1.e4

## create subplots, 4 columns
fig, ax_array = plt.subplots(ncols=4, nrows=int(np.ceil(1.*n/4)), \
                    figsize=(20,20))
fig.suptitle("z Slice", fontsize=30)
## prepare individual plots
fig1, ax1 = plt.subplots(figsize=(10,10))

for i in xrange(n):
    # read density file
    f = tables.open_file("DD%04d/density_PSI.h5" % i, mode = 'r')
    density = np.array(f.get_node("/density"))
    f.close()

    x_dim = density.shape[2]
    y_dim = density.shape[1]
    z_dim = density.shape[0]

    # save z_slice
    z_slice = density[int(z_dim/2),:,:]

    # plotting
    icol = i % 4
    irow = i / 4
    ax = ax_array[irow, icol]
    im = ax.imshow(z_slice, interpolation='none', \
            norm=LogNorm(vmin=minval, vmax=maxval))
    ax.set_title("DD%04d" % i)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    # individual plots 
    im = ax1.imshow(z_slice, interpolation='none', \
            norm=LogNorm(vmin=minval, vmax=maxval))
    ax1.set_title("DD%04d: z Slice" % i)
    div = make_axes_locatable(ax1)
    cax = div.append_axes("right", size="15%", pad=0.05)
    cbar = plt.colorbar(im, cax=cax)
    fig1.savefig("data%04d_slice_z.png" % i)


fig.tight_layout()
fig.subplots_adjust(right=0.95)
cax = fig.add_axes([0.96, 0.1, 0.02, 0.8])
fig.colorbar(im, cax=cax)
fig.savefig("slice_z.pdf")
fig.savefig("slice_z.png")
