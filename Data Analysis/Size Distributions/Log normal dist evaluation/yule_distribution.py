import scipy.integrate as integrate
from scipy.special import beta
import numpy, random, matplotlib.pyplot as plt

UK_SIZE_DIST = [2087030, 299710, 151140, 80575, 25915, 14615, 9825]
import csv, scipy.optimize as op

def main():
    for i in range(100):
        print(cdf(i, 1))

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


def pdf(x, row):
    return beta(x, row + 1)

def cdf(x, row):
    total = 0
    i = 0
    while i <= x:
        total += pdf(x, row)

        i += 1

    return total




if __name__ == '__main__':
    main()
