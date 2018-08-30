import csv
from scipy.stats import norm, lognorm, linregress
from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt


def main():
    las = {}
    print('Getting data...')
    companies = get_ch_data()
    growth_parameters = get_sic_growth_parameters()
    sic_multipliers = get_sic_multipliers()
    ln_sic_params = get_sic_ln_params()
    ln_la_params = get_la_ln_params()
    la_growth_parameters = get_la_growth_parameters()

    local_unit_totals = get_local_unit_totals()
    predicted_la_totals = {}

    print('Calculating sizes...')
    i = 0
    for id, company in companies.items():
        i += 1
        if i % 10000 == 0:
            print('\t' + str(i))
        sic = company['sic']
        la  = company['LA' ]
        if sic not in sic_multipliers or sic not in growth_parameters or sic not in ln_sic_params:
            continue
        if la not in ln_la_params or la not in la_growth_parameters:
            #print(la + ' missing')
            continue
        loc = 1 + growth_parameters[sic]['mean']
        scale = growth_parameters[sic]['sd']
        age = company['age']
        #size = norm.rvs(size=age, loc=loc, scale=scale).prod()
        size = lognorm.rvs(ln_sic_params[sic]['sd'], scale=np.exp(ln_sic_params[sic]['mean']))
        #size = lognorm.rvs(np.sqrt(ln_la_params[la]['sd']), scale=np.exp(ln_la_params[la]['mean']))




        #size = norm.rvs(size=age, scale=la_growth_parameters[la]['sd'], loc=1 + la_growth_parameters[la]['mean']).prod()
        #size = (1 + la_growth_parameters[la]['mean']) ** age
        if company['LA'] in las:
            las[company['LA']] += size * sic_multipliers[sic]
        else:
            las[company['LA']]  = size * sic_multipliers[sic]


    employment_data = get_employment_data()
    x = []
    y = []
    for la, n in las.items():
        if la not in employment_data:
            print(la +' missing')
            continue
        y.append(n)
        x.append(employment_data[la])

        if 5 * x[-1] < y[-1]:
            print(la) 

    plt.figure(0)
    plt.scatter(x, y, label='local_authorities')
    #grad, intercept, _, _, _ = linregress(x, y)
    intercept = 0
    grad = minimize(lambda t: (((t * np.array(x)) - np.array(y)) ** 2).mean(), 1).x[0]
    #print(grad)
    plt.plot(x, grad * np.array(x) + intercept, label='y = ' + str(grad)  + 'x +' + str(intercept), color='black')
    plt.legend()
    plt.savefig('employment_predictions_sic_ln_dists_process.png')


    plt.show()





def get_ch_data():
    companies = {}
    with open('../Data/CH/2012-Snapshot.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            companies[line[0]] = {'age': int(int(line[2]) * 12 / 365 * 28), 'LA': line[1]}
    files = ['../Data/CH/Company_Data/' + str(i) + '.csv' for i in range(0, 5)]
    company_sics = {}
    for file in files:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                try:
                    sic = int(line[1][:2])
                except:
                    pass
                company_sics[line[0]] = sic
    to_delete = []
    for company in companies:
        if company not in company_sics:
            to_delete.append(company)
            continue
        companies[company]['sic'] = company_sics[company]
    return companies

def get_sic_growth_parameters():
    data = {}
    with open('growth_parameters_by_sic.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            data[int(line[0])] = {'mean': float(line[1]), 'sd': float(line[2])}

    return data

def get_local_unit_totals():
    las = {}
    sizes = ['0-4','4-9','10-19','20-49','49-100','100-249','250+']
    with open('../Data/ONS/2012_local_units_by_la.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            las[line['id']] = {s: int(line[s]) for s in sizes}
            las[line['id']]['total'] = line['Total']

    return las

def get_la_growth_parameters():
    data = {}
    with open('growth_parameters_by_local_authority.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            data[line[0]] = {'mean': float(line[1]), 'sd': float(line[2])}

    return data

def get_sic_multipliers():
    multipliers = {}
    with open('../sic_ch_multipliers.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            multipliers[int(line[0])] = float(line[1])

    return multipliers

def get_employment_data():
    employment = {}
    with open('../Data/ONS/2012_Employment_Totals.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            employment[line[0]] = int(float(line[1]) * 1000)

    return employment

def get_sic_ln_params():
    params = {}
    with open('sic_local_unit_lognormal_params_2012.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            params[int(line[0])] = {'mean': float(line[1]), 'sd': float(line[2])}
    return params

def get_la_ln_params():
    params = {}
    with open('la_local_units_lognormal_params.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            params[line[0]] = {'mean': float(line[1]), 'sd': float(line[2])}
    return params


if __name__ == '__main__':
    main()
