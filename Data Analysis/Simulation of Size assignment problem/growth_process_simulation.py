import random, numpy as np
from scipy.stats import multivariate_normal, norm, lognorm
import matplotlib.pyplot as plt


def main():
    a = 50
    b = 50
    max_age = 10 * 12
    max_companies = 400000 * 2 / (a * b)
    ages = {i: {j: [random.randint(0, max_age - 1) for _ in range(random.randint(0, max_companies - 1))] for j in range(b)} for i in range(a)}

    means = {i: {j: x for j, x in enumerate(multivariate_normal.rvs([0.0001] * b, cov=0.0001))} for i in range(a)}
    variances  = {i: {j: x ** 2 for j, x in enumerate(multivariate_normal.rvs([0.001] * b, cov=0.001))} for i in range(a)}

    #simulate growth process

    sizes = []
    for i, data in ages.items():
        for j, age_data in data.items():
            for age in age_data:
                sizes.append(norm.rvs(1 + means[i][j], np.sqrt(variances[i][j]), size=age).prod())

    mean = np.mean(np.log(sizes))
    variance = np.var(np.log(sizes), ddof=1)

    x = np.linspace(0, 20)

    plt.hist(sizes, 60,range=[0, 20], density=True)
    plt.plot(x, lognorm.pdf(x, np.sqrt(variance), scale=np.exp(mean)))
    plt.savefig('growth_simulation_global_dist.png')
    plt.show()



if __name__ == '__main__':
    main()
