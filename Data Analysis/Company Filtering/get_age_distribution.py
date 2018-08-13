import csv

FILES = ['2013/' + str(i) + '.csv' for i in range(6)]
AGE_BANDS = [2, 4, 10]


def main():
    companies = load_data()
    las = {}
    #first populate las dict
    for c in companies:
        if c[1] not in las:
            las[c[1]] = [0] * (len(AGE_BANDS) + 1)

    for c in companies:
        for i, age in enumerate(AGE_BANDS):
            if int(c[2]) / 12 < age:
                las[c[1]][i] += 1
                break
        else:
            las[c[1]][-1] += 1


    write_data(las)


def write_data(data):
    with open('2013_age_data_ch.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['la'] + AGE_BANDS + ['10+'])
        for la, d in data.items():
            writer.writerow([la] + d)

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
