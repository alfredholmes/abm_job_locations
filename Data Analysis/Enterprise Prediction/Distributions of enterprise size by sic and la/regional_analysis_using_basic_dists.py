import analysis, regional_analysis
import csv
import size_assignation

from scipy.stats import lognorm
import numpy as np
import matplotlib.pyplot as plt


def main():
    colours = {'0-4': 'red', '5-9': 'blue', '10-19': 'orange', '20-49': 'green', '50-99': 'yellow', '100-249': 'purple', '250+': 'pink'}

    size_distributions_by_sic = size_assignation.get_size_distributions_by_sic()
    size_distributions_by_la  = size_assignation.get_size_distributions_by_la()

    companies = analysis.get_companies(1)
    for company in companies:
        la = company['la']
        sic = company['sic']
        #company['size'] = lognorm.rvs(size_distributions_by_la[la]['sd'], scale=np.exp(size_distributions_by_la[la]['mean']))
        company['size'] = lognorm.rvs(size_distributions_by_sic[sic]['sd'], scale=np.exp(size_distributions_by_sic[sic]['mean']))


    results = regional_analysis.regional_analysis(companies)
    for data in results.values():
        data['a'] = np.array(data['a']) / np.max(data['a'])
    for size, points in results.items():
        for i in range(len(points['x'])):
            plt.scatter(points['x'][i], points['y'][i], color=colours[size])
    plt.savefig('results_when_picking_sizes_from_sic_size_no_alpha.png')
    plt.show()

if __name__ == '__main__':
    main()
