from scipy.stats import lognorm
from scipy.optimize import root, fsolve
import numpy as np
import csv, datetime

def main():
    params = [0.24247032943908334, 1.732968915296001]
    target_mean = lognorm.mean(params[1], scale=np.exp(params[0]))
    target_variance = lognorm.var(params[1], scale=np.exp(params[0]))
    companies = get_companies()

    companies_by_age = {}
    for company in companies:
        if company['age'] in companies_by_age:
            companies_by_age[company['age']] += 1
        else:
            companies_by_age[company['age']]  = 1

    param_mean = fsolve(mean, 0.0001, args=(target_mean, companies_by_age), fprime=mean_jacobian)[0]
    #param_variance = fsolve(variance, 0.1, args=(param_mean, target_variance, companies_by_age), fprime=variance_jacobian)[0]

    print(mean([param_mean], target_mean, companies_by_age), variance([0], param_mean, target_variance, companies_by_age))

    #print(param_mean, param_variance)


def mean(param, target, age_bins):

    total = 0
    sum = 0
    for age, n in age_bins.items():
        sum += n * (1 + param[0]) ** int(age)
        total += n

    return [sum / total - target]

def mean_jacobian(param, target, age_bins):
    total = 0
    sum = 0
    for age, n in age_bins.items():
        sum += n * age * (1 + param[0]) ** (age - 1)
        total += n

    return [sum / total]


def variance(param, param_mean, target, age_bins):
    total = 0
    v = 0
    cv = 0
    for age_1, n_1 in age_bins.items():
        v += n_1 * (param[0] ** 2 + (1 + param_mean) **2) ** age_1
        total += n_1
        for age_2, n_2 in age_bins.items():
            cv -= n_1 * n_2 * (1 + param_mean) ** (age_1 + age_2)

    x = v / total + cv / total ** 2 - target
    print(x)

    return [x]

def variance_jacobian(param, param_mean, target, age_bins):
    d_var = 0
    total = 0
    for age, n in age_bins.items():
        d_var += n * age * 2 * param[0] * (param[0] ** 2 + (1 + param_mean) ** 2) ** (age - 1)
        total += n

    return [d_var / total]


def get_companies():
    date = datetime.datetime(2017, 1, 1)
    companies = []
    files = ['../Data/CH/Company_Data/' + str(i) + '.csv' for i in range(7)]
    for file in files:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                try:
                    sic = int(line[1][:2])
                except:
                    continue
                la = line[5]

                if (date - datetime.datetime.strptime(line[3], '%Y-%m-%d')).days > 0:
                    continue
                age = int((date - datetime.datetime.strptime(line[2], '%Y-%m-%d')).days / 28)
                #age = 1
                companies.append({'sic': sic, 'la': la, 'age': age})

    return companies


if __name__ == '__main__':
    main()
