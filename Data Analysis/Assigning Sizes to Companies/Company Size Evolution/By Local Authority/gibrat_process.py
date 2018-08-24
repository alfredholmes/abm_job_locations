#About: This file aims to find parameters for a gibrat process that leads to the empirical distribution of company sizes


import matplotlib.pyplot as plt
from scipy.stats import norm
import scipy.integrate as integrate
from scipy.optimize import minimize, Bounds

import math

import numpy as np
import csv, datetime as dt

FILES = ['../../Business_Creations_And_Deaths.csv']

##### THIS CODE IS WRONG
##### TODO: FIX CODE

def main():
    #methods = [1]
    las = get_ages_by_la()
    params = {}
    local_authority_parameters = get_la_parameters()

    for la, ages in las.items():
        if la not in local_authority_parameters:
            print('LA Missing ' + la)
            continue
        la_mean = local_authority_parameters[la]['mean']
        la_sd = local_authority_parameters[la]['sd']
        total = 0
        lin = 0
        sq = 0
        for age, n in ages.items():
            total += n
            lin += age * n
            sq += (age * n) ** 2

        params[la] = [la_mean / (lin / total), la_sd * total / lin]

    with open('parameters_by_local_authority.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for sic, parameters in params.items():
            writer.writerow([sic] + parameters)




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

def get_la_parameters():
    data = {}
    with open('la_lognormal_params.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            data[line[0]] = {'mean': float(line[1]), 'sd': float(line[2])}

    return data

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
