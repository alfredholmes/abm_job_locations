#About: This file aims to find parameters for a gibrat process that leads to the empirical distribution of company sizes

import matplotlib.pyplot as plt
from scipy.stats import norm
import scipy.integrate as integrate
from scipy.optimize import minimize, Bounds

import numpy as np
import csv, datetime as dt

TARGET = np.array([2087030, 299710, 151140, 80575, 25915, 14615, 9825])
TARGET = TARGET / np.sum(TARGET)
print(TARGET)
ENDPOINTS = [0,5,10,20,50,100,250,np.inf]

ENDPOINTS = [np.log(x) for x in ENDPOINTS]
ENDPOINTS_WITHOUT_INF = [0,5,10,20,50,100,250,10000]
WIDTHS = [ENDPOINTS_WITHOUT_INF[i] - ENDPOINTS_WITHOUT_INF[i-1] for i in range(1, len(ENDPOINTS_WITHOUT_INF))]
print(ENDPOINTS)

def main():
    #methods = [1]
    ages = get_ages()
    total = 0
    for age, n in ages.items():
        total += n


    res = minimize(likelyhood, (0, 0.01), args=ages, bounds=Bounds([-np.inf, 0], [np.inf, np.inf]))
    print(res)
    print(simulate((res.x[0], res.x[1]), ages))


    #print(res)
def likelyhood(params, ages):
    print('\t' + str(params))
    proportions = simulate(params, ages)
    error = (np.minimum(proportions, TARGET) * WIDTHS).mean()
    return -error


def simulate(params, ages):
    mean, variance = get_mean_variance(params[0], params[1])
    sd = np.sqrt(variance)
    endpoints = ENDPOINTS
    target = []

    proportions = np.zeros(len(TARGET))
    total = 0
    for age, n in ages.items():
        total += n
        proportions += [n * norm.cdf(endpoints[i], loc=mean, scale=age*sd) - n * norm.cdf(endpoints[i-1], loc=mean, scale=age * sd) for i in range(1, len(endpoints))]

    return (proportions / total)


def get_ages():
    data = {}
    with open('Business_Creations_And_Deaths_10000_sample.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        dead_companies = set()
        for line in reader:
            if line[2] == 'DEATH':
                dead_companies.add(line[1])
        csvfile.seek(0)
        for line in reader:
            if line[1] not in dead_companies:
                if line[0] in data:
                    data[line[0]] += 1
                else:
                    data[line[0]]  = 1

    now = dt.datetime.now()
    r = {}
    for date, n in data.items():
        then = dt.datetime.strptime(date, '%Y-%m-%d')
        age = int((now - then).days / 30)
        if age in r:
            r[age] += 1
        else:
            r[age] = 1


    return r
#functions to calculate E(log(1+\epsilon)) and variance \epsilon from N(mu, sigma)
def get_mean_variance(mu, sigma):
    mean = expectation(mu, sigma)
    variance = integrate.quad(lambda t: (np.log(1+t) ** 2) * norm.pdf(t, loc=mu, scale=sigma), mu - 4 * sigma, mu + 4 * sigma)[0] - mean ** 2
    return mean, variance

def expectation(mu, sigma):
    return integrate.quad(lambda t: np.log(1 + t) * norm.pdf(t, loc=mu, scale=sigma), mu - 4 * sigma, mu + 4 * sigma)[0]

def variance(mu, sigma):
    return integrate.quad(lambda t: (np.log(1+t) ** 2) * norm.pdf(t, loc=mu, scale=sigma), mu - 4 * sigma, mu + 4 * sigma)[0] - expectation(mu, sigma) ** 2

if __name__ == '__main__':
    main()
