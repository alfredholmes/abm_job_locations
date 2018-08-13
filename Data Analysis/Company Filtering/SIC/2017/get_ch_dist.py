import csv


FILES = ['../../CHData/2017/company_data_' + str(i) + '.csv' for i in range(10)]


def main():
    ons = get_ons_data()
    ch = get_ch_data()

    totals = []
    for i in range(10000):
        ch_total = 0
        ons_total = 0

        if i in ch:
            ch_total = ch[i]

        if i in ons:
            ons_total = ons[i]

        totals.append([i, ch_total, ons_total])

    with open('2017_sic_ch_ons.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for t in totals:
            if t[1] != 0 or t[2] != 0:
                writer.writerow(t)

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
