import csv, random

SIZES = ['0-4','5-9','10-19','20-49', '50-99','100-249','250+']

SCALE_FACTOR = 1.4

def main():
    sic_dist_params = get_sic_dist_params()
    la_2_sic_totals = get_la_2_sic_total()

    #Estimate the size distributions

    output = {}

    for la, sic_totals in la_2_sic_totals.items():
        size_dist = {s: 0 for s in SIZES}
        for id, n in sic_totals.items():
            mean = sic_dist_params[id]['mean']
            standard_deviation = sic_dist_params[id]['sd']
            for _ in range(n):
                size_dist[get_size_band(random.lognormvariate(mean, standard_deviation))] += 1
        output[la] = size_dist

    with open('generated_size_dist.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, ['la'] + SIZES)
        writer.writeheader()
        for la, size_dist in output.items():
            size_dist['la'] = la
            for s in size_dist:
                try:
                    size_dist[s] *= SCALE_FACTOR
                    size_dist[s] = int(size_dist[s])
                except:
                    pass
            writer.writerow(size_dist)

def get_la_2_sic_total():
    data = {}
    with open('2_SIC_total_by_la.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            sic_totals = {}
            for i in range(1, 100):
                total = ''
                if str(i) in line:
                    total = line[str(i)]
                if total == '':
                    sic_totals[i] = 0
                else:
                    sic_totals[i] = int(total)

            data[line['la']] = sic_totals
    return data


def get_size_band(size):
    min_values = [5, 10, 20, 50, 100, 250]
    for i, x in enumerate(min_values):
        if size < x:
            return SIZES[i]
    return SIZES[-1]

def get_sic_dist_params():
    data = {}
    with open('sic_lognormal_params.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            data[int(line[0])] = {'mean': float(line[1]), 'sd': float(line[2])}
        for i in range(100):
            if i not in data:
                data[i] = {'mean': 1, 'sd': 0}

    return data

if __name__ == '__main__':
    main()
