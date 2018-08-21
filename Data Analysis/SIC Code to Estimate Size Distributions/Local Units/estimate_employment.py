import csv
from scipy.stats import lognorm
import numpy as np
import matplotlib.pyplot as plt
import random


SIZE_BANDS = ['0-4','5-9','10-19','20-49', '50-99','100-249','250+']
SIZES = [0, 5, 10, 20, 50, 100, 250, np.inf]
BROAD_GROUPS = [(0, 4), (5, 40), (41, 44), (45, 46), (46, 47), (47, 48), (49, 54), (55, 57), (58, 64), (64, 67), (68, 69), (69, 76), (77, 83), (84, 85), (85, 86), (86, 89), (90, 100)]


def main():

    estimated = estimate_employment()
    actual = get_employment_data()

    result = {'x': [], 'y': []}

    predicted = 0
    actual_total = 0

    for la, n in estimated.items():
        result['y'].append(n)
        result['x'].append(actual[la])

        predicted += n
        actual_total += actual[la]
        #print(n, actual[la])

    print(predicted, actual_total)

    plt.scatter(result['x'], result['y'], label='UK Local Authorities')
    plt.plot(result['x'], result['x'], label='Target', color='black')
    plt.legend()

    plt.xlabel('Employment (ONS 2016)')
    plt.ylabel('Predicted Employment')

    plt.savefig('Employment prediction')

    plt.show()

def estimate_employment():
    las = get_broad_industry_totals_by_la()
    params = get_broad_industry_params()

    prediction = {}

    for la, totals in las.items():
        total = 0
        for bg, n in totals.items():
            mean = params[bg]['mean']
            sd = params[bg]['sd']
            #print(mean, sd)
            #total += np.sum(lognorm.rvs(sd, size=n, scale=np.exp(mean)))
            for _ in range(n):
                total += random.lognormvariate(mean, sd)
        prediction[la] = total
    return prediction

def ln_cdf(x, mu, sigma):
    return lognorm.cdf(x, sigma, scale=np.exp(mu))

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


def get_employment_data():
    data = {}
    with open('Data/2016_employment.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            data[line[0]] = int(float(line[1]) * 1000)

    return data
if __name__ == '__main__':
    main()
