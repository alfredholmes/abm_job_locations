#About: This file aims to find parameters for a gibrat process that leads to the empirical distribution of company sizes


import matplotlib.pyplot as plt
from scipy.stats import norm
import scipy.integrate as integrate
from scipy.optimize import minimize, Bounds

import math

import numpy as np
import csv, datetime as dt

FILES = ['../../Business_Creations_And_Deaths.csv']

#print(TARGET)
ENDPOINTS = [0,5,10,20,50,100,250,np.inf]
ENDPOINTS = [np.log(x) for x in ENDPOINTS]

def main():
    #methods = [1]
    las = get_ages_by_la()
    params = {}
    targets = get_targets()
    for la, ages in las.items():
        if la not in targets:
            print('Missing LA ' + la)
            continue
        print(la)
        total = 0
        for age, n in ages.items():
            total += n
        res = minimize(likelyhood, (0, 0.01), args=(ages,targets[la]), bounds=Bounds([-np.inf, 0], [np.inf, np.inf]))
        if not res.success:
            print(res)
        params[la] = res.x
        print(res.x)

    with open('parameters_by_local_authority.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for sic, parameters in params.items():
            writer.writerow([sic] + parameters)


    #print(res)
def likelyhood(params, ages, target):
    proportions = simulate(params, ages)
    error = ((proportions - target) ** 2).mean()

    #print(error)
    return error


def simulate(params, ages):
    mean, variance = get_mean_variance(params[0], params[1])
    sd = np.sqrt(variance)

    #print(mean, sd)
    endpoints = ENDPOINTS
    target = []

    proportions = np.zeros(len(ENDPOINTS) - 1)
    total = 0
    for age, n in ages.items():
        total += n
        if sd == 0:
            proportions += [n if endpoints[i] > age * mean and endpoints[i-1] < age * mean else 0 for i in range(1, len(endpoints))]
        else:
            to_add = [n * norm.cdf(endpoints[i], loc=mean*age, scale=age*sd) - n * norm.cdf(endpoints[i-1], loc=mean*age, scale=age * sd) for i in range(1, len(endpoints))]
            to_add = [f if not math.isnan(f) else 0 for f in to_add]
            proportions += to_add



    return (proportions / total)

def get_targets():

    sizes = ['0-4','5-9','10-19','20-49','50-99','100-249','250+']
    proportions = {}
    with open('2017-la-company-size-distributions.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            la = line['la']
            data = np.array([float(line[s]) for s in sizes])
            proportions[la] = data / np.sum(data)

    return proportions

def get_ages_by_la():
    files = ['2017_Company_info/' + str(i) + '.csv' for i in range(0, 10)]
    las = {}
    for file in files:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                la = line[1]
                age = int(line[2])
                if la in las:
                    if age in las[la]:
                        las[la][age] += 1
                    else:
                        las[la][age]  = 1
                else:
                    las[la] = {age: 1}
    return las

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

def get_company_las():
    companies = {}
    with open('2012-Snapshot.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            companies[line[0]] = line[1]

if __name__ == '__main__':
    main()
