import csv


def main():
    companies = get_companies()

    las = {}


    for company in companies:
        la = company['la']
        sic = company['sic']
        size = company['size']

        if la in las:
            if sic in las[la]:
                if size in las[la][sic]:
                    las[la][sic][size] += 1
                else:
                    las[la][sic][size]  = 1
            else:
                las[la][sic] = {size: 1}
        else:
            las[la] = {sic: {size: 1}}

    
    for la, sics in las.items():
        for sic, sizes in sics.items():
            total = 0
            for n in sizes.values():
                total += n
            print(total)


def get_companies():
    companies = []
    with open('output.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            companies.append({'la': line[0], 'sic': int(line[1]), 'size': int(line[2])})

    return companies


if __name__ == '__main__':
    main()
