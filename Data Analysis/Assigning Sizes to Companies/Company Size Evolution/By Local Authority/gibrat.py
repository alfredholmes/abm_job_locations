import matplotlib.pyplot as plt
from scipy.stats import norm, lognorm
from scipy.optimize import minimize, Bounds, bisect, newton_krylov, anderson

import numpy as np
import csv, datetime as dt


def main():
    las = get_ages_by_la()
    la_params = get_la_parameters()

    la_growth_params = {}

    for la, ages in las.items():
        if la not in la_params:
            print(la + ' missing')
            continue

        target_mean = lognorm.mean(la_params[la]['sd'], scale=np.exp(la_params[la]['mean']))
        

        mu = bisect(lambda x: mean(x, ages, target_mean), 0, 0.03)
        la_growth_params[la] = mu

    with open('la_growth_means.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for la, mu in la_growth_params.items():
            writer.writerow([la, mu])


def variance_error(x, mean, ages, target):
    return variance(mean, x, ages) - target

def mean(x, ages, target):
#    print(x)
    total = 0
    mean = 0
    for age, n in ages.items():
        mean += n * (1 + x) ** age
        total += n
    return mean / total - target


def variance(mean, variance, ages):
    total = 0
    dist_var = 0

    for age, n in ages.items():
        total += n
    for age, n in ages.items():
        dist_var += (n / total) ** 2 * ((variance + (1 + mean) ** 2) ** age - (1 + mean) ** (2 * age))


    return dist_var / (total ** 2)


def get_la_parameters():
    data = {}
    with open('la_lognormal_params.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            data[line[0]] = {'mean': float(line[1]), 'sd': float(line[2])}

    return data

#get the mean and the variance of the national distribution taking the parameters of \epsilon


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


if __name__ == '__main__':
    main()
