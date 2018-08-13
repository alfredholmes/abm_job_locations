import csv


FILES = ['2013/' + str(i) + '.csv' for i in range(6)]


def main():
    data = {}
    for file in FILES:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                if line[5][:5] not in data:
                    data[line[5][:5]]  = 1
                else:
                    data[line[5][:5]] += 1

    with open('sic_ch_2013_total.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for d,n in data.items():
            writer.writerow([d, n])




if __name__ == '__main__':
    main()
