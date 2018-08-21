import csv
from scipy.stats import lognorm
import numpy as np
import matplotlib.pyplot as plt


SIZE_BANDS = ['0-4','5-9','10-19','20-49', '50-99','100-249','250+']
SIZES = [0, 5, 10, 20, 50, 100, 250, np.inf]
BROAD_GROUPS = [(0, 4), (5, 40), (41, 44), (45, 46), (46, 47), (47, 48), (49, 54), (55, 57), (58, 64), (64, 67), (68, 69), (69, 76), (77, 83), (84, 85), (85, 86), (86, 89), (90, 100)]


def main():
    la_totals = get_broad_industry_totals_by_la()
    params = get_broad_industry_params()
    size_dist, sic_totals = get_broad_industry_size_dist()

    results = {s : {'x': [], 'y': []} for s in SIZE_BANDS}

    for group, totals in size_dist.items():

        for i, n in enumerate(totals):
            p = n / sic_totals[group]

            mean = params[str(group)]['mean']
            sd = params[str(group)]['sd']


            q = ln_cdf(SIZES[i+1], mean, sd) - ln_cdf(SIZES[i], mean, sd)

            results[SIZE_BANDS[i]]['x'].append(p)
            results[SIZE_BANDS[i]]['y'].append(q)
    plt.figure(0)
    for s, r in results.items():
        plt.scatter(r['x'], r['y'], label=s)

    plt.plot([0, 1],[0, 1])
    plt.legend()

    plt.xlabel('Actual Broad Indistry Size Proportion')
    plt.ylabel('Predicted Broad Indistry Size Proportion')

    plt.savefig('Figures/Broad_Industry_Predicted_proportions.png')

    #simulate la distributions
    sim_las = {}

    for la, totals in la_totals.items():
        size_dist = {s : 0 for s in SIZE_BANDS}
        for bg, n in totals.items():

            mean = params[str(bg)]['mean']
            sd = params[str(bg)]['sd']

            rvs = lognorm.rvs(sd, size=n, scale=np.exp(mean))
            for s in rvs:
                size_dist[get_size_band(s)] += 1
        sim_las[la] = size_dist


    results = {s : {'x': [], 'y': []} for s in SIZE_BANDS}
    actual_la = get_la_size_dist()
    for la, sizes in actual_la.items():
        total = 0
        sim_total = 0
        for s, n in sizes.items():
            total += n
            sim_total += sim_las[la][s]

        for s, n in sizes.items():
            results[s]['x'].append(n / total)
            results[s]['y'].append(sim_las[la][s] / sim_total)

    plt.figure(1)
    max = 0
    for s, r in results.items():
        plt.scatter(r['x'], r['y'], label=s)
        m = np.max(r['x'])
        if m > max:
            max = m
    plt.plot([0, max], [0, max], label='target')

    plt.xlabel('Actual Local Authority Employment Size Band Proportion')
    plt.ylabel('Predicted Local Authority Employment Size Band Proportion')

    plt.legend()
    plt.savefig('Figures/la_size_dist_comparison_actual_against_sic_prediction.png')

    plt.figure(2)
    for s, r in results.items():
        plt.hist(r['x'], 20, label=s, density=True)
    plt.legend()


    plt.xlabel('Local Authority Employment Size Band Proportion')
    plt.ylabel('Density')

    plt.savefig('Figures/actual_la_size_dists.png')

    plt.figure(3)
    for s, r in results.items():
        plt.hist(r['y'], 20, label=s, density=True)
    plt.legend()


    plt.xlabel('Predicted Local Authority Employment Size Band Proportion')
    plt.ylabel('Density')
    plt.savefig('Figures/predicted_la_size_dists.png')

    plt.show()



def get_size_band(x):
    for i, z in enumerate(SIZES):
        if x < z:
            return SIZE_BANDS[i-1]
    return SIZE_BANDS[-1]


def ln_cdf(x, mu, sigma):
    return lognorm.cdf(x, sigma, scale=np.exp(mu))

def get_la_size_dist():
    data = {}
    with open('Data/2017_la_local_unit_size_dist.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            data[line['la']] = {s : int(line[s]) for s in SIZE_BANDS}

    return data

def get_broad_industry_size_dist():
    data = {}
    with open('Data/2017_2_SIC_size_dists.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            try:
                data[int(line['SIC'][:2])] = np.array([int(line[s]) for s in SIZE_BANDS])
            except:
                pass
        r = {}
        for group in BROAD_GROUPS:
            totals = np.zeros(len(SIZE_BANDS))
            for i in range(group[0], group[1]):
                if i in data:
                    totals += data[i]
            r[group] = totals

    totals = {}
    for group, arr in r.items():
        totals[group] = np.sum(arr)

    return r, totals

def get_broad_industry_totals_by_la():
    data = {}
    with open('Data/2017_broad_group_local_units_by_la.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            data[line['la']] = {str(bg) : int(line[str(bg)]) for bg in BROAD_GROUPS}
    return data

def get_broad_industry_params():
    data = {}
    with open('sic_broad_group_params.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            data[line[0]] = {'mean': float(line[1]), 'sd': float(line[2])}
    return data

if __name__ == '__main__':
    main()
