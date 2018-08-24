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


    mu = bisect(lambda x: mean(x, ages, target_mean), 0, 0.03)
    #mu = bisect(lambda x: mean(x, ages, target_mean), 0, 0.1)

    #var = bisect(lambda x: variance_error(x, mu, ages, target_variance), 0, 0.01)

    #print(mu, np.sqrt(var))
    #plt.plot([x/500000 for x in range(1000)], [mean(x / 1000000, ages, 0) for x in range(1000)])
    #plt.plot([0, 1000 / 50000], [target_mean, target_mean])
    plt.plot([x/10000 for x in range(1000)], [variance(mu, x / 10000, ages) for x in range(1000)])
    plt.show()

    #var = bisect(lambda x : (x, mu, ages, target_variance), 0, 0.01)
    #print(var)
    #var = bisect(lambda x : error(mu, x, ages, target_variance), 0, var)
    #print(var)

    #print(mu, np.sqrt(var))



    #print(error(mu, var, ages, target_variance))


    #print(minimize(error, (0.001, 0.0001), (ages, target_mean, target_variance), bounds=Bounds([-0.5, 0], [0.5, 0.001])))
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
