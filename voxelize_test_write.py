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

## using yt to load enzo data
ds = yt.load("DD0000/data0000")

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

f = tables.open_file("test.h5", mode = 'w')
f.create_array(f.root, "pos", pos)
f.create_array(f.root, "vel", vel)
f.close()
