import csv


FILES = ['../../CHData/2017/company_data_' + str(i) + '.csv' for i in range(10)]


def main():
    ons = get_ons_data()
    ch = get_ch_data()

    ratios = {}
    for sic, n in ch.items():
        ons_total = 0
        if sic in ons:
            ons_total = ons[sic]
            ratios[sic] =  ons_total / n


    las = {}

    for file in FILES:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                try:
                    if int(line[5][:4]) in ratios:
                        if line[1] in las:
                            las[line[1]] += ratios[int(line[5][:4])]
                        else:
                            las[line[1]]  = ratios[int(line[5][:4])]
                except:
                    pass
    with open('2017_la_totals_filtered.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for id, n in las.items():
            writer.writerow([id, n])

def get_ons_data():
    data = {}
    with open('2017_sic_totals.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            data[int(line[0])] = int(line[1])
    return data

def get_ch_data():
    data = {}
    for file in FILES:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                try:
                    sic = int(line[5][:4])
                    if sic in data:
                        data[sic] += 1
                    else:
                        data[sic] = 1
                except:
                    print(line[5])

    return data

if __name__ == '__main__':
    main()
