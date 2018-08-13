import csv, random

def main():
    #companies = get_companies()
    migration_data = get_migrations()

    migrations = []

    for m in migration_data:
        if m['OldLocalAuthority'] != m['NewLocalAuthority']:
            migrations.append([m['OldLocalAuthority'], m['NewLocalAuthority']])


    migrations = sum_migrations(migrations)
    write_migrations(migrations)


def write_migrations(migrations):
    with open('la_companies_house_migration.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for la_from, m in migrations.items():
            for la_to,v in m.items():
                writer.writerow([la_from, la_to, v])


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
    data = []
    with open('company_migration_data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            data.append(line)

    return data

#returns list of companies
def get_companies():
    data = []
    with open('2017-Snapshot.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            data.append(line[0])
    return data

if __name__ == '__main__':
    main()
