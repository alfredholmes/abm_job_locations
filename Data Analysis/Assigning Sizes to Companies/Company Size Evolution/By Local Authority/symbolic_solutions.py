import sympy as sp
import numpy as np
from scipy.stats import norm, lognorm

import gibrat


def main():
    las = gibrat.get_ages_by_la()
    la_params = gibrat.get_la_parameters()




    for la, ages in las.items():
        if la not in la_params:
            print(la + ' missing')
            continue

        print('Processing ' + la)

        target_mean = lognorm.mean(la_params[la]['sd'], scale=np.exp(la_params[la]['mean']))
        target_variance = lognorm.var(la_params[la]['sd'], scale=np.exp(la_params[la]['mean']))

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
        coefficiencts[-1] -= n * (1 + mean) ** (2 * age) / total

    coefficiencts[-1] -= target

    roots = np.roots(coefficiencts)
    real_roots = [a for a in roots if np.imag(a) == 0 and np.real(a) - (1 + mean) ** 2 > 0]

    closest = (np.real([real_roots])).argmin()
    return np.real(real_roots[closest]) - (1 + mean) ** 2



if __name__ == '__main__':
    main()
