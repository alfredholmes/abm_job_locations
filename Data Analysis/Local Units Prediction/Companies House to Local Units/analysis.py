import csv, datetime
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np


def main():
    #years = [str(i) for i in range(2012, 2018)]
    years = ['2012', '2013', '2014', '2015', '2016', '2017']
    results = {}
    data = get_ch_data()
    for year in years:
        date = datetime.datetime.strptime(year, '%Y')
        ons_totals = get_ons_data(year)
        sic_totals = get_total_sic_at_date(date, data)
        #print(ons_totals)


        for sic, n in sic_totals.items():
            if sic not in ons_totals or sic == 99:
                print('Missing sic ' + str(sic) + ' number of companies: ' + str(n))
                continue

            if sic not in results:
                results[sic] = {year: ons_totals[sic] / n}
            else:
                results[sic][year] = ons_totals[sic] / n


    gradients = []
    average_multipliers = {}
    plt.figure(0)
    for sic, data in results.items():
        x = []
        y = []

        for year, value in data.items():
            x.append(int(year))
            y.append(value)

        average_multipliers[sic] = np.array(y).mean()

        plt.plot(x, y, label=sic, marker='o')
        grad, _, _, _, _ = linregress(x, y)
        gradients.append(grad)

    with open('sic_ch_multipliers.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for sic, x in average_multipliers.items():
            writer.writerow([sic, x])



    #plt.legend()

    plt.savefig('sic_ch_lu_ratio_timeseries.png')
    plt.figure(1)
    plt.hist(gradients, 30, density=True)
    plt.savefig('grad_histogram.png')
    plt.show()


#return the total number of companies house registered companies at datetime argument
def get_total_sic_at_date(date, data):
    sic_totals = {}
    companies = {}


    for line in data:
        death = datetime.datetime.strptime(line[3], '%Y-%m-%d')
        birth = datetime.datetime.strptime(line[2], '%Y-%m-%d')
        if (death - date).days > 0 and (birth - date).days < 0:
            try:
                sic = int(line[1][:2])
            except:
                pass
            if sic in sic_totals:
                sic_totals[sic] += 1
            else:
                sic_totals[sic]  = 1
    return sic_totals

def get_ch_data():
    data = []
    files = ['Data/CH/Company_Data/' + str(i) + '.csv' for i in range(0, 5)]
    for file in files:
        with open(file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                data.append(line)

    return data

def get_ons_data(year):
    ons_data = {}
    with open('Data/ONS/' + str(year) + '_2_SIC_Local_Unit_Size_Bands.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            ons_data[int(line['SIC'])] = int(line['Total'])

    return ons_data



if __name__ == '__main__':
    main()
