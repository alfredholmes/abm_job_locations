import analysis
import matplotlib.pyplot as plt
import numpy as np


def main():
    companies = analysis.get_companies(1)


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

    size_of_bins = []
    for la, sics in las.items():
        for sic, sizes in sics.items():
            total = 0
            for size, n in sizes.items():
                total += n
            size_of_bins.append(total)

    plt.hist(size_of_bins, 40, density=True)
    plt.xlabel('Size of sic-la bin')
    plt.savefig('size_of_bins.png')
    plt.show()

if __name__ == '__main__':
    main()
