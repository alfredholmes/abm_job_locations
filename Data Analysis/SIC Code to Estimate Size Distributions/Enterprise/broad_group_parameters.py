import csv, scipy.optimize as op, scipy.stats as sps, numpy, math, random
import numpy as np

SIZES = ['0-4','5-9','10-19','20-49', '50-99','100-249','250+']
BROAD_GROUPS = [(0, 4), (5, 40), (41, 44), (45, 46), (46, 47), (47, 48), (49, 54), (55, 57), (58, 64), (64, 67), (68, 69), (69, 76), (77, 83), (84, 85), (85, 86), (86, 89), (90, 100)]


def main():
    data = get_data()
    output = []
    for id, d in data.items():
        r = op.minimize(ll, [0, 1], d, bounds=op.Bounds([-np.inf, 0], [np.inf, np.inf]))
        mean = r.x[0]
        sd   = r.x[1]
        output.append([id, mean, sd])
    with open('sic_broad_group_params.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for line in output:
            writer.writerow(line)



def get_data():
    data = {}
    with open('Data/2017_SIC_Size_Distributions.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            try:
                data[int(line['SIC'][:2])] = np.array([int(line[s]) for s in SIZES])
            except:
                pass
        r = {}
        for group in BROAD_GROUPS:
            totals = np.zeros(len(SIZES))
            for i in range(group[0], group[1]):
                if i in data:
                    totals += data[i]
            r[group] = totals

    return r


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
