import yt
import numpy as np
import sys

ds = yt.load(sys.argv[1])
ad = ds.all_data()
dims = ds.domain_dimensions

ids = np.array(ad['all', 'particle_index']).astype(np.int64,order='C')
#print ids[:256]
#print np.argsort(ids)[:256]

pos = ad['all', 'particle_position']
#print pos[:256]
pos = pos[np.argsort(ids),:]
#print pos[:256]
pos = pos.reshape(np.append(dims, 3)).astype(np.float64, order='C')

for i in xrange(dims[0]):
    print "i =", i, "(x,y,z) =", pos[0,0,i,:] 
