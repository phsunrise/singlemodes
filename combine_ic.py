import h5py
import numpy as np

## read dimensions from file
f = h5py.File("ParticleDisplacements_x",'r')
dims = f['ParticleDisplacements_x'].shape[1:]
print "dimensions =", dims
f.close()

length = np.prod(dims) ## length of the array for each axis
print length

##### calculate and combine positions
## first create the grid
ax = np.linspace(0.,1.,dims[0],endpoint=False) + 0.5/dims[0]
grid = np.meshgrid(ax,ax,ax, indexing='ij') # the indexing here is important!
print grid[2-0][0,0,:]

## read the displacements and calculate the positions
filenames = ["ParticleDisplacements_x", \
             "ParticleDisplacements_y", \
             "ParticleDisplacements_z"]
pos = np.zeros(np.append(3, dims))
for i, filename in enumerate(filenames):
    fin = h5py.File(filename, 'r')
    pos[i,:,:,:] = grid[2-i]+fin[filename] # add displacements to grid
    # the "2-i" is because of the 'ij' indexing above
    fin.close()

pos = np.array(pos).reshape((3,length)).astype(np.float64) # flatten the pos array
fout = h5py.File("ParticlePositions", 'w')
pos = fout.create_dataset("ParticlePositions", data=pos)
pos.attrs.create("Component_Rank", (3,))
pos.attrs.create("Component_Size", (length,))
pos.attrs.create("Dimensions", (length,))
pos.attrs.create("Rank", (1,))
pos.attrs.create("TopGridDims", (-99999,-99999,-99999))
pos.attrs.create("TopGridEnd", (-100000,-100000,-100000))
pos.attrs.create("TopGridStart", (0,0,0))
fout.close()

## combine velocities
fout = h5py.File("ParticleVelocities", 'w')
vel = fout.create_dataset("ParticleVelocities", \
                       (3, length), np.float64)

filenames = ["ParticleVelocities_x", \
             "ParticleVelocities_y", \
             "ParticleVelocities_z"]
for i, filename in enumerate(filenames):
    fin = h5py.File(filename, 'r')
    vel[i,:] = np.array(fin[filename]).reshape((1,length))
    fin.close()

vel.attrs.create("Component_Rank", (3,))
vel.attrs.create("Component_Size", (length,))
vel.attrs.create("Dimensions", (length,))
vel.attrs.create("Rank", (1,))
vel.attrs.create("TopGridDims", (-99999,-99999,-99999))
vel.attrs.create("TopGridEnd", (-100000,-100000,-100000))
vel.attrs.create("TopGridStart", (0,0,0)) 
fout.close()
