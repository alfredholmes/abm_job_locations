import matplotlib.pyplot as plt
import random
import numpy as np



def main():
    companies = np.ones(10000)
    population = len(companies) * 30
    s = companies.sum()
    for _ in range(population):
        print(_)
        position = random.random()
        sum = 0
        for i, n in enumerate(companies):
            sum += n / s
            if position < sum:
                break
        companies[i] += 1
        s += 1

    plt.hist(np.log(companies - 1), 50, density=True, range = (-10, 10))
    plt.show()

if __name__ == '__main__':
    main()
