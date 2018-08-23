#About: This file aims to find parameters for a gibrat process that leads to the empirical distribution of company sizes


import matplotlib.pyplot as plt
from scipy.stats import norm
import scipy.integrate as integrate
from scipy.optimize import minimize, Bounds

import numpy as np
import csv, datetime as dt

FILES = ['Business_Creations_And_Deaths_With_SIC/' + str(i) + '.csv' for i in range(0, 5)]

#print(TARGET)
ENDPOINTS = [0,5,10,20,50,100,250,np.inf]
ENDPOINTS = [np.log(x) for x in ENDPOINTS]

def main():
    #methods = [1]
    sics = get_ages_by_sic()
    params = {}
    targets = get_targets()
    for sic, ages in sics.items():
        if sic not in targets:
            print('Missing SIC ' + str(sic))
            continue
        print(sic)
        total = 0
        for age, n in ages.items():
            total += n
        res = minimize(likelyhood, (0, 0.01), args=(ages,targets[sic]), bounds=Bounds([-np.inf, 0], [np.inf, np.inf]))
        if not res.success:
            print(res)
        params[sic] = res.x
        print(res.x)

    with open('parameters_by_sic.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for sic, parameters in params.items():
            writer.writerow([sic] + parameters)


    #print(res)
def likelyhood(params, ages, target):
    #print('\t' + str(params))
    proportions = simulate(params, ages)
    error = ((proportions - target) ** 2).mean()
    #print(error)
    return error


def simulate(params, ages):
    mean, variance = get_mean_variance(params[0], params[1])
    sd = np.sqrt(variance)
    endpoints = ENDPOINTS
    target = []

    proportions = np.zeros(len(ENDPOINTS) - 1)
    total = 0
    for age, n in ages.items():
        total += n
        if sd == 0:
            proportions += [n if endpoints[i] > age * mean and endpoints[i-1] < age * mean else 0 for i in range(1, len(endpoints))]
        else:
            proportions += [n * norm.cdf(endpoints[i], loc=mean*age, scale=age*sd) - n * norm.cdf(endpoints[i-1], loc=mean*age, scale=age * sd) for i in range(1, len(endpoints))]

    return (proportions / total)

def get_targets():
    sizes = ['0-4','5-9','10-19','20-49','50-99','100-249','250+']
    proportions = {}
    with open('2017_2_SIC_size_dists.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            sic = int(line['SIC'][:2])
            if sic == 99:
                continue
            data = np.array([float(line[s]) for s in sizes])
            proportions[sic] = data / np.sum(data)

    return proportions


def get_ages_by_sic():
    data = {}
    dead_companies = set()
    for file in FILES:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                if line[2] == 'DEATH':
                    dead_companies.add(line[1])
                else:
                    #add sic code to the data
                    try:
                        sic = int(line[2][:2])
                        data[sic] = {}
                    except:
                        pass
    for file in FILES:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                if line[1] not in dead_companies:
                    try:
                        sic = int(line[2][:2])
                        if line[0] in data[sic]:
                            data[sic][line[0]] += 1
                        else:
                            data[sic][line[0]]  = 1
                    except:
                        pass
    now = dt.datetime.now()
    r = {sic: {} for sic in data}

    for sic, ages in data.items():
        for date, n in ages.items():
            then = dt.datetime.strptime(date, '%Y-%m-%d')
            age = int((now - then).days / 30)
            if age in r[sic]:
                r[sic][age] += 1
            else:
                r[sic][age] = 1
    return r
#functions to calculate E(log(1+\epsilon)) and variance \epsilon from N(mu, sigma)
def get_mean_variance(mu, sigma):
    if sigma == 0:
        return np.log(1+mu), 0
    mean = expectation(mu, sigma)
    variance = integrate.quad(lambda t: (np.log(1+t) ** 2) * norm.pdf(t, loc=mu, scale=sigma) if t > -1 else 0, mu - 4 * sigma, mu + 4 * sigma)[0] - mean ** 2
    return mean, variance

def expectation(mu, sigma):
    return integrate.quad(lambda t: np.log(1 + t) * norm.pdf(t, loc=mu, scale=sigma) if t > -1 else 0, mu - 4 * sigma, mu + 4 * sigma)[0]

def variance(mu, sigma):
    return integrate.quad(lambda t: (np.log(1+t) ** 2) * norm.pdf(t, loc=mu, scale=sigma) if t > -1 else 0, mu - 4 * sigma, mu + 4 * sigma)[0] - expectation(mu, sigma) ** 2

if __name__ == '__main__':
    main()
