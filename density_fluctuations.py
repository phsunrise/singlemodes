import os
import matplotlib.pyplot as plt
import numpy as np
import tables
import yt

fig, ax = plt.subplots() 

i = 0
x = []
y = []
while os.path.isdir("DD%04d" % i):
    f = tables.open_file("DD%04d/density_PSI.h5" % i, mode = 'r')
    density = np.array(f.get_node("/density"))
    f.close()

    x.append(i)
    delta = density / np.mean(density) - 1
    y.append(np.max(abs(delta)))
    
    i += 1

plt.semilogy(x, y, 'ro')
for i,j in zip(x,y):
    plt.annotate("%.2e" % j, xy=(i, j), \
                xytext=(2,10), textcoords="offset points", \
                fontsize=10)
plt.xticks(x, x)
print plt.margins()
plt.margins(x=0.1)
plt.xlabel("dataset")
plt.ylabel("max abs(delta_rho)/rho_0")
plt.savefig("max_delta_rho.png")

np.savez_compressed("max_delta_rho.npz", delta_rho=y)
