from scipy.stats import lognorm
import predict_la_enterprises
import numpy as np
import csv
import matplotlib.pyplot as plt

def main():
    locations = get_company_locations()
    multipliers = predict_la_enterprises.get_sic_multipliers()
    companies = get_companies(locations)
    sic_ln_params = get_sic_ln_params()

    actual_las = get_enterprises_by_size()

    las = {}
    sizes = ['0-4', '5-9','10-19', '20-49', '50-99', '100-249', '250+']
    size_bands = [5, 10, 20, 50, 100, 250]

    for id, company in companies.items():

        if company['4_sic'] not in sic_ln_params:
            continue
        if company['2_sic'] not in multipliers:
            continue
        if company['la'] not in actual_las:
            continue
        #print('here')

        size = lognorm.rvs(sic_ln_params[company['4_sic']]['sd'], scale=np.exp(sic_ln_params[company['4_sic']]['mean']))
        for i, s in enumerate(size_bands):
            if size < s:
                size_band = sizes[i]
                break
        else:
            size_band = sizes[-1]




        if company['la'] in las:
            if size_band in las[company['la']]:
                las[company['la']][size_band] += multipliers[company['2_sic']]
            else:
                las[company['la']][size_band]  = multipliers[company['2_sic']]
        else:
            las[company['la']] = {size_band: multipliers[company['2_sic']]}

    results = {s: {'x': [], 'y': []} for s in sizes}

    for la, size_dist in las.items():
        actual_size_dist = actual_las[la]
        actual_total = 0
        total = 0
        for size, n in size_dist.items():
            total += n
            actual_total += float(actual_size_dist[size])
        for size, n in size_dist.items():
            results[size]['x'].append(float(actual_size_dist[size]) / actual_total)
            results[size]['y'].append(n / total)


    for s, data in results.items():
        plt.scatter(data['x'], data['y'])

    plt.show()





def get_enterprises_by_size():
    sizes = ['0-4', '5-9','10-19', '20-49', '50-99', '100-249', '250+']
    data = {}
    with open('Data/ONS/2012_enterprise_size_by_la.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            data[line['la']] = {s: line[s] for s in sizes}

    return data

def get_company_locations():
    locations = {}
    with open('2012-Snapshot.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            locations[line[0]] = line[1]
    return locations


def get_companies(locations):
    files = ['Data/CH/Company_Data/' + str(i) + '.csv' for i in range(5)]
    data = {}
    for file in files:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                if line[0] not in locations:
                    continue
                try:
                    data[line[0]] = {'4_sic': int(line[1][:4]), '2_sic': int(line[1][:2]), 'la': locations[line[0]]}
                except:
                    pass
    return data

def get_sic_ln_params():
    params = {}
    with open('sic_enterprise_lognormal_params_2012.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            if float(line[1]) == 0 and float(line[2]) == 1:
                continue
            params[int(line[0])] = {'mean': float(line[1]), 'sd': float(line[2])}
    return params


if __name__ == '__main__':
    main()
