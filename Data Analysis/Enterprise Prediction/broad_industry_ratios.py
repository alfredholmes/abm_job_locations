import csv
import analysis, predict_la_enterprises

import matplotlib.pyplot as plt

MULTIPLIERS = True

def main():
    broad_industry_la, industry_groups = get_broad_industry_la_data()
    upper_bounds = get_upper_bounds(industry_groups)

    #print(upper_bounds)

    companies = analysis.get_ch_data()
    multipliers = predict_la_enterprises.get_sic_multipliers()
    location = predict_la_enterprises.get_2012_company_locations()

    las = {}

    for company in companies:
        #print(company)
        if company[0] not in location:
            continue
        try:
            sic = int(company[1][:2])
        except:
            continue

        if sic == '99':
            continue

        for i, upper in enumerate(upper_bounds):
            if sic < upper:
                sic_band = industry_groups[i]
                break
        la = location[company[0]]
        m = 1
        if MULTIPLIERS:
            if sic not in multipliers:
                continue
            m = multipliers[sic]
        if la in las:
            if sic_band in las[la]:
                las[la][sic_band] += m
            else:
                las[la][sic_band]  = m
        else:
            las[la] = {sic_band: m}

    #print(las)

    results = {band: {'x': [], 'y': []} for band in industry_groups}

    for la, size_data in broad_industry_la.items():
        if la not in las:
            continue
        for band, n in size_data.items():
            x = int(n)
            y = 0
            if band in las[la]:
                y = las[la][band]

            results[band]['x'].append(x)
            results[band]['y'].append(y)



    for sic, data in results.items():
        plt.scatter(data['x'], data['y'], label=sic)

    plt.plot([0, 6000], [0, 6000], label='y=x')
    plt.legend()
    plt.xlabel('Number of companies (ONS)')
    plt.ylabel('Number of companies (CH corrected)')
    plt.savefig('broad_industry_ratios.png')
    plt.show()



def get_upper_bounds(groups):
    upper_bounds = []
    for group in groups:
        if '-' in group:
            upper = 1 + int(group.split('-')[-1])
        else:
            upper = 1 + int(group)
        upper_bounds.append(upper)
    return upper_bounds

def get_broad_industry_la_data():
    data = {}
    with open('/Data/CH/2012_enterprise_industry_group_by_la_id.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        for line in reader:

            data[line[0]] = {h: line[i + 1] for i, h in enumerate(header[1:-1])}
    return data, header[1:-1]

if __name__ == '__main__':
    main()
