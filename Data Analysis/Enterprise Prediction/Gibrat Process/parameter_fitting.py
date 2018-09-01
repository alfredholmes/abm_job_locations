import csv
import datetime


import numpy as np
from scipy.stats import lognorm
from scipy.optimize import minimize



def main():
    print('loading data...')
    sic_lognormal_params = get_sic_lognormal_params()
    #print(sic_lognormal_params)
    ch_data = get_ch_data(datetime.datetime(2017, 6, 1))
    #sic_multipliers = get_sic_multipliers()
    ages_by_sic = get_ages_by_sic(ch_data, datetime.datetime(2017, 6, 1))

    print('done')

    results = {}

    for sic, ages in ages_by_sic.items():
        print(sic)
        if sic not in sic_lognormal_params:
            print('missing sic ' + str(sic))
            continue

        #print(sic_lognormal_params[sic]['sd'], sic_lognormal_params[sic]['mean'])
        target_mean = lognorm.mean(sic_lognormal_params[sic]['sd'], scale=np.exp(sic_lognormal_params[sic]['mean']))
        target_variance = lognorm.var(sic_lognormal_params[sic]['sd'], scale=np.exp(sic_lognormal_params[sic]['mean']))

        mean = find_mean(target_mean, ages)
        #print(mean)
        variance = find_varaince(target_variance, ages, mean)

        results[sic] = [mean, variance]


    with open('sic_growth_params.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for sic, data in results.items():
            writer.writerow([sic] + data)


def find_mean(target, ages):
    total = 0
    max_age = 0
    for age, n in ages.items():
        total += n
        if age > max_age:
            max_age = age

    params = np.zeros(max_age + 1)
    for age, n in ages.items():
        params[max_age - age] = n / total

    params[-1] -= target

    roots = np.roots(params)
    real_roots = np.array([np.real(r) for r in roots if np.imag(r) == 0])
    return real_roots[((real_roots - 1) ** 2).argmin()] - 1

def find_varaince(target, ages, mean):
    total = 0
    max_age = 0
    for age, n in ages.items():
        total += n
        if age > max_age:
            max_age = age

    params = np.zeros(max_age + 1)

    for age_1, n_1 in ages.items():
        for age_2, n_2 in ages.items():
            if age_1 == age_2:
                params[max_age - age_1] = n_1 / total
            params[-1] -= n_1 * n_2 / (total ** 2) * (1 + mean) ** (age_1 + age_2)
    params[-1] -= target

    roots = np.roots(params)
    real_roots = [np.real(r) for r in roots if np.imag(r) == 0]
    #print(real_roots)
    real_roots = [r for r in real_roots if r > (1 + mean) ** 2]
    if len(real_roots) == 0:
        return 0
    if len(real_roots) == 1:
        return real_roots[0] - (1 + mean) ** 2
    else:
        return real_roots[np.array(real_roots).argmin] - (1 + mean) ** 2


def get_ages_by_sic(companies, date):
    ages = {}
    for company in companies:
        birth = datetime.datetime.strptime(company[2], '%Y-%m-%d')
        age = int(round((date - birth).days / 28))
        try:
            sic = int(company[1][:2])
        except:
            continue

        if sic in ages:
            if age in ages[sic]:
                ages[sic][age] += 1
            else:
                ages[sic][age]  = 1
        else:
            ages[sic] = {age: 1}

    return ages



def get_sic_multipliers():
    multipliers = {}
    with open('../Data/sic_ch_multipliers.csv') as csvfile:
        reader = csv.reader()
        for line in reader:
            multipliers[int(line[0])] = float(line[1])
    return multipliers


def get_sic_lognormal_params():
    params = {}
    with open('../Data/2017_2_sic_enterprise_lognormal_params.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            if line[1] == '0.0' and line[2] == '1.0' or float(line[2]) > 100:
                continue
            params[int(line[0])] = {'mean': float(line[1]), 'sd': float(line[2])}

    return params


def get_ch_data(date):
    files = ['../Data/CH/Company_Data/' + str(i) + '.csv' for i in range(5)]
    companies = []
    for file in files:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                incorp_date = datetime.datetime.strptime(line[2], '%Y-%m-%d')
                last_seen = datetime.datetime.strptime(line[3], '%Y-%m-%d')
                if (date - incorp_date).days > 0 and (date - last_seen).days < 0:
                    companies.append(line)

    return companies
if __name__ == '__main__':
    main()
