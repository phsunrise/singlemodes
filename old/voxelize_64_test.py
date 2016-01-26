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

i = 0
subgridsize = 64 
while os.path.isdir("DD%04d" % i):
    ## using yt to load enzo data
    ds = yt.load("DD%04d/data%04d" % (i, i))

    ## use a covering grid to include all data
    all_data_level_0 = ds.covering_grid(level = 0, \
                left_edge = [0, 0, 0], dims = ds.domain_dimensions)
    ids = np.array(all_data_level_0['all', 'particle_index']).astype(int, \
            order='C')
    #print ids
    pos = np.zeros([int(np.prod(ds.domain_dimensions)), 3])
    pos[:,0] = all_data_level_0['all', 'particle_position_x']
    pos[:,1] = all_data_level_0['all', 'particle_position_y']
    pos[:,2] = all_data_level_0['all', 'particle_position_z']
    pos = pos.reshape(np.append(ds.domain_dimensions, 3)).astype(np.float64, \
        order='C')
    pos = pos[:64,:64,:64,:]
    vel = np.zeros([int(np.prod(ds.domain_dimensions)), 3])
    vel[:,0] = all_data_level_0['all', 'particle_velocity_x']
    vel[:,1] = all_data_level_0['all', 'particle_velocity_y']
    vel[:,2] = all_data_level_0['all', 'particle_velocity_z']
    vel = vel.reshape(np.append(ds.domain_dimensions, 3)).astype(np.float64, \
        order='C')
    vel = vel[:64,:64,:64,:]
    #print "pos: ", pos
    #print "vel: ", vel

    boxsize = 1.
    box = ((0.0, 0.0, 0.0), (boxsize, boxsize, boxsize))
    nx = ds.domain_dimensions[0]

    ## set voxelization options 
    order = 1
    tol = 1000
    subgrid = (subgridsize, subgridsize, subgridsize)
    window = box
    fields = {'m': None}

    ## chunk through Lagrangian patches
    mtot = 0.0
    tstart = time.time()
    for pos, vel, mass, block, nblocks in psi.elementBlocksFromGrid(pos, vel, order=order, periodic=True):
        ## make periodic and voxelize it
        psi.voxelize(fields, pos, vel, mass, tol=tol, window=window, \
            grid=subgrid, periodic=True, box=box)
        
        ## bookkeeping
        mtot += np.sum(mass)
        tend = time.time()
        sys.stdout.write("\rVoxelized block %d of %d. Time = %.1f s" % (block, nblocks, tend-tstart))
        sys.stdout.flush()
        
    print '\nGlobal error = %.10e' % np.abs(np.sum(fields['m'])/mtot-1.0)

    # save density data to file
    f = tables.open_file("density%04d_64.h5" % i, mode = 'w')
    f.create_array(f.root, "density", fields['m'])
    f.close()

    i += 1
