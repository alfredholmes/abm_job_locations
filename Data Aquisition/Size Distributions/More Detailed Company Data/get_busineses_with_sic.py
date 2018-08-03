import csv


FILES = ['2017/company_data_' + str(i) + '.csv' for i in range(10)]

def main():
    companies = load_data()
    local_authorities = {}
    for company in companies:
        if (company[-1] != '99999 - Dormant Company' and company[-1] != 'None Supplied') or company[-2] != 'NO ACCOUNTS FILED':
            if company[1] not in local_authorities:
                local_authorities[company[1]]  = 1
            else:
                local_authorities[company[1]] += 1

    write_data('non_dormant_companies.csv', local_authorities)

def load_data():
    data = []
    for file in FILES:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                data.append(line)
    return data

def write_data(file, dict):
    with open(file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for d,n in dict.items():
            writer.writerow([d, n])


if __name__ == '__main__':
    main()
