import csv, random

YEARS = [i for i in range(2012, 2018)]

def main():
    migrations = get_migrations()

    for year, data in migrations.items():
        new = []
        for line in data:
            if line['OldLocalAuthority'] != line['NewLocalAuthority']:
                new.append([line['OldLocalAuthority'], line['NewLocalAuthority']])

        migrations[year] = sum_migrations(new)

    for year, data in migrations.items():
        with open('output/' + str(year) + '_migrations.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            for from_la, m in data.items():
                for to_la, n in m.items():
                    writer.writerow([from_la, to_la, n])

def sum_migrations(data):
    r = {}
    for d in data:
        if d[0] in r:
            if d[1] in r[d[0]]:
                r[d[0]][d[1]] += 1
            else:
                r[d[0]][d[1]] = 1
        else:
            r[d[0]] = {d[1]: 1}
    return r



def get_migrations():
    data = {year : [] for year in YEARS}
    with open('company_migration_data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            year = int(line['Date'][:4])
            if year in data:
                data[year].append(line)
    return data

if __name__ == '__main__':
    main()
