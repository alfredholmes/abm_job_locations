import matplotlib.pyplot as plt
from scipy.stats import lognorm
import numpy as np
import csv

SIZES = ['0-4','5-9','10-19','20-49', '50-99','100-249','250+']
BANDS = [0, 5, 10, 20, 50, 100, 250, np.inf]

BROAD_GROUPS = [(0, 4), (5, 40), (45, 46), (47, 48), (49, 54), (55, 57), (58, 64), (64, 67), (69, 76), (77, 83), (84, 85), (85, 86), (86, 89), (90, 100)]

def main():
    params = get_ln_params()
    sic_dists, totals = get_sic_dists()

    results = {s: {'x' : [], 'y': []} for s in SIZES}

    for sic, dist in sic_dists.items():
        for s in SIZES:
            if totals[sic] != 0:
                p = dist[s] / totals[sic]

                upper = BANDS[SIZES.index(s) + 1]
                lower = BANDS[SIZES.index(s)]

                mu = params[sic]['mean']
                sigma = params[sic]['sd']

                q = ln_cdf(upper, mu, sigma) - ln_cdf(lower, mu, sigma)

                results[s]['x'].append(p)
                results[s]['y'].append(q)

    plt.figure(0)
    for s, d in results.items():
        plt.scatter(d['x'], d['y'], label=s)

    plt.plot([0, 1], [0, 1], color='black', label='Target')
    plt.xaxis
    plt.legend()
    plt.savefig('sic_dist_replication.png')
    plt.figure(1)

    for s, d in results.items():
        plt.hist(d['x'], 20, alpha = 0.5, label=s)
    plt.legend()
    plt.savefig('sic_size_band_proportion.png')
    plt.show()



def ln_cdf(x, mu, sigma):
    return lognorm.cdf(x, sigma, scale=np.exp(mu))

def get_sic_dists():
    data = {}
    totals = {}
    with open('2017_SIC_Size_Distributions.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            try:
                sic = int(line['SIC'][:2])
                data[sic] = {s: int(line[s]) for s in SIZES}
                totals[sic] = int(line['Total'])
            except:
                pass
    return data, totals

def get_broad_industry_data():
    data = {}
    with open('2017_SIC_Size_Distributions.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            try:
                data[int(line['SIC'][:2])] = np.array([int(line[s]) for s in SIZES])
            except:
                pass
        r = {}
        for group in BROAD_GROUPS:
            totals = np.zeros(len(SIZES))
            for i in range(group[0], group[1]):
                if i in data:
                    totals += data[i]
            r[group] = totals

    return r

def get_broad_industry_params():
    data = {}
    with open('sic_broad_group_params.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            data[line[0]] = {'mean': float(line[1]),  'sd': float(line[2])}
    return data

def get_ln_params():
    data = {}
    with open('sic_lognormal_params.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            data[int(line[0])] = {'mean': float(line[1]),  'sd': float(line[2])}
    return data

if __name__ == '__main__':
    main()
