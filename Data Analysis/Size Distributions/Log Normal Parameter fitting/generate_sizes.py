import csv, random

SIZES = ['0-4','5-9','10-19','20-49', '50-99','100-249','250+']
MAX_SIZES = [5, 10, 20, 50, 100, 250]

def main():
    la_totals = get_la_totals()
    la_params = get_la_params()

    la_size_bands = {}

    for la, n in la_totals.items():
        la_size_bands[la] = {s: 0 for s in SIZES}

        for _ in range(n):
            mean = la_params[la]['mean']
            sd   = la_params[la]['sd']
            la_size_bands[la][get_size_band(random.lognormvariate(mean, sd))] += 1

    with open('simulated_size_distribution.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, ['la'] + SIZES)
        for la, size_data in la_size_bands.items():
            size_data['la'] = la
            writer.writerow(size_data)

def get_la_totals():
    data = {}
    with open('la_company_size_dist_by_id.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            total = 0
            for size in SIZES:
                total += int(line[size])

            data[line['la']] = total
    return data

def get_la_params():
    data = {}
    with open('la_lognormal_params.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            data[line[0]] = {'mean': float(line[1]), 'sd': float(line[2])}
    return data

def get_size_band(size):
    for i, m in enumerate(MAX_SIZES):
        if size < m:
            return SIZES[i]
    return SIZES[-1]


if __name__ == '__main__':
    main()
