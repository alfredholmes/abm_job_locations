from scipy.stats import norm, lognorm
import datetime as dt
import numpy as np
import csv

def main():
    sic_params = get_parameters()
    sics = get_ages_by_sic()
    results = {}
    for sic, ages in sics.items():
        if sic not in sic_params:
            print('Missing sic ' + str(sic))
            continue
        target_mean = lognorm.mean(sic_params[sic]['sd'], scale=np.exp(sic_params[sic]['mean']))
        target_variance = lognorm.var(sic_params[sic]['sd'], scale=np.exp(sic_params[sic]['mean']))

        mean = calculate_mean(target_mean, ages)
        variance = calculate_variance(target_variance, mean, ages)

        print(mean, variance)

        results[sic]  = [mean, np.sqrt(variance)]

    with open('parameters_by_sic.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for sic, data in results.items():
            writer.writerow([sic] + data)


def get_ages_by_sic():
    files = ['Business_Creations_And_Deaths_With_SIC/' + str(i) + '.csv' for i in range(0, 5)]
    data = {}
    dead_companies = set()
    for file in files:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                if line[2] == 'DEATH':
                    dead_companies.add(line[1])
                else:
                    #add sic code to the data
                    try:
                        sic = int(line[2][:2])
                        data[sic] = {}
                    except:
                        pass

    for file in files:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                if line[1] not in dead_companies:
                    try:
                        sic = int(line[2][:2])
                        if line[0] in data[sic]:
                            data[sic][line[0]] += 1
                        else:
                            data[sic][line[0]]  = 1
                    except:
                        pass
    now = dt.datetime.now()
    r = {sic: {} for sic in data}

    for sic, ages in data.items():
        for date, n in ages.items():
            then = dt.datetime.strptime(date, '%Y-%m-%d')
            age = int((now - then).days / 30)
            if age in r[sic]:
                r[sic][age] += 1
            else:
                r[sic][age] = 1
    return r

def get_parameters():
    data = {}
    with open('sic_lognormal_params.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            try:
                data[int(line[0])] = {'mean': float(line[1]), 'sd': float(line[2])}
            except:
                pass

    return data

def calculate_mean(target, ages):
    total = 0
    max_age = 0

    for age, n in ages.items():
        #print(expectation)
        if age > max_age:
            max_age = age
        total += n

    coefficiencts = np.zeros(max_age + 1)


    for age, n in ages.items():
        coefficiencts[max_age - age] = n / total

    coefficiencts[-1] -= target

    roots = np.roots(coefficiencts)
    real_roots = [a for a in roots if np.imag(a) == 0]

    closest = ((np.real([real_roots]) - 1) ** 2).argmin()
    return np.real(real_roots[closest]) - 1

def calculate_variance(target, mean, ages):
    total = 0
    max_age = 0

    for age, n in ages.items():
        #print(expectation)
        if age > max_age:
            max_age = age
        total += n

    coefficiencts = np.zeros(max_age + 1)


    for age, n in ages.items():
        coefficiencts[max_age - age] = (n / total) ** 2
        #print(n / total * ((1 + mean) ** (2 * age)))
        coefficiencts[-1] -= (n ** 2) * (1 + mean) ** (2 * age) / (total ** 2)

    coefficiencts[-1] -= target

    roots = np.roots(coefficiencts)
    real_roots = [a for a in roots if np.imag(a) == 0 and np.real(a) - (1 + mean) ** 2 > 0]

    closest = (np.real([real_roots])).argmin()
    return np.real(real_roots[closest]) - (1 + mean) ** 2



if __name__ == '__main__':
    main()
