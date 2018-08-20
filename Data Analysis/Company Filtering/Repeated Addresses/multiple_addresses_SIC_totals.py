import csv

FILES = ['2017/' + str(i) + '.csv' for i in range(10)]

def main():
    addresses = set()
    sic_totals = {int(i): 0 for i in range(10000)}
    ons = get_ONS_totals()

    for file in FILES:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                address = line[-1] + line[-2]
                if address in addresses:

                    continue
                sic = 9999
                try:
                    sic = int(line[5][:4])
                except:
                    pass
                sic_totals[sic] += 1
    data = []
    for sic, total in sic_totals.items():
        if sic in ons:
            if total != 0 and ons[sic] != 0:
                data.append([sic, total, ons[sic]])
        else:
            if total != 0:
                data.append([sic, total, 0])


    with open('4_sic_totals_no_repeated_addresses.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['sic', 'CH', 'ONS'])
        for line in data:
            writer.writerow(line)


def get_ONS_totals():
    with open('2017_4_SIC_ONS_totals.csv', 'r') as csvfile:
        data = {}
        reader = csv.reader(csvfile)

        for line in reader:
            sic = int(line[0][:4])
            data[sic] = int(line[1])

        return data
if __name__ == '__main__':
    main()
