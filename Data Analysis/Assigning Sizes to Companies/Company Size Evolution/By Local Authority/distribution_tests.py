import csv
import symbolic_solutions
import numpy as np
from scipy.stats import norm, lognorm
import matplotlib.pyplot as plt

import datetime

def main():
    date = datetime.datetime.strptime('2017-03-11', '%Y-%m-%d')
    las = symbolic_solutions.get_ages_by_la(date)
    la_ln_params = symbolic_solutions.get_la_parameters()
    la_growth_params = get_la_growth_parameters()
    la_size_bands = get_la_size_bands()

    sizes = [0, 5, 10, 20, 50, 100, 250, np.inf]
    companies = []
    for la, ages in las.items():
        size_bands = np.zeros(len(sizes) - 1)
        if la not in la_growth_params or la not in la_ln_params:
            continue
        #run prediction

        for age, n in ages.items():
            size = (1 + la_growth_params[la]['mean']) ** age
            #companies += [size] * int(round(n))

            for _ in range(round(n)):
                size = norm.rvs(size=age, scale=np.sqrt(la_growth_params[la]['sd']), loc=1 + la_growth_params[la]['mean']).prod()
            #    size = (1 + la_growth_params[la]['mean']) ** age
                companies.append(size)
            #print(size_bands, la_size_bands[la])

        #print(la, sum / total, lognorm.mean(la_ln_params[la]['sd'],scale=np.exp(la_ln_params[la]['mean'])))
        plt.hist(companies, 50, range=[0, 20], density=True)
        plt.plot(np.linspace(0, 20, num=1000), lognorm.pdf(np.linspace(0, 20, num=1000), la_ln_params[la]['sd'], scale=np.exp(la_ln_params[la]['mean'])))
        plt.show()
        break


def get_la_growth_parameters():
    parameters = {}
    with open('growth_parameters_by_local_authority.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            parameters[line[0]] = {'mean': float(line[1]), 'sd': float(line[2])}

    return parameters

def get_la_size_bands():
    size_bands = {}
    with open('la_local_unit_lognormal_params_2017.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            size_bands[line[0]] = [int(x) for x in line[4:]]

    return size_bands

if __name__ == '__main__':
    main()
