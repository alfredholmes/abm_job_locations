import csv, random, math


EMPLOYMENT_BANDS = ['0-4', '5-9', '10-19', '50-99', '100-249', '250+']

def main():

    #load companies info
    print('loading companies')
    companies = get_companies()
    print('done')


    #load local authority company statistics
    scaling = {} #Companies house doesn't match
    las = {}



    print('loading LAs')
    with open('la_company_size_dist_by_id.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            total = 0
            for band in EMPLOYMENT_BANDS:
                total += int(line[band])
            scaling[line['la']] = total
            las[line['la']] = [line[band] for band in EMPLOYMENT_BANDS]
    print('Done')

    total_employment  = 0
    for key, total in scaling.items():
        total_employment += total

    print(total_employment)

    recon_las = {}
    fractions = []

    for company, data in companies.items():
        if data[0] in recon_las:
            recon_las[data[0]] += 1
        else:
            recon_las[data[0]] = 1

    for la, total in scaling.items():
        fractions.append([la, (recon_las[la] / total)])

    with open('scaling_factors.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for line in fractions:
            writer.writerow(line)


def get_companies():
    #2012 snapshot 0: CompanyNumber 1: LocalAuthority 2:Age in months
    companies = {}
    with open('2012-Snapshot.csv') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            companies[line[0]] = (line[1], line[2])
    print('loaded ' + str(len(companies)) + ' companies')
    return companies

if __name__ == '__main__':
    main()
