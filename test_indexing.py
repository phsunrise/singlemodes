import numpy as np
import itertools

ax = np.linspace(1.,4.,4)
grid = np.meshgrid(ax,ax,ax,indexing='ij')

for x,y,z in itertools.product(*map(xrange, (4,4,4))):
    print x+1,y+1,z+1,grid[0][x,y,z],grid[1][x,y,z],grid[2][x,y,z]

grid = np.array([grid[2],grid[1],grid[0]]).reshape(3,64)
print grid
