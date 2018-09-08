#This script performs MLE on the company data fitting a log normal distribution to 2012 ONS data for each local authority
# TODO: Evaluate accuracy of fitted distributions
import csv, scipy.optimize as op, scipy.stats as sps, numpy, math, random

SIZES = ['0-4','5-9','10-19','20-49', '50-99','100-249','250+']




def main():
    data = get_data()
    output = []
    for id, d in data.items():
        mean, sd = get_mean_sd(d)
        output.append([id, mean, sd])
        print(mean, sd)

    with open('output/2017_2_sic_enterprise_lognormal_params.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for line in output:
            writer.writerow(line)


def get_mean_sd(data):
    data = numpy.divide(data, numpy.sum(data))
    start = (0.24247032943908334, 1.732968915296001)
    r = op.minimize(ll, start, data, bounds=op.Bounds([-numpy.inf, 0], [numpy.inf, numpy.inf]))
    mean = r.x[0]
    sd   = r.x[1]

    if sps.lognorm.var(sd, scale=numpy.exp(mean)) < 200:
        return mean, sd
    else:
        return start


def get_data():
    data = {}
    with open('2017_enterprise_size_by_sic.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            data[line['SIC']] = [int(line[s]) for s in SIZES]
    return data


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
