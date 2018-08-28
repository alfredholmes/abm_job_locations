import matplotlib.pyplot as plt
from scipy.stats import norm, lognorm
from scipy.optimize import minimize, Bounds, bisect, newton_krylov, anderson

import numpy as np
import csv, datetime as dt

TARGET = [0.24247032943908334, 1.732968915296001]


def main():
    ages = get_ages()

    target_mean = lognorm.mean(TARGET[1], scale=np.exp(TARGET[0]))
    target_variance = lognorm.var(TARGET[1], scale=np.exp(TARGET[0]))


    mean = calculate_mean(target_mean, ages)
    variance = calculate_variance(target_variance, mean, ages)

    print(mean, variance)


def calculate_mean(target, ages):
    total = 0
    max_age = 0

    for age, n in ages.items():
        #print(expectation)
        if age > max_age:
            max_age = age
        total += n

    coefficiencts = np.zeros(max_age + 1)


    for age, n in ages.items():
        coefficiencts[max_age - age] = n / total

    coefficiencts[-1] -= target

    roots = np.roots(coefficiencts)
    real_roots = [a for a in roots if np.imag(a) == 0]

    closest = ((np.real([real_roots]) - 1) ** 2).argmin()
    return np.real(real_roots[closest]) - 1

def calculate_variance(target, mean, ages):
    total = 0
    max_age = 0

    for age, n in ages.items():
        #print(expectation)
        if age > max_age:
            max_age = age
        total += n

    coefficiencts = np.zeros(max_age + 1)


    for age, n in ages.items():
        coefficiencts[max_age - age] = n / total
        #print(n / total * ((1 + mean) ** (2 * age)))
        coefficiencts[-1] -= (n ** 2) * (1 + mean) ** (2 * age) / (total ** 2)

    coefficiencts[-1] -= target

    roots = np.roots(coefficiencts)
    real_roots = [a for a in roots if np.imag(a) == 0 and np.real(a) - (1 + mean) ** 2 > 0]

    closest = (np.real([real_roots])).argmin()
    return np.real(real_roots[closest]) - (1 + mean) ** 2

#get the mean and the variance of the national distribution taking the parameters of \epsilon


def get_ages():
    data = {}
    with open('../../Business_Creations_And_Deaths.csv', 'r') as csvfile:
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

if __name__ == '__main__':
    main()
