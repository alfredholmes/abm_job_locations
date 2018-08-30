import sympy as sp
import numpy as np
from scipy.stats import norm, lognorm
import matplotlib.pyplot as plt
import csv

from scipy.optimize import minimize

import datetime


def main():
    date = datetime.datetime.strptime('2017-03-11', '%Y-%m-%d')
    las = get_ages_by_la(date)
    la_params = get_la_parameters()


    results = {}
    for la, ages in las.items():
        if la not in la_params:
            print(la + ' missing')
            continue

        print('Processing ' + la)

        target_mean = lognorm.mean(la_params[la]['sd'], scale=np.exp(la_params[la]['mean']))
        target_variance = lognorm.var(la_params[la]['sd'], scale=np.exp(la_params[la]['mean']))
        mean = calculate_mean(target_mean, ages)

        plt.plot(np.linspace(0, 2, num=1000), [get_dist_variance(x, mean, ages) for x in np.linspace(0,2, num=1000)])
        plt.show()


        variance = calculate_variance(target_variance, mean, ages)
        #variance = minimize(lambda x: (get_dist_variance(x, mean, ages) - target_variance) ** 2, 0.1).x[0] ** 2
        print(mean, variance)

        results[la]  = [mean, np.sqrt(variance)]

    with open('parameters_by_sic.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for sic, data in results.items():
            writer.writerow([la] + data)


def get_dist_variance(x, mean, ages):
    total = 0
    max_age = 0

    for age, n in ages.items():
        #print(expectation)
        if age > max_age:
            max_age = age
        total += n

    coefficiencts = np.zeros(max_age + 1)


    for age_1, n_1 in ages.items():
        for age_2, n_2 in ages.items():
            if age_1 == age_2:
                coefficiencts[max_age - age_1] = n_1 / total
            coefficiencts[-1] -= (n_1 * n_2 / (total ** 2)) * ((1 + mean) ** age_1) * ((1 + mean) ** age_2)

    variance = 0
    for i, n in enumerate(coefficiencts):
        variance += n * (x**2 + (1 + mean ** 2)) ** (max_age - i)


    return variance


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

    print(real_roots)

    closest = ((np.real([real_roots]) - 1) ** 2).argmin()
    mean =  np.real(real_roots[closest]) - 1

    return mean

def calculate_variance(target, mean, ages):
    total = 0
    max_age = 0

    for age, n in ages.items():
        #print(expectation)
        if age > max_age:
            max_age = age
        total += n

    coefficiencts = np.zeros(max_age + 1)


    for age_1, n_1 in ages.items():
        for age_2, n_2 in ages.items():
            if age_1 == age_2:
                coefficiencts[max_age - age_1] = n_1 / total
            coefficiencts[-1] -= (n_1 * n_2 / (total ** 2)) * ((1 + mean) ** age_1) * ((1 + mean) ** age_2)


    coefficiencts[-1] -= target

    roots = np.roots(coefficiencts)
    print([a for a in roots if np.imag(a) == 0])
    real_roots = [a for a in roots if np.imag(a) == 0 and np.real(a) > (1 + mean) ** 2]


    closest = (np.real([real_roots])).argmin()
    return np.real(real_roots[closest]) - (1 + mean) ** 2

def get_sic_multipliers():
    data = {}
    with open('sic_ch_multipliers.csv') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            data[int(line[0])] = float(line[1])
    return data

def get_la_parameters():
    params = {}
    with open('la_local_unit_lognormal_params_2017.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            params[line[0]] = {'mean': float(line[1]), 'sd': float(line[2])}
    return params

def get_ages_by_la(date):
    sic_multipliers = get_sic_multipliers()
    files = ['2017_Company_info/' + str(i) + '.csv' for i in range(0, 7)]
    las = {}
    for file in files:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                try:
                    sic = int(line[1][:2])
                    multiplier = sic_multipliers[sic]
                except:
                    continue
                la = line[-1]

                birth = datetime.datetime.strptime(line[2], '%Y-%m-%d')
                death = datetime.datetime.strptime(line[3], '%Y-%m-%d')

                if (date - birth).days < 0 or (date - death).days > 0:
                    continue

                age = int((date - birth).days / 28)

                if la in las:
                    if age in las[la]:
                        las[la][age] += multiplier
                    else:
                        las[la][age]  = multiplier
                else:
                    las[la] = {age: multiplier}

    return las






if __name__ == '__main__':
    main()
