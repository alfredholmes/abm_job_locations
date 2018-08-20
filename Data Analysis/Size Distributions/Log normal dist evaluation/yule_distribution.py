import scipy.integrate as integrate
from scipy.special import beta
import numpy, random, matplotlib.pyplot as plt

UK_SIZE_DIST = [2087030, 299710, 151140, 80575, 25915, 14615, 9825]
import csv, scipy.optimize as op

def main():
    r = get_yule_param(UK_SIZE_DIST)[0]
    row = r[0]

    print(row)



    sizes = []
    for _ in range(10000):
        r = random.random()
        i = 0
        while r < cdf(i, row):
            i += 1
            print(i)
        sizes.append(i)
        print(_, i)

    plt.hist(sizes, 50)
    plt.show()

def get_yule_param(data):
    r = op.minimize(ll, [1, 1], data, bounds = op.Bounds([0, -numpy.inf], [numpy.inf, numpy.inf]))
    return r.x

def ll(params, data):
    #endpoints = [0,5,10,20,50,100,250,numpy.inf]
    endpoints = [0,5,10,20,50,100,250,1000]
    s = 0
    for i, x in enumerate(UK_SIZE_DIST):
        print(i, params)
        if endpoints[i] != 0:
            if endpoints[i + 1] != numpy.inf:
                s += x * (cdf(endpoints[i + 1], params[0]) - cdf(endpoints[i], params[0]))
            else:
                s += x * (1 - cdf(endpoints[i], params[0]))
        if endpoints[i] == 0:
            s += x * cdf(endpoints[i + 1], params[0])

    #print(s)

    return -s * params[1]


def cdf(k, row):
    return integrate.quad(lambda s: beta(s, row + 1), 0, k)[0]




if __name__ == '__main__':
    main()
