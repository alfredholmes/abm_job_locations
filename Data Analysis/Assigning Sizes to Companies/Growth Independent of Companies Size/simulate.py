import csv
from scipy.stats import lognorm
import datetime
import numpy as np

import matplotlib.pyplot as plt

#simulate employment sizes for 2012-03-12 and 2013-03-10

def main():
    mean, sd = get_ln_params()
    print('Getting companies...')
    companies = get_companies()
    sizes = []
    #for 2012 just pick sizes from ln dist
    print('Calculating sizes...')
    now = datetime.datetime.strptime('2012-03-12', '%Y-%m-%d')
    i = 0
    for company, data in companies.items():
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

    fig.savefig('Predicted_LA_Employment_Rates.png')
    plt.show()
    #plt.hist(sizes, bins=[0, 5, 10, 20, 50, 100, 250, 10000])
    #plt.show()

def get_companies():
    data = {}
    with open('../Business_Creations_And_Deaths.csv') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            if line[2] == 'BIRTH':
                data[line[1]] = {'BIRTH': datetime.datetime.strptime(line[0],  '%Y-%m-%d')}
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
