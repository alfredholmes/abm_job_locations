import csv

FILES = ['2017/' + str(i) + '.csv' for i in range(10)]

def main():
    addresses = set()
    local_authority_data = {}
    local_authority_data_with_repeated_addresses = {}
    for file in FILES:
        print(file)
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                address = line[-1] + line[-2]
                if address not in addresses:
                    addresses.add(address)
                    if line[1] in local_authority_data:
                        local_authority_data[line[1]] += 1
                    else:
                        local_authority_data[line[1]]  = 1
                if line[1] in local_authority_data_with_repeated_addresses:
                    local_authority_data_with_repeated_addresses[line[1]] += 1
                else:
                    local_authority_data_with_repeated_addresses[line[1]]  = 1

    with open('no_repeated_addresses_2017_la_totals.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for id, n in local_authority_data.items():
            writer.writerow([id, n, local_authority_data_with_repeated_addresses[id]])

if __name__ == '__main__':
    main()
