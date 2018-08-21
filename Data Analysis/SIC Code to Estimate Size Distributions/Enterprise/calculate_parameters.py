#This script performs MLE on the company data fitting a log normal distribution to 2012 ONS data for each local authority
# TODO: Evaluate accuracy of fitted distributions
import csv, scipy.optimize as op, scipy.stats as sps, numpy as np, math, random

SIZES = ['0-4','5-9','10-19','20-49', '50-99','100-249','250+']




def main():
    data = get_data()
    output = []
    for id, d in data.items():
        r = op.minimize(ll, [0, 1], d, bounds=op.Bounds([-np.inf, 0], [np.inf, np.inf]))
        mean = r.x[0]
        sd   = r.x[1]
        output.append([id, mean, sd])
    with open('sic_lognormal_params.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for line in output:
            writer.writerow(line)



def get_data():
    data = {}
    with open('Data/2017_SIC_Size_Distributions.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            try:
                data[int(line['SIC'][:2])] = [int(line[s]) for s in SIZES]
            except:
                pass
    return data


def ll(param, arr):
    endpoints = [0,5,10,20,50,100,250,np.inf]
    s = 0
    for i,x in enumerate(arr):
        #print(x)
        a = (np.log(endpoints[i+1]) - param[0]) / param[1]
        b = (np.log(endpoints[i  ]) - param[0]) / param[1]
        if b != -np.inf and a != np.inf:
            s += x * np.log(sps.norm.cdf(a) - sps.norm.cdf(b))
        elif b == -np.inf:
            s+= x * np.log(sps.norm.cdf(a))
        else:
            s+= x * np.log(1 - sps.norm.cdf(b))
    return -s #return negative such that minimise methods can be used


if __name__ == '__main__':
    main()
