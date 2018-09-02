import csv
import analysis
import numpy as np
import matplotlib.pyplot as plt

def main():
    colours = {'0-4': 'red', '5-9': 'blue', '10-19': 'orange', '20-49': 'green', '50-99': 'yellow', '100-249': 'purple', '250+': 'pink'}

    company_data = [analysis.get_companies(i) for i in range(1, 3)]
    for i, companies in enumerate(company_data):
        results = regional_analysis(companies)
        plt.figure(i)
        for size, data in results.items():
            data['a'] = np.array(data['a']) / np.max(data['a'])
            for j in range(len(data['x'])):
                plt.scatter(data['x'][j], data['y'][j], label=size, alpha=data['a'][j], color=colours[size])
        plt.plot([0, 1], [0, 1], label='y=x')
        plt.xlabel('Actual proportion')
        plt.ylabel('Assigned proportion')

        plt.savefig(str(i) + '_result_sic_regional_distributions.png')

    plt.show()

def regional_analysis(companies):
    regions = get_regions()

    size_dists = get_regional_size_distributions()

    size_bands = ['0-4', '5-9', '10-19', '20-49', '50-99', '100-249', '250+']
    upper_limits = [5, 10, 20, 50, 100, 250, np.inf]

    sizes = {}

    for company in companies:
        region = regions[company['la']]
        sic = int(company['sic'])
        size = int(company['size'])
        for j, s in enumerate(upper_limits):
            if size < s:
                size_band = size_bands[j]
                break
        else:
            size_band = size_bands[-1]

        if sic in sizes:
            if region in sizes[sic]:
                if size_band in sizes[sic][region]:
                    sizes[sic][region][size_band] += 1
                else:
                    sizes[sic][region][size_band]  = 1
            else:
                sizes[sic][region] = {size_band: 1}
        else:
            sizes[sic] = {region: {size_band: 1}}

    #print(sizes)

    results  = {s: {'x': [], 'y': [], 'a':[]} for s in size_bands}


    for sic, regions_sizes in sizes.items():
        if sic not in size_dists:
            print(str(sic) + 'sic missing')
            continue
        for region, size_dist in regions_sizes.items():
            if region not in size_dists[sic]:
                #print(region + ' region missing')
                continue
            total = 0
            for n in size_dist.values():
                total += n
            for size, n in size_dist.items():
                if size_dists[sic][region]['Total'] == 0:
                    results[size]['x'].append(0)
                else:
                    results[size]['x'].append(size_dists[sic][region][size] / size_dists[sic][region]['Total'])

                results[size]['y'].append(n / total)
                results[size]['a'].append(size_dists[sic][region]['Total'])

    return results


def get_regions():
    regions = {}
    with open('../Data/ONS/lad_17_geo_info.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            if line['region'] != '':
                regions[line['id']] = line['region']
            else:
                regions[line['id']] = line['country']
    return regions

def get_regional_size_distributions():
    sizes = ['0-4', '5-9', '10-19', '20-49', '50-99', '100-249', '250+', 'Total']
    with open('../Data/ONS/2017_enterprise_size_dists_by_sic_by_region.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        regions = next(reader)
        size_by_region_by_sic = {}
        next(reader)
        for line in reader:
            try:
                sic = int(line[0][:2])
            except:
                continue
            size_by_region_by_sic[sic] = {}
            for i, region in enumerate(regions):
                offset = 1 + len(sizes)
                size_by_region_by_sic[sic][region] = {s: int(line[offset + i]) for i, s in enumerate(sizes)}
    return size_by_region_by_sic


if __name__ == '__main__':
    main()
