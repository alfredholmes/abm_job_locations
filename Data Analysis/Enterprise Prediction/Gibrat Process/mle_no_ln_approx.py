import csv, datetime
import growth_model_2_rvs
import numpy as np

from scipy.optimize import minimize
from scipy.stats import norm

import os
from multiprocessing import Pool

def main():
    sizes_by_la, sizes_by_sic = get_size_distribution_data()
    print('Getting companies...')
    companies = growth_model_2_rvs.get_companies(sizes_by_la, sizes_by_sic)
    print('done')

    local_authorities = [la for la in sizes_by_la]
    sic_codes = [sic for sic in sizes_by_sic]

    print('Sorting companies...')

    age_bins = growth_model_2_rvs.sort_companies(companies, sizes_by_la, sizes_by_sic)

    print('done')
    scale = 0.01
    initial = np.ones((2 * len(sic_codes) + 2 * len(local_authorities))) * scale
    initial = np.divide(initial, [1] * (len(sic_codes) + len(local_authorities)) + [10] * (len(sic_codes) + len(local_authorities)))
    #print(likelihood_jacobian(initial, age_bins, sizes_by_la, sizes_by_sic, local_authorities, sic_codes))
    #print(likelihood(initial, age_bins, sizes_by_la, sizes_by_sic, local_authorities, sic_codes))

    result = minimize(lambda x: -likelihood(x, age_bins, sizes_by_la, sizes_by_sic, local_authorities, sic_codes), initial, jac=lambda x: -likelihood_jacobian(x, age_bins, sizes_by_la, sizes_by_sic, local_authorities, sic_codes))
    print(result)
    with open('param_fit.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(local_authorities + sic_codes)
        writer.writerow(result.x)

def likelihood(params, age_bins, sizes_by_la, sizes_by_sic, local_authorities, sic_codes):
    """ Likelihood function
    params is a 1 dim array of means then standard deviations for the parameters of each local authority and SIC code
    """

    sizes = ['0-4', '5-9', '10-19', '20-49', '50-99', '100-249', '250+']


    with Pool() as p:
        split_age_bins = split_dict(age_bins, os.cpu_count())
        input = [(params, age_bin, sizes_by_la, sizes_by_sic, local_authorities, sic_codes) for age_bin in split_age_bins]
        out = p.starmap(likelihood_inner_summand, input)

    l = np.zeros((len(local_authorities) + len(sic_codes), len(sizes)))
    totals = np.zeros(len(local_authorities) + len(sic_codes))

    for sub_l, sub_totals in out:
        l += sub_l
        totals += sub_totals

    age_coefficients = np.zeros((len(local_authorities) + len(sic_codes), len(sizes)))

    for la, size_bins in sizes_by_la.items():
        index = local_authorities.index(la)
        for size, n in size_bins.items():
            size_index = sizes.index(size)
            age_coefficients[index][size_index] = n

    for sic, size_bins in sizes_by_sic.items():
        index = len(local_authorities) + sic_codes.index(sic)
        for size, n in size_bins.items():
            size_index = sizes.index(size)
            age_coefficients[index][size_index] = n



    l = np.transpose(np.divide(np.transpose(l), totals))
    l = np.log(l)

    sum = 0

    for i in range(len(l)):
        sum += np.dot(l[i], age_coefficients[i])

    print(sum)

    return sum

def likelihood_inner_summand(params, age_bins, sizes_by_la, sizes_by_sic, local_authorities, sic_codes):
    """ Part of the likelihood function, split for multiprocessing
        parameters:
            same as likelihood
        output:
            sub_l - sub likelihood summand
            sub_totals - sub totals for each grouping
    """
    sizes = ['0-4', '5-9', '10-19', '20-49', '50-99', '100-249', '250+']
    upper_bounds = [5, 10, 20, 50, 100, 250, np.inf]
    l = np.zeros((len(local_authorities) + len(sic_codes), len(sizes)))
    totals = np.zeros(len(local_authorities) + len(sic_codes))



    for la, age_sic_bin in age_bins.items():
        la_index = local_authorities.index(la)
        for sic, ages in age_sic_bin.items():
            sic_index = len(local_authorities) + sic_codes.index(sic)
            mean = params[la_index] + params[sic_index]
            var = params[len(local_authorities) + len(sic_codes) + la_index] ** 2 + params[len(local_authorities) + len(sic_codes) + sic_index] ** 2
            for age, n in ages.items():
                #print(la_index, n)
                if age <= 0:
                    continue # TODO: handle special case
                totals[la_index] += n
                totals[sic_index] += n
                lower = 0
                for i, size in enumerate(sizes):
                    upper = upper_bounds[i]
                    s = 0
                    if upper != np.inf:
                        s += norm.cdf((np.log(upper) - age * mean) / np.sqrt(age * var))
                    else:
                        s += 1
                    if lower != 0:
                        s -= norm.cdf((np.log(lower) - age * mean) / np.sqrt(age * var))

                    l[la_index][i] += n * s
                    l[sic_index][i] += n * s

                    lower = upper

    return l, totals


def likelihood_jacobian(params, age_bins, sizes_by_la, sizes_by_sic, local_authorities, sic_codes):
    """ Jacobian of the likelihood function
    inputs:
        same as likelihood
    outputs:
        jacobian matrix
    """
    sizes = ['0-4', '5-9', '10-19', '20-49', '50-99', '100-249', '250+']

    jacobian = np.zeros((len(params)))
    totals = np.zeros(len(params))

    with Pool() as p:
        split_age_bins = split_dict(age_bins, os.cpu_count())

        input = [(params, age_bin, sizes_by_la, sizes_by_sic, local_authorities, sic_codes) for age_bin in split_age_bins]
        out = p.starmap(inner_summand_jacobian, input)

    numerator = np.zeros((len(params), len(params), len(sizes)))
    denominator = np.zeros((len(params), len(sizes)))
    for sub_numerator, sub_denominator, sub_totals in out:
        numerator += sub_numerator
        denominator += sub_denominator
        totals += sub_totals

    age_coefficients = np.zeros((len(params), len(sizes)))

    half_param_length = int(len(params) / 2)

    for la, size_bins in sizes_by_la.items():
        index = local_authorities.index(la)
        for size, n in size_bins.items():
            size_index = sizes.index(size)
            age_coefficients[index][size_index] = n
            age_coefficients[index + half_param_length][size_index] = n


    for sic, size_bins in sizes_by_sic.items():
        index = len(local_authorities) + sic_codes.index(sic)
        for size, n in size_bins.items():
            size_index = sizes.index(size)
            age_coefficients[index][size_index] = n
            age_coefficients[index + half_param_length][size_index] = n


    for mat in numerator:
        for i in range(len(mat)):
            mat[i] = np.divide(mat[i], denominator[i])
            mat[i] = np.divide(mat[i], totals[i])

    for i, mat in enumerate(numerator):
        for v in mat:
            jacobian[i] += np.dot(v, age_coefficients[i])

    return jacobian



def inner_summand_jacobian(params, age_bins, sizes_by_la, sizes_by_sic, local_authorities, sic_codes):
    """ Function that calculates the derivative of the inner summand for parrallelisation
    inputs:
        Same as likelihood_jacobian
    outputs:
        numerator, denominator, totals
    """

    sizes = ['0-4', '5-9', '10-19', '20-49', '50-99', '100-249', '250+']
    upper_bounds = [5, 10, 20, 50, 100, 250, np.inf]

    numerator = np.zeros((len(params), len(params), len(sizes)))
    denominator = np.zeros((len(params), len(sizes)))
    totals = np.zeros(len(params))

    half_param_length = int(len(params) / 2)

    for la, age_bins_by_sic in age_bins.items():
        la_index = local_authorities.index(la)
        for sic, ages in age_bins_by_sic.items():
            sic_index = len(local_authorities) + sic_codes.index(sic)
            mean = params[la_index] + params[sic_index]
            var = params[half_param_length + la_index] ** 2 + params[half_param_length + sic_index] ** 2

            for age, n in ages.items():
                if age <= 0:
                    continue
                    # TODO: Handle this case
                totals[la_index] += n
                totals[sic_index] += n
                totals[half_param_length + la_index] += n
                totals[half_param_length + sic_index] += n

                lower = 0
                for i, size in enumerate(sizes):
                    upper = upper_bounds[i]
                    s = 0
                    t = 0
                    u = 0
                    v = 0
                    if upper != np.inf:
                        s += norm.cdf((np.log(upper) - age * mean) / np.sqrt(age * var))
                        t += norm.pdf((np.log(upper) - age * mean) / np.sqrt(age * var)) / np.sqrt(age * var)
                        u += norm.pdf((np.log(upper) - age * mean) / np.sqrt(age * var)) * - ((np.log(upper) - age * mean) / (age * var) ** 1.5) * age * params[half_param_length + la_index]
                        v += norm.pdf((np.log(upper) - age * mean) / np.sqrt(age * var)) * - ((np.log(upper) - age * mean) / (age * var) ** 1.5) * age * params[half_param_length + sic]
                    if lower != 0:
                        s -= norm.cdf((np.log(lower) - age * mean) / np.sqrt(age * var))
                        t -= norm.pdf((np.log(lower) - age * mean) / np.sqrt(age * var)) / np.sqrt(age * var)
                        u -= norm.pdf((np.log(lower) - age * mean) / np.sqrt(age * var)) * - ((np.log(lower) - age * mean) / (age * var) ** 1.5) * age * params[half_param_length + la_index]
                        v -= norm.pdf((np.log(lower) - age * mean) / np.sqrt(age * var)) * - ((np.log(lower) - age * mean) / (age * var) ** 1.5) * age * params[half_param_length + sic_index]

                    denominator[la_index][i] += n * s
                    denominator[sic_index][i] += n * s
                    denominator[half_param_length + la_index][i] += n * s
                    denominator[half_param_length + sic_index][i] += n * s

                    numerator[la_index][la_index][i] += n * t * (-age * params[la_index])
                    numerator[la_index][sic_index][i] += n * t * (-age * params[la_index])

                    numerator[sic_index][la_index][i] += n * t * (-age * params[sic_index])
                    numerator[sic_index][sic_index][i] += n * t * (-age * params[sic_index])

                    numerator[half_param_length + la_index][half_param_length + la_index][i] += n * u
                    numerator[half_param_length + la_index][half_param_length + sic_index][i] += n * u

                    numerator[half_param_length + sic_index][half_param_length + sic_index][i] += n * v
                    numerator[half_param_length + sic_index][half_param_length + la_index][i] += n * v

                    lower = upper


    return numerator, denominator, totals

def split_dict(dict, n):
    """ Function to split a dict into an array for multiprocessing
        parameters:
            dict, n
        returns:
            nd array of dicts of approx equal sizes
    """
    keys = [key for key in dict]
    s = len(keys) / n
    grouped_keys = [keys[int(i * s): int((i + 1) * s)] for i in range(n)]

    return [{key: dict[key] for key in keys} for keys in grouped_keys]





def get_size_distribution_data():
    sizes = ['0-4', '5-9', '10-19', '20-49', '50-99', '100-249', '250+']

    sizes_by_la = {}
    with open('../Data/ONS/2017_enterprise_size_by_la.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            if np.sum([float(line[s]) for s in sizes]) < 50:

                print('not including la ' + line['la'] + ' due to small size: ' + str(np.sum([float(line[s]) for s in sizes])))
                continue
            sizes_by_la[line['la']] = {s: int(line[s]) for s in sizes}
    sizes_by_sic = {}
    with open('../Data/ONS/2017_enterprise_size_by_sic.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            if np.sum([float(line[s]) for s in sizes]) < 50:
                print('not including SIC ' + line['SIC'] + ' due to small size: ' +  str(np.sum([float(line[s]) for s in sizes])))
                continue

            sizes_by_sic[int(line['SIC'])] = {s: int(line[s]) for s in sizes}

    return sizes_by_la, sizes_by_sic


if __name__ == '__main__':
    main()
