import csv
import matplotlib.pyplot as plt
import numpy as np


def main():
    company_data = [get_companies(i) for i in range(1, 3)]
    las_dists = []
    for companies in company_data:
        las = {}


        for company in companies:
            la = company['la']
            sic = company['sic']
            size = company['size']

            if la in las:
                if sic in las[la]:
                    if size in las[la][sic]:
                        las[la][sic][size] += 1
                    else:
                        las[la][sic][size]  = 1
                else:
                    las[la][sic] = {size: 1}
            else:
                las[la] = {sic: {size: 1}}


        for la, sics in las.items():
            for sic, sizes in sics.items():
                total = 0
                for n in sizes.values():
                    total += n
                print(total)

        las_dists.append(las)

    angles = []
    random_angles = []
    i = 0
    missing = 0
    for la, sics in las_dists[0].items():
        for sic, sizes in sics.items():
            i += 1
            if sic not in las_dists[1][la]:
                missing += 1
                continue

            #find max size
            max_size = 0
            for size in sizes:
                if size > max_size:
                    max_size = size

            for size in las_dists[1][la][sic]:
                if size > max_size:
                    max_size = size
            a = np.zeros(max_size + 1)
            b = np.zeros(max_size + 1)

            for size, n in sizes.items():
                a[size] = n
            for size, n in las_dists[1][la][sic].items():
                b[size] = n


            angle = np.arccos(np.dot(a, b) / np.sqrt(np.dot(a, a) * np.dot(b, b)))
            angles.append(angle)

    print(missing / i)
    plt.hist(angles, 50, density=True)
    plt.savefig('angle_distribution.png')
    plt.show()

def get_companies(file):
    companies = []
    with open('output_' + str(file) + '.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            companies.append({'la': line[0], 'sic': int(line[1]), 'size': int(line[2])})

    return companies


if __name__ == '__main__':
    main()
