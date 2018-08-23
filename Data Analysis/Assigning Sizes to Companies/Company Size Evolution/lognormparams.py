import gibrat_process
import csv
import numpy as np

def main():
    mean = 0
    sd = 0
    with open('parameters.csv') as csvfile:
        reader = csv.reader(csvfile)
        line = next(reader)
        mean = float(line[0])
        sd = float(line[1])

    mean, variance = gibrat_process.get_mean_variance(mean, sd)
    #this mean and variance is that of log(1 + \epsilon), so if a company is x years old, log S ~ N(x*mean, x*sd) where S is the size of the company
    with open('../lognorm_per_month_params.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([mean, np.sqrt(variance)])

if __name__ == '__main__':
    main()
