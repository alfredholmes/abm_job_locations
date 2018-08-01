import csv, scipy.optimize as op, scipy.stats as sps, math

SIZES = ['0-4','5-9','10-19','20-49', '50-99','100-249','250+']


def main():
    data = get_data()
    for id,d in data.items():
        r = op.minimize(ll, [0, 1], tuple(d))
        print(r)

def get_data():
    data = {}
    with open('la_company_size_dist_by_id.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            data[line['la']] = [int(line[s]) for s in SIZES]
    return data


def ll(param, arr):
    r = 0
    endpoints = [0.0001,4,19,49,99,249,2000]
    for i,x in enumerate(arr):
        r += x * (sps.norm.cdf(math.log((endpoints[i + 1]) - param[0]) / param[1]) - sps.norm.nd.cdf(math.log((endpoints[i]) - param[0]) / param[1]))

    return 1 / (r**2)


if __name__ == '__main__':
    main()
