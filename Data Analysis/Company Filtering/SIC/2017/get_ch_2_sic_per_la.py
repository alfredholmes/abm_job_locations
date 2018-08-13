import csv


FILES = ['../../CHData/2017/company_data_' + str(i) + '.csv' for i in range(10)]

BANDS = [(1, 4),
         (5, 40),
         (41, 44),
         (45, 46),
         (46, 47),
         (47, 48),
         (49, 54),
         (55, 57),
         (58, 64),
         (64, 67),
         (68, 69),
         (69, 76),
         (77, 83),
         (84, 85),
         (85, 86),
         (86, 88),
         (90, 99)
        ]


def main():
    companies = get_ch_data()
    las = {}
    for company in companies:
        if company[0] in las:
            if str(company[1]) in las[company[0]]:
                las[company[0]][str(company[1])] += 1
            else:
                las[company[0]][str(company[1])]  = 1
        else:
            las[company[0]] = {str(company[1]): 1}

    with open('2_sic_by_la.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, ['la'] + [str(band) for band in BANDS])
        writer.writeheader()
        for la, sic in las.items():

            sic['la'] = la
            writer.writerow(sic)



def get_ch_data():
    data = []
    for file in FILES:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                try:
                    sic = int(line[5][:2])
                    band = get_band(sic)
                    if band is None:
                        continue
                    data.append([line[1], band])
                except:
                    pass

    return data

def get_band(x):
    b = BANDS[:]
    while len(b) > 1:
        target = int((len(b) + 1) / 2)
        if x < b[target][1]:
            if x >= b[target][0]:
                return b[target]
            b = b[:target]
        else:
            b = b[target:]
    if x >= b[0][0] and x < b[0][1]:
        return b[0]
    else:
        return None

if __name__ == '__main__':
    main()
