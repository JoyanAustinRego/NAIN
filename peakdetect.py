import sys
from numpy import NaN, Inf, arange, isscalar, asarray, array


def peakdet(v, delta, x=None):
    maxtab = []
    mintab = []

    if x is None:
        x = arange(len(v))

    v = asarray(v)

    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')

    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')

    if delta <= 0:
        sys.exit('Input argument delta must be positive')

    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN

    lookformax = True

    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]

        if lookformax:
            if this < mx - delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn + delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return array(maxtab), array(mintab)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from math import sin, pi, cos
    series = [0,1,2,3,4,5,4,3,4,5,4,3,2,1,0,-1,-2,-3,-4,-5,-4,-3,-4,-5,-4,-3,-2,-1,0] # [sin(2*pi*500*i/8000.0)*cos(2*pi*100*i/8000.0) for i in range(100)]
    maxtab, mintab = peakdet(series,.1)
    plt.plot(series)
    plt.scatter(array(maxtab)[:, 0], array(maxtab)[:, 1], color='blue')
    plt.scatter(array(mintab)[:, 0], array(mintab)[:, 1], color='red')
    plt.show()

