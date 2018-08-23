#problems with optimisation mean that some of the parameters in parameters_by_sic.csv are wrong (0 variance etc - fix by picking companies with similar size dists and picking their params)

import csv
import gibrat_process

def main():
    params = load_parameters()
    good = get_good_parameters(params)

    distributions = gibrat_process.get_targets()

    for p in params:
        if p not in good:
            #find the closest distribution match
            dist = distributions[p]
            best_sic = None
            best_distance = 0
            for g in good:
                good_dist = distributions[g]
                distance = ((good_dist - dist) ** 2).mean()
                if best_sic is None or distance < best_distance:
                    best_distance = distance
                    best_sic = g
            params[p] = params[best_sic]

    with open('better_parameters.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['SIC', 'mean', 'sd'])
        for sic, p in params.items():
            writer.writerow([sic, p['mean'], p['sd']])

def load_parameters():
    data = {}
    with open('parameters_by_sic.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            print(line)
            data[int(line[0])] = {'mean': float(line[1]), 'sd': float(line[2])}
    return data

def get_good_parameters(params):
    good = {}
    for sic, p in params.items():
        if (p['mean'] > -0.2 and p['sd'] != 0) and not (p['mean'] == 0 and p['sd'] == 0.01):
            good[sic] = p
    return good



if __name__ == '__main__':
    main()
