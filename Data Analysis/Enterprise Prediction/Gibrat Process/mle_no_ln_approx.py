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

    sic_codes = [sic for sic in sizes_by_sic]
    local_authorities = [la for la in sizes_by_la]

    print('Sorting companies...')

    age_bins = growth_model_2_rvs.sort_companies(companies, sizes_by_la, sizes_by_sic)

    print('done')
    scale = 0.0001
    initial = np.ones((2 * len(sic_codes) + 2 * len(local_authorities))) * scale
    initial = np.divide(initial, [1] * (len(sic_codes) + len(local_authorities)) + [0.1] * (len(sic_codes) + len(local_authorities)))
    print(likelihood(initial, age_bins, sizes_by_la, sizes_by_sic, local_authorities, sic_codes))


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
    #print(l)
    l = np.log(l)

    sum = 0

    for i in range(len(l)):
        sum += np.dot(l[i], age_coefficients[i])


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
        print(la)
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

                    l[la_index][i] += s
                    l[sic_index][i] += s

                    lower = upper

    return l, totals

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
