import csv


MAX = 1.8
MIN = 0.4

FILES = ['2013/' + str(i) + '.csv' for i in range(6)]

def main():
    ons = read_ons('ons_2013_sic_total.csv')
    ch  = read_ch('sic_ch_2013_total.csv')

    codes_to_ignore = []
    for sic, n in ch.items():
        if (sic not in ons or MIN * n > ons[sic] or MAX * n < ons[sic]):
            codes_to_ignore.append(str(sic))

    las = {}

    for file in FILES:
        d = []
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                if line[5][:2] not in codes_to_ignore:
                    if line[1] not in las:
                        las[line[1]] = 1
                    else:
                        las[line[1]] += 1

    with open('2013_total_per_la_sic_filtered.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for id, n in las.items():
            writer.writerow([id, n])




def read_ons(file):
    data = {}
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            if len(line[0]) == 2:
                data[int(line[0])] = int(line[1])
    return data


def read_ch(file):
    data = {}
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            try:
                data[int(line[0])] = int(line[1])
            except:
                pass
    return data

if __name__ == '__main__':
    main()
