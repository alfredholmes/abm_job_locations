import csv
import symbolic_solutions
import numpy as np
from scipy.stats import norm

import datetime

def main():
    date = datetime.datetime.strptime('2017-03-11', '%Y-%m-%d')
    las = symbolic_solutions.get_ages_by_la(date)
    la_params = symbolic_solutions.get_la_parameters()
    la_size_bands = get_la_size_bands()

    sizes = [0, 5, 10, 20, 50, 100, 250, np.inf]

    for la, ages in las.items():
        size_bands = np.zeros(len(sizes) - 1)
        if la not in la_params:
            continue
        #run prediction
        for age, n in ages.items():
            for _ in range(int(n)):
                size = norm.rvs(size=age, scale=la_params[la]['sd'], loc=la_params[la]['mean']).prod()
                for i, max in enumerate(sizes[1:]):
                    if size < max:
                        size_bands[i] += 1
                        break
        print(size_bands, la_size_bands[la])






def get_la_size_bands():
    size_bands = {}
    with open('la_local_unit_lognormal_params_2017.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            size_bands[line[0]] = [int(x) for x in line[4:]]

    return size_bands

if __name__ == '__main__':
    main()
