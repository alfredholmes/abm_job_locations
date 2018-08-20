import matplotlib.pyplot as plt
from scipy.stats import lognorm
from scipy.stats import linregress
import numpy as np
import random, csv

SIZE_BANDS = ['0-4','5-9','10-19','20-49','50-99','100-249','250+']
BANDS = [0, 5, 10, 20, 50, 100, 250, np.inf]


def main():
    total_companies = get_number_of_companies()
    total_employment = get_total_employment_stats()
    params = get_parameters()

    results = {'x': np.zeros(len(total_companies)), 'y': np.zeros(len(total_companies))}
    i = 0
    for la, n in total_companies.items():
        mean = params[la]['mean']
        sd = params[la]['sd']

        companies = lognorm.rvs(sd, size=n, scale=np.exp(mean))
        total = np.sum(companies)

        results['x'][i] = (total_employment[la])
        results['y'][i] = (total)

        i+= 1

    slope, intercept, _,_,_  = linregress((results['x']), (results['y']))



    plt.scatter((results['x']), (results['y']))
    plt.xlabel('Actual')
    plt.ylabel('Predicted')

    plt.plot((results['x']),intercept + slope*(results['x']), label=str(slope) + 'x + ' + str(intercept))
    plt.legend()
    plt.savefig('EmploymentPrediction.png')
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

def get_total_employment_stats():
    data = {}
    with open('data/2016_employment.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            data[line[0]] = float(line[1]) * 1000
    return data

def get_number_of_companies():
    data = {}
    with open('data/la_company_size_dist_by_id.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            total = 0
            for s in SIZE_BANDS:
                total += int(line[s])
            data[line['la']] = total
        return data

if __name__ == '__main__':
    main()
