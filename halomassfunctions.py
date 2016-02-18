import sys
import numpy as np
from scipy.interpolate import interp1d


def delta_critical(hlink):
    ## calculates critical fluctuation
    #return 1.686
    return 0.65296 / hlink**3 - 1.

def GaussianWindow(k, V):
    R = (V / (2.*np.pi)**1.5) ** (1./3.)
    W = np.exp(- (k*R)**2 / 2.)
    return W

def tophat_xspace(k, V):
    R = (V / (4.*np.pi/3.)) ** (1./3.)
    W = 3*(np.sin(k*R)-k*R*np.cos(k*R)) / (k*R)**3
    return W

def tophat_kspace(k, V):
    R = (V / 6. / np.pi**2) ** (1./3.) # V=6*pi^2*R^3
    W = (abs(k * R) <= 1).astype(float)
    return W

def sigma2(powerSpec, V, kmin, kmax, points=500,\
           window='tophat_x'):
    P = interp1d(powerSpec[:,0], powerSpec[:,1], kind='linear', \
                bounds_error=False, fill_value=0.)
        # P is a function

    # the following are arrays
    lnk = np.linspace(np.log(kmin), np.log(kmax), points, \
            endpoint=False) + (np.log(kmax)-np.log(kmin))/points/2
    k = np.exp(lnk)

    if window=='gaus':
        W = GaussianWindow(k, V)
    elif window=='tophat_x':
        W = tophat_xspace(k, V)
    elif window=='tophat_k':
        W = tophat_kspace(k, V)

    integrand = k**3 * P(k) / (2.*np.pi**2) * np.abs(W)**2

    return np.sum(integrand) * (lnk[1]-lnk[0])


def PSMassFn(powerSpec, M, dM, rhomean, hlink=0.1, \
             kmin=1.e-3, kmax=1.e3, points=500, \
             window='tophat_x'):
    delta_c = delta_critical(hlink)
    sigma = np.sqrt(sigma2(powerSpec, M/rhomean, \
                        kmin, kmax, points, window))
    sigmam = np.sqrt(sigma2(powerSpec, (M-dM/2.)/rhomean, \
                        kmin, kmax, points, window))
    sigmap = np.sqrt(sigma2(powerSpec, (M+dM/2.)/rhomean, \
                        kmin, kmax, points, window))

    #print M, sigma, delta_c
    temp = np.sqrt(2./np.pi) * rhomean / M
    temp = temp * delta_c / sigma**2
    temp = temp * np.exp(-delta_c**2 / sigma**2 / 2.)
    temp = temp * np.abs((sigmap-sigmam) / dM)
    
    return temp

def STMassFn(powerSpec, M, dM, rhomean, hlink=0.1, \
             kmin=1.e-3, kmax=1.e3, points=500, window='tophat_x'):
    delta_c = delta_critical(hlink)
    sigma = np.sqrt(sigma2(powerSpec, M/rhomean, \
                        kmin, kmax, points, window))
    sigmam = np.sqrt(sigma2(powerSpec, (M-dM/2.)/rhomean, \
                        kmin, kmax, points, window))
    sigmap = np.sqrt(sigma2(powerSpec, (M+dM/2.)/rhomean, \
                        kmin, kmax, points, window))

    #print M, sigma, delta_c

    A = 0.3222
    a = 0.707
    p = 0.3
    
    temp = A * np.sqrt(2.*a/np.pi) * rhomean / M
    temp = temp * delta_c / sigma**2
    temp = temp * (1 + (sigma**2/a/delta_c**2)**p)
    temp = temp * np.exp(-a * delta_c**2 / sigma**2 / 2.)
    temp = temp * np.abs((sigmap-sigmam) / dM)
    
    return temp

#def JenkinsMassFn(powerSpec, M, dM, rhomean, hlink=0.1, \
#                  kmin=1.e-3, kmax=1.e3, points=500):
#    if hlink != 0.2:
#        print "linking length must be equal to 0.2!"
#        print "Exiting..."
#        sys.exit(1)
#
#    delta_c = delta_critical(hlink)
#    sigma = np.sqrt(sigma2(powerSpec, M/rhomean, \
#                        kmin, kmax, points))
#    if -np.log(sigma) < -1.2 or -np.log(sigma) > 1.05:
#        print "(Jenkins) Warning: sigma out of range"
#
#    sigmam = np.sqrt(sigma2(powerSpec, (M-dM/2.)/rhomean, \
#                        kmin, kmax, points))
#    sigmap = np.sqrt(sigma2(powerSpec, (M+dM/2.)/rhomean, \
#                        kmin, kmax, points))
#
#    temp = 0.315 * np.exp(- np.abs(-np.log(sigma)+0.61) ** 3.8)
#    temp = temp * rhomean / M / sigma
#    temp = temp * np.abs((sigmap-sigmam) / dM)
#    
#    return temp 
