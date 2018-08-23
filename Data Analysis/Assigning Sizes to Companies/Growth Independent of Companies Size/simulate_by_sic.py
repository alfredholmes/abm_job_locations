import csv
from scipy.stats import lognorm
import datetime
import numpy as np

import matplotlib.pyplot as plt

FILES = ['../Company Size Evolution/By SIC Code/Business_Creations_And_Deaths_With_SIC/' + str(i) + '.csv' for i in range(0, 5)]

#simulate employment sizes for 2012-03-12 and 2013-03-10

def main():
    national_mean, national_sd = get_ln_params()
    params_by_sic = get_params_by_sic()
    print('Getting companies...')
    companies = get_companies()
    sizes = []
    #for 2012 just pick sizes from ln dist
    print('Calculating sizes...')
    now = datetime.datetime.strptime('2012-03-12', '%Y-%m-%d')
    i = 0
    for company, data in companies.items():
        mean = national_mean
        sd = national_sd
        try:
            mean = params_by_sic[int(data['SIC'])]['mean']
            sd = params_by_sic[int(data['SIC'])]['sd']
        except:
            pass
        if i % 100000 == 0:
            print(i)

        i += 1
        age = int((now - data['BIRTH']).days / 28)
        if age <= 0:
            continue
        try:
            size = lognorm.rvs(sd * age, scale=np.exp(mean*age))
            data['SIZE'] = size
        except:
            print('Exception: mean: ' + str(mean * age) + ', sd:' + str(sd * age))

    #employment prediction
    #locations
    print('calculating LA employment...')
    las = {}
    with open('../2012-Snapshot.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            if line[0] in companies:
                if line[1] in las:
                    if 'SIZE' in companies[line[0]]:
                        las[line[1]] += companies[line[0]]['SIZE']
                else:
                    if 'SIZE' in companies[line[0]]:
                        las[line[1]] = companies[line[0]]['SIZE']

    graph = {'x': [], 'y': []}
    with open('../2012_Employment_Totals.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            graph['x'].append(int(float(line[1]) * 1000))
            graph['y'].append(las[line[0]])

    fig = plt.figure()
    sp = fig.add_subplot(1, 1, 1)
    sp.scatter(graph['x'], graph['y'])

    #sp.set_yscale('log')
    #sp.set_xscale('log')

    fig.savefig('Predicted_LA_Employment_Rates_Growth_dependent_on_SIC.png')
    plt.show()
    #plt.hist(sizes, bins=[0, 5, 10, 20, 50, 100, 250, 10000])
    #plt.show()


def get_params_by_sic():
    data = {}
    with open('../SIC_Growth_Parameters.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            data[line['SIC']] = {'mean': float(line['mean']), 'sd': float(line['sd'])}
    return data
def get_companies():
    data = {}
    for file in FILES:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                if line[1] != 'DEATH':
                    data[line[1]] = {'BIRTH': datetime.datetime.strptime(line[0],  '%Y-%m-%d'), 'SIC': line[2][:2]}
                else:
                    if line[1] not in data:
                        print('ERROR: Company dying but this company is not yet alive...')
                    else:
                        data[line[1]]['DEATH'] = datetime.datetime.strptime(line[0],  '%Y-%m-%d')

    return data

def get_ln_params():
    with open('../lognorm_per_month_params.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        line = next(reader)
        return float(line[0]), float(line[1])

if __name__ == '__main__':
    main()
