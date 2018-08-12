import csv

def main():
    ons = read_ons('ons_2013_sic_total.csv')
    ch  = read_ch('sic_ch_2013_total.csv')

    data = {}
    for c,n in ch.items():
        if int(str(c)[:2]) in data:
            data[int(str(c)[:2])][0] += n
        elif int(str(c)[:2]) in ons:
            data[int(str(c)[:2])] = [n, ons[int(str(c)[:2])]]
        else:
            print(int(str(c)[:2]))
    with open('2013_sic_comparison.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for sic, d in data.items():
            writer.writerow([sic] + d)




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
