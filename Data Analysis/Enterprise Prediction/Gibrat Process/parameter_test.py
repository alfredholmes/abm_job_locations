from scipy.stats import lognorm
import numpy as np
import csv

def main():
    #mu, sigma = (-0.09393732098510958, 2.005628423533079)
    with open('../Data/2017_2_sic_enterprise_lognormal_params.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            mu = float(line[1])
            sigma = float(line[2])
            print(line[0], lognorm.mean(sigma, scale=np.exp(mu)), lognorm.var(sigma, scale=np.exp(mu)))

if __name__ == '__main__':
    main()
