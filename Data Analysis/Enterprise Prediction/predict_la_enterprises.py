import csv
import analysis
import matplotlib.pyplot as plt

def main():
    companies = analysis.get_ch_data()
    multipliers = get_sic_multipliers()
    location = get_2012_company_locations()

    average_mult = 0
    for sic, mult in multipliers.items():
        average_mult += mult

    average_mult /= len(multipliers)

    las = {}
    addresses = set()
    date = 2013

    for company in companies:
        try:
            sic = int(company[1][:2])
        except:
            continue
        if company[0] not in location:
            continue
        la = location[company[0]]
        if sic not in multipliers:
            print(str(sic) + ' sic missing')
            to_add = average_mult
        else:
            to_add = multipliers[sic]
            #print(company[0] + ' company missing')
        if la in las:
            las[la] += to_add
        else:
            las[la]  = to_add

    la_totals = get_la_lu_totals()

    x = []
    y = []
    for la, n in las.items():
        if la not in la_totals:
            print(la + ' missing')
            continue
        x.append(la_totals[la])
        y.append(n)

    plt.scatter(x, y)
    plt.plot(x, x)
    plt.savefig('la_local_unit_predictions_with_ch.png')
    plt.show()

def get_la_lu_totals():
    data = {}
    with open('Data/ONS/2012_enterprise_size_by_la.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for line in reader:

            data[line[0]] = int(line[-1])

    return data

def get_sic_multipliers():
    data = {}
    with open('sic_ch_multipliers.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            data[int(line[0])] = float(line[1])

    return data

def get_2012_company_locations():
    companies = {}
    with open('Data/CH/2012-Snapshot.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            #print(line[0], line[1])
            companies[line[0]] = line[1]
    return companies

if __name__ == '__main__':
    main()
