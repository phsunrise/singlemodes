import numpy as np
import yt

ds = yt.load("DD0000/data0000")
all_data_level_0 = ds.covering_grid(level = 0, \
            left_edge = [0, 0, 0], dims = ds.domain_dimensions)
ids = np.array(all_data_level_0['all', \
    'particle_index']).reshape(ds.domain_dimensions).astype(int, \
    order='C')

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

for i in xrange(256):
    print ids[0,i,0], pos[0,i,0,:]
