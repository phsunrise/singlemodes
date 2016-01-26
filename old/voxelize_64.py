import os
import sys
import time
import numpy as np
import yt
import tables 
import itertools

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
    vel = np.zeros([int(np.prod(ds.domain_dimensions)), 3])
    vel[:,0] = all_data_level_0['all', 'particle_velocity_x']
    vel[:,1] = all_data_level_0['all', 'particle_velocity_y']
    vel[:,2] = all_data_level_0['all', 'particle_velocity_z']
    vel = vel.reshape(np.append(ds.domain_dimensions, 3)).astype(np.float64, \
        order='C')
    #print "pos: ", pos
    #print "vel: ", vel

    boxsize = 1.
    box = ((0.0, 0.0, 0.0), (boxsize, boxsize, boxsize))
    nx = ds.domain_dimensions[0]

    ## set voxelization options 
    order = 1
    tol = 1000
    subgridsize = 64
    grid_n = 256/subgridsize
    subgrid = (subgridsize, subgridsize, subgridsize)
    window = box

    ## chunk through Lagrangian patches
    density = np.zeros(ds.domain_dimensions)
    mtot = 0.0
    tstart = time.time()
    for i3, i2, i1 in itertools.product(*map(xrange, \
                    (grid_n, grid_n, grid_n))):
        fields = {'m': None}
        pos1 = pos[i3*subgridsize:(i3+1)*subgridsize, \
                   i2*subgridsize:(i2+1)*subgridsize, \
                   i1*subgridsize:(i1+1)*subgridsize, :]
        vel1 = vel[i3*subgridsize:(i3+1)*subgridsize, \
                   i2*subgridsize:(i2+1)*subgridsize, \
                   i1*subgridsize:(i1+1)*subgridsize, :]
        for pos1, vel1, mass, block, nblocks in psi.elementBlocksFromGrid(pos1, vel1, order=order, periodic=True):
            ## make periodic and voxelize it
            psi.voxelize(fields, pos1, vel1, mass, tol=tol, window=window, \
                grid=subgrid, periodic=True, box=box)
            
            ## bookkeeping
            #mtot += np.sum(mass)
            tend = time.time()
            sys.stdout.write("\rVoxelized block %d of %d. Time = %.1f s" % (block, nblocks, tend-tstart))
            sys.stdout.flush()
            
        #print '\nGlobal error = %.10e' % np.abs(np.sum(fields['m'])/mtot-1.0)

        #hlp.makeFigs(fields['m'], log=True,
        #   title='Example 4: Voxelizing elements loaded from a Gadget snapshot',
        #   figname="Example4")

        density[i3*subgridsize:(i3+1)*subgridsize, \
                i2*subgridsize:(i2+1)*subgridsize, \
                i1*subgridsize:(i1+1)*subgridsize] = fields['m']

    f = tables.open_file("density%04d_64.h5" % i, mode = 'w')
    f.create_array(f.root, "density", density)
    f.close()

    i += 1
