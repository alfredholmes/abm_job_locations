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
    las = get_ch_data()
    with open('2017_la_totals_bad_sic_removed.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for la, n in las.items():
            writer.writerow([la, n])



def get_ch_data():
    data = {}
    for file in FILES:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                try:
                    sic = int(line[5][:2])
                    band = get_band(sic)
                    if band is None or band == (1, 4):
                        continue
                    if line[1] in data:
                        data[line[1]] += 1
                    else:
                        data[line[1]]  = 1
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
