import yt
import numpy as np
import sys

ds = yt.load(sys.argv[1])
ad = ds.all_data()
dims = ds.domain_dimensions # dimensions
length = np.prod(dims) # flattened array length
print dims, length

#all_data_level_0 = ds.covering_grid(level = 0, \
#    left_edge = [0,0,0], dims=dims)

ids_old = np.array(ad['all', 'particle_index']).astype(int,order='C')
#ids_old = np.array(range(length))
subdims = dims/4
sublen = length/64 # length of subgrid (flattened)
ids = np.zeros(dims).astype(int,order='C')
for i in range(64):
    if i == 0:
        temp = ids_old[0:sublen].reshape(subdims)
    else:
        temp = ids_old[sublen*(64-i):sublen*(64-i+1)].reshape(subdims)
    
    xl = (i % 4) * subdims[0]
    xh = ((i % 4) + 1) * subdims[0]
    yl = ((i / 4) % 4) * subdims[0]
    yh = (((i / 4) % 4) + 1) * subdims[0]
    zl = (i / 16) * subdims[0]
    zh = ((i / 16) + 1) * subdims[0]
    ids[zl:zh, yl:yh, xl:xh] = temp

    #if i == 1:
    #    print "temp:\n", temp
    #    print xl,xh,yl,yh,zl,zh
#print ids[0,:,:]
ids = ids.reshape(length).astype(int,order='C')
#print ids[0:32]


pos = ad['all', 'particle_position']
#print pos[512:1024,:].reshape(8,8,8,3)
pos = pos[ids,:]
pos = pos.reshape(np.append(dims, 3)).astype(np.float64, order='C')

for i in xrange(dims[0]):
    print "i =", i, "(x,y,z) =", pos[0,i,0,:] 
