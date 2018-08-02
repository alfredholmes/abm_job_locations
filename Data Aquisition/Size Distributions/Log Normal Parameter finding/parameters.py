#This script performs MLE on the company data fitting a log normal distribution to 2012 ONS data for each local authority
# TODO: Evaluate accuracy of fitted distributions
import csv, scipy.optimize as op, scipy.stats as sps, numpy, math, random

SIZES = ['0-4','5-9','10-19','20-49', '50-99','100-249','250+']

def main():
    data = get_data()
    for id,d in data.items():
        r = op.minimize(ll, [0, 1], d, bounds=op.Bounds([-10, 0], [10, 10]))
        mean = r.x[0]
        sd   = r.x[1]

        print(mean, sd)

        total = 0
        for v in d:
            total += v
        bands = [0] * 7
        for i in range(total):
            k = random.lognormvariate(mean, sd)
            if k < 4:
                bands[0] +=1
                continue
            if k < 9:
                bands[1] +=1
                continue
            if k < 19:
                bands[2] +=1
                continue
            if k < 49:
                bands[3] +=1
                continue
            if k < 99:
                bands[4] +=1
                continue
            if k < 249:
                bands[5] +=1
                continue
            bands[6] += 1

        print(bands)
        print(d)


def get_data():
    data = {}
    with open('la_company_size_dist_by_id.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            data[line['la']] = [int(line[s]) for s in SIZES]
    return data


def ll(param, arr):
    endpoints = [0,4,9,19,49,99,249,numpy.inf]
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
