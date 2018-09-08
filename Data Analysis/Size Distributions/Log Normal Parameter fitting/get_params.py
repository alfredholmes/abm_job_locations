import parameters
from scipy.stats import lognorm
import numpy as np
import matplotlib.pyplot as plt

def main():
    sizes = [5, 10, 20, 50, 100, 250, np.inf]
    #to_fit = [124155,11480,2735,955,275,120,60]
    to_fit = [2087030,299710,151140,80575,25915,14615,9825]


    params = parameters.get_mean_sd(to_fit)
    print(params)
    last = 0
    x = []
    y = []
    for i,s in enumerate(sizes):
        print(lognorm.cdf(s, params[1], scale=np.exp(params[0])) - lognorm.cdf(last, params[1], scale=np.exp(params[0])), to_fit[i] / np.sum(to_fit))
        x.append(lognorm.cdf(s, params[1], scale=np.exp(params[0])) - lognorm.cdf(last, params[1], scale=np.exp(params[0])))
        y.append(to_fit[i] / np.sum(to_fit))
        last = s

    print(lognorm.mean(params[1], scale=np.exp(params[0])), lognorm.var(params[1], scale=np.exp(params[0])))

    plt.scatter(x, y)
    plt.plot([0, 1], [0, 1])
    plt.show()




if __name__ == '__main__':
    main()
