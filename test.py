
# coding: utf-8

# In[18]:

import tables
import numpy

a = numpy.zeros((400, 400, 3))
for i in xrange(400):
    a[i, i, :] = numpy.sqrt(i)
    
f = tables.open_file("test1.h5", mode = 'w', title = "Test file")
f.create_array(f.root, "array", a)
f.close()


# In[19]:

f1 = tables.open_file("test1.h5", mode = 'r')

b = f1.get_node("/array")
print b[2,2,0]

f1.close()


# In[ ]:



