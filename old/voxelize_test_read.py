import os
import sys
import time
import numpy as np
import yt
import tables 

sys.path.insert(0, "/home/phsun/PyPSI")
import PyPSI as psi
import PyPSIExampleHelpers as hlp

'''
    Voxelizing elements
    
    We load our grid of positions and velocities from a file
    rather than generating them ourselves.
    
    We also use the 'periodic' options in PyPSI.elementBlocksFromGrid() and PyPSI.voxelize(),
    along with 'box', to indicate that PSI should create appropriate ghost elements and wrap
    the domain.
    
'''

f = tables.open_file(sys.argv[1], mode = 'r')
pos = np.array(f.get_node("/pos"))
vel = np.array(f.get_node("/vel"))
f.close()

boxsize = 1.
box = ((0.0, 0.0, 0.0), (boxsize, boxsize, boxsize))

## set voxelization options 
order = 1
tol = 1000
gridsize = 256
grid = (gridsize, gridsize, gridsize)
window = box
fields = {'m': None}

## chunk through Lagrangian patches
mtot = 0.0
tstart = time.time()
for pos, vel, mass, block, nblocks in psi.elementBlocksFromGrid(pos, vel, order=order, periodic=True):
    ## make periodic and voxelize it
    psi.voxelize(fields, pos, vel, mass, tol=tol, window=window, \
        grid=grid, periodic=True, box=box)
    
    ## bookkeeping
    mtot += np.sum(mass)
    tend = time.time()
    sys.stdout.write("\rVoxelized block %d of %d. Time = %.1f s" % (block, nblocks, tend-tstart))
    sys.stdout.flush()
    
print '\nGlobal error = %.10e' % np.abs(np.sum(fields['m'])/mtot-1.0)


