import matplotlib.pyplot as plt
from scipy.stats import lognorm
import numpy as np
import random, csv

SIZE_BANDS = ['0-4','5-9','10-19','20-49','50-99','100-249','250+']
BANDS = [0, 5, 10, 20, 50, 100, 250, np.inf]

def main():
    local_authority_data, la_totals = get_local_authority_data()
    params = get_parameters()

    results = {s : {'x': [], 'y': []} for s in SIZE_BANDS}

    for l, d in local_authority_data.items():
        for size, n in d.items():
            upper = BANDS[SIZE_BANDS.index(size) + 1]
            lower = BANDS[SIZE_BANDS.index(size)]

            mu = params[l]['mean']
            sigma = params[l]['sd']

            p = n / la_totals[l]

            #results[size].append([p, ln_cdf(upper, mu, sigma) - ln_cdf(lower, mu, sigma)])
            results[size]['x'].append(p)
            results[size]['y'].append(ln_cdf(upper, mu, sigma) - ln_cdf(lower, mu, sigma))
    plt.figure(0)

    for r, d in results.items():
        plt.scatter(d['x'], d['y'], label=r)


    plt.plot([0, 1], [0, 1], label='Target')
    plt.legend()

    plt.savefig('proportions.png')


    plt.figure(1)
    for r, d in results.items():
        plt.hist(d['x'], 20, label=r)

    plt.legend()
    plt.savefig('la_dists.png')

    plt.show()

def ln_cdf(x, mu, sigma):
    return lognorm.cdf(x, sigma, scale=np.exp(mu))

def get_parameters():
    data = {}
    with open('data/la_lognormal_params.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            data[line[0]] = {'mean': float(line[1]), 'sd': float(line[2])}
    return data

def get_local_authority_data():
    data = {}
    totals = {}
    with open('data/la_company_size_dist_by_id.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            data[line['la']] = {s : int(line[s]) for s in SIZE_BANDS}
            totals[line['la']] = 0
            for s, n in data[line['la']].items():
                totals[line['la']] += n
    return data, totals


if __name__ == '__main__':
    main()
