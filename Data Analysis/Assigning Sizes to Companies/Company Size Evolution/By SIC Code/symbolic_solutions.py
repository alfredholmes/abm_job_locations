from scipy.stats import norm, lognorm
import numpy as np
import gibrat_process
import csv

def main():
    sic_params = get_parameters()
    sics = gibrat_process.get_ages_by_sic()
    results = {}
    for sic, ages in sics.items():
        if sic not in sic_params:
            print('Missing sic ' + str(sic))
            continue
        target_mean = lognorm.mean(sic_params[sic]['sd'], scale=np.exp(sic_params[sic]['mean']))
        target_variance = lognorm.var(sic_params[sic]['sd'], scale=np.exp(sic_params[sic]['mean']))

        mean = calculate_mean(target_mean, ages)
        variance = calculate_variance(target_variance, mean, ages)

        print(mean, variance)

        results[sic]  = [mean, np.sqrt(variance)]

    with open('parameters_by_sic.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for sic, data in results.items():
            writer.writerow([sic] + data)


def get_parameters():
    data = {}
    with open('sic_lognormal_params.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            try:
                data[int(line[0])] = {'mean': float(line[1]), 'sd': float(line[2])}
            except:
                pass

    return data

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
        coefficiencts[max_age - age] = (n / total) ** 2
        #print(n / total * ((1 + mean) ** (2 * age)))
        coefficiencts[-1] -= (n ** 2) * (1 + mean) ** (2 * age) / (total ** 2)

    coefficiencts[-1] -= target

    roots = np.roots(coefficiencts)
    real_roots = [a for a in roots if np.imag(a) == 0 and np.real(a) - (1 + mean) ** 2 > 0]

    closest = (np.real([real_roots])).argmin()
    return np.real(real_roots[closest]) - (1 + mean) ** 2


if __name__ == '__main__':
    main()
