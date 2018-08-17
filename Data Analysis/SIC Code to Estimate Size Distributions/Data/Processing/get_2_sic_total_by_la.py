import csv

FILES = ['../CH/2017/' + str(i) + '.csv' for i in range(10)]


def main():
    las = get_la_data()

    with open('2_SIC_total_by_la.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, ['la'] + [i for i in range(1, 100)])
        writer.writeheader()
        for la, data in las.items():
            las[la]['la'] = la
            writer.writerow(las[la])


def get_la_data():
    data = {}
    addresses = set()
    for file in FILES:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                try:
                    sic = int(line[5][:2])
                    la = line[1]
                    address = la + line[6]
                    if address in addresses:
                        continue

                    addresses.add(address)

                    #print(sic)
                    if sic == 99: #Non supplied
                        continue
                    if la in data:
                        if sic in data[la]:
                            data[la][sic] += 1
                        else:
                            data[la][sic]  = 1
                    else:
                        data[la] = {sic: 1}
                except:
                    print("--- Failed to process company ---")
                    print(line)

    return data

if __name__ == '__main__':
    main()
