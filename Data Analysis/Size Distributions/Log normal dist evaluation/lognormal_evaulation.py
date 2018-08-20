import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import csv, scipy.optimize as op, scipy.stats as sps
import random, numpy

UK_SIZE_DIST = [2087030, 299710, 151140, 80575, 25915, 14615, 9825]
CROP_DIST = [124155, 11480, 2735, 955, 275, 120, 60]




def main():
    plt.hist([1, 5, 10, 50, 100, 250, 999], weights=CROP_DIST, bins=[0, 5, 10, 50, 100, 250, 1000], alpha=0.5, facecolor='green')
    #plt.hist([1, 2, 1], bins=[0, 1, 2, 3)
    total_companies = 0
    for n in CROP_DIST:
        total_companies += n

    mean, sd = get_ln_params(CROP_DIST)
    print(mean, sd)
    sizes = []
    for _ in range(total_companies):
        sizes.append(random.lognormvariate(mean, sd))

    plt.hist(sizes, bins=[0, 5, 10, 50, 100, 250, 1000], alpha=0.5, facecolor='blue')

    plt.show()

def get_ln_params(size_data):
    #r = op.minimize(ll, [0, 1], size_data, bounds=op.Bounds([-10, 0], [10, 10]))
    r = op.minimize(ll, [0, 1], size_data)
    mean = r.x[0]
    sd   = r.x[1]

    return mean, sd

def ll(param, arr):
    endpoints = [0,5,10,20,50,100,250,numpy.inf]
    s = 0
    for i,x in enumerate(arr):
        #print(x)
        a = (numpy.log(endpoints[i+1]) - param[0]) / param[1]
        b = (numpy.log(endpoints[i  ]) - param[0]) / param[1]
        if b != -numpy.inf and a != numpy.inf:
            s += x * numpy.log(sps.norm.cdf(a) - sps.norm.cdf(b))
        elif b == -numpy.inf:
            s+= x * numpy.log(sps.norm.cdf(a))
        else:
            s+= x * numpy.log(1 - sps.norm.cdf(b))
    return -s #return negative such that minimise methods can be used

if __name__ == '__main__':
    main()
