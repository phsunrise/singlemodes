import numpy as np
import matplotlib.pyplot as plt

size = 100 
boxlen = 300.
M = 20 
dx = boxlen / size
x = np.linspace(0., boxlen, size, endpoint=False)
k = np.arange(size) *2*np.pi / boxlen
fx = np.zeros(size).astype(np.float64)
fx[:M*2] = 1.
fk = np.zeros(size).astype(np.float64)
for i in xrange(size):
    if i == 0:
        fk[i] = (2*M+1)*1./size
    else:
        fk[i] = np.sin(k[i]/2*dx*(2*M+1))/size/np.sin(k[i]/2*dx)
fk_fft = np.fft.fft(fx) / size 
for i in xrange(size/2):
    print fk[i]**2/abs(fk_fft[i])**2

plt.loglog(k[:size/2], fk[:size/2]**2, "ro")
plt.loglog(k[:size/2], np.abs(fk_fft[:size/2])**2, "bo")
plt.savefig("test_fourier.png")
