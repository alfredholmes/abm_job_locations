import csv

FILES = ['2017/company_data_' + str(i) + '.csv' for i in range(10)]
AGE_BANDS = []


def main():
    companies = load_data()



    for company in companies:




def load_data():
    data = []
    for file in FILES:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                data.append(line)
    return data


if __name__ == '__main__':
    main()
