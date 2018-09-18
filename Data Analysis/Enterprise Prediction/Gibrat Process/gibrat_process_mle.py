import csv, datetime
import numpy as np

from scipy.stats import norm
from scipy.optimize import minimize, Bounds

def main():
    print('Getting data...')
    companies = get_companies()
    age_bins = calculate_age_bins(companies)
    normalize_age_bins(age_bins)
    print('done')


    #result = minimize(lambda x: -likelihood(x, age_bins), (0.1, 0.01), jac=lambda x: -jacobian(x, age_bins), bounds=Bounds([-np.inf, 0], [np.inf, np.inf]))
    result = minimize(lambda x: -likelihood(x, age_bins), (0.1, 0.01))

    print(result)
    mean, sd = result.x
    #mean, sd = 9.47160452e-03, 2.47575785e-08
    age_bins = calculate_age_bins(companies)

    sizes = [5, 10, 20, 50, 100, 250, np.inf]
    results = np.zeros(7)
    j = 0
    for age, n in age_bins.items():
        #print(j / len(age_bins))
        j += 1
        if age <= 0:
            continue
        for _ in range(n):
            size = norm.rvs((1 + mean), sd, size=age).prod()

            for i, upper in enumerate(sizes):
                if size < upper:
                    results[i] += 1
                    break
    print(results)
    print([2087030, 299710, 151140, 80575, 25915, 14615, 9825])


def likelihood(params, age_bins):
    """ likelihood function for MLE

    calculates the probability of the observed outcome given the data
    -------------------------------
    Arguments:
        params: tuple of mean and standard deviation
        age_bins: dict of normalized age bins, {a: p} where p is the probability
                of picking a company with age a if pick a random company
    -------------------------------
    Returns:
        likelihood (float)

    """
    target = [2087030, 299710, 151140, 80575, 25915, 14615, 9825]
    sizes = [5, 10, 20, 50, 100, 250, np.inf]

    inner_sum = likelihood_inner_sum(params, age_bins, sizes)
    r = np.log(inner_sum).dot(target)
    print(r)
    return r


def likelihood_inner_sum(params, age_bins, sizes):
    """ Inner summand of the likelihood function split for multiprocessing

    -------------------------------
    Arguments:
        params, age_bins: Same as likelihood
        sizes:
            array of the upper bounds of the size bands for the total company size breakdown

    ------------------------------
    Returns:
        vector of length of sizes of the non logged inner summand (see data report)
    """
    mean, sd = params
    out = np.zeros(len(sizes))
    for age, p in age_bins.items():
        if age <= 0:
            continue
        lower = 0
        for i, upper in enumerate(sizes):
            if upper != np.inf:
                out[i] += p * norm.cdf((np.log(upper) - (age * mean)) / np.sqrt(age * sd ** 2))
            else:
                out[i] += p
            if lower != 0:
                out[i] -= p * norm.cdf((np.log(lower) - (age * mean)) / np.sqrt(age * sd ** 2))

            lower = upper
    return out

def jacobian(params, age_bins):
    target = [2087030, 299710, 151140, 80575, 25915, 14615, 9825]
    mean, sd = params

    sizes = [5, 10, 20, 50, 100, 250, np.inf]

    denominators = np.zeros(len(sizes))
    numerators = np.zeros((len(params), len(sizes)))

    for age, p in age_bins.items():
        if age <= 0:
            continue

        lower = 0
        for i, upper in enumerate(sizes):
            if upper != np.inf:
                numerators[0][i] += p * norm.pdf((np.log(upper) - (age * mean)) / np.sqrt(age * sd ** 2)) * (-age) / np.sqrt(age * sd ** 2)
                numerators[1][i] += p * norm.pdf((np.log(upper) - (age * mean)) / np.sqrt(age * sd ** 2)) * -( np.log(upper) - (age * mean)) / (age * sd ** 2) ** 1.5 * sd * age
                denominators[i] += p * norm.cdf((np.log(upper) - (age * mean)) / np.sqrt(age * sd ** 2))
                #print(p * norm.pdf((np.log(upper) - (age * mean)) / np.sqrt(age * sd ** 2)) * (-age) / np.sqrt(age * sd ** 2))
            else:
                denominators[i] += 1
            if lower != 0:
                numerators[0][i] -= p * norm.pdf((np.log(lower) - (age * mean)) / np.sqrt(age * sd ** 2)) * (-age) / np.sqrt(age * sd ** 2)
                numerators[1][i] -= p * norm.pdf((np.log(lower) - (age * mean)) / np.sqrt(age * sd ** 2)) * -(np.log(lower) - (age * mean)) / (age * sd ** 2) ** 1.5 * sd * age
                denominators[i] -= p * norm.cdf((np.log(lower) - (age * mean)) / np.sqrt(age * sd ** 2))
            lower = upper
    #print(numerators, denominators)

    jac = np.divide(numerators, denominators)
    jacobian_vector = np.zeros(len(params))

    for i in range(len(jac)):
        jacobian_vector[i] += jac[i].dot(target)

    #print(jac)

    return jacobian_vector


def normalize_age_bins(age_bins):
    total = 0
    for n in age_bins.values():
        total += n
    for age in age_bins:
        age_bins[age] /= total


def calculate_age_bins(companies):
    ages = {}
    for company in companies:
        if company['age'] in ages:
            ages[company['age']] += 1
        else:
            ages[company['age']]  = 1

    return ages

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
