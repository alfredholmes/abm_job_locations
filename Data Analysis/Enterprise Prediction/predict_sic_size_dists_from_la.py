import analysis, predict_la_enterprises
import csv

import numpy as np
from scipy.stats import lognorm

import matplotlib.pyplot as plt

def main():
    companies = analysis.get_ch_data()
    multipliers = predict_la_enterprises.get_sic_multipliers()
    locations = predict_la_enterprises.get_2012_company_locations()
    params = get_la_lognorm_params()

    size_by_sic = get_2012_size_bands()

    predicted_sic_size_bands = {}

    for company in companies:
        if company[0] not in locations:
            continue
        try:
            sic = int(company[1][:2])
        except:
            continue

        if sic == 99:
            continue
        if sic not in multipliers:
            m = 1
        else:
            m = multipliers[sic]

        la = locations[company[0]]
        if la not in params:
            #print(la + ' missing from params')
            continue

        size = lognorm.rvs(params[la]['sd'], scale=np.exp(params[la]['mean']))
        size_band = get_size_band(size)
        if sic in predicted_sic_size_bands:
            if size_band in predicted_sic_size_bands[sic]:
                predicted_sic_size_bands[sic][size_band] += 1
            else:
                predicted_sic_size_bands[sic][size_band]  = 1
        else:
            predicted_sic_size_bands[sic] = {size_band: 1}

    bands = ['0-4', '5-9', '10-19','20-49', '50-99', '100-249', '250+']
    results = {b : {'x': [], 'y': []} for b in bands}

    for sic, bands in predicted_sic_size_bands.items():
        if sic not in size_by_sic:
            print(str(sic) + ' missing')
            continue
        total = 0

        for band, n in bands.items():
            total += n

        for band, n in bands.items():
            if size_by_sic[sic]['Total'] == 0:
                continue
            results[band]['x'].append(size_by_sic[sic][band] / size_by_sic[sic]['Total'])
            results[band]['y'].append(n / total)

    for band, data in results.items():
        plt.scatter(data['x'], data['y'])

    plt.plot([0, 1], [0, 1])
    plt.xlabel('ONS proportion')
    plt.ylabel('CH prediction')
    plt.savefig('enterprise_size_by_sic_predicted_with_la_sizes.png')
    plt.show()

def get_2012_size_bands():
    data = {}
    bands = ['0-4', '5-9', '10-19','20-49', '50-99', '100-249', '250+', 'Total']
    with open('Data/ONS/2012_enterprise_size_by_sic.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            data[int(line['SIC'])] = {b: int(line[b]) for b in bands}
    return data


def get_size_band(size):
    ends = [5, 10, 20, 50, 100, 250, np.inf]
    bands = ['0-4', '5-9', '10-19','20-49', '50-99', '100-249', '250+']
    for i, end in enumerate(ends):
        if size < end:
            return bands[i]

def get_la_lognorm_params():
    params = {}
    with open('Data/la_enterprise_lognormal_params_2012.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            params[line[0]] = {'mean': float(line[1]), 'sd': float(line[2])}

    return params

if __name__ == '__main__':
    main()
