import csv

def main():
    ons = read('ons_2013_sic_total.csv')
    ch  = read('sic_ch_2013_total.csv')

    with open('2013_sic_comparison.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['sic', 'ch', 'ons'])
        for sic, total in ch.items():
            if sic not in ons:
                print(sic)
            else:
                writer.writerow([sic, total, ons[sic]])


def read(file):
    data = {}
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            try:
                data[int(line[0][:4])] = line[1]
            except:
                pass
    return data

if __name__ == '__main__':
    main()
