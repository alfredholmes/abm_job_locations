from scipy.stats import lognorm, multivariate_normal
import numpy as np
import random
import matplotlib.pyplot as plt


def main():
    parameters = generate_parameters(50, 50)
    sizes, size_array = generate_sizes(parameters, 50, 50, 100000)

    mean = np.mean(np.log(size_array))
    var = np.var(np.log(size_array), ddof=1)
    plt.figure(0)
    plt.hist(size_array, 50, density=True)
    plt.plot(np.linspace(0, 4), lognorm.pdf(np.linspace(0, 4), np.sqrt(var), scale=np.exp(mean)), label='lognorm, mean: ' + str(mean) + ', var: ' + str(var))
    plt.xlabel('Size')
    plt.savefig('simulated global distribution uniform parameters.png')
    plt.figure(1)
    size_cross_section = sizes[0]
    size_array_cross_section = []
    for b, data in size_cross_section.items():
        for s in data:
            size_array_cross_section.append(s)

    mean = np.mean(np.log(size_array_cross_section))
    var  = np.var(np.log(size_array_cross_section), ddof=1)

    plt.hist(size_array_cross_section, 50, density=True)
    plt.plot(np.linspace(0, 4), lognorm.pdf(np.linspace(0, 4), np.sqrt(var), scale=np.exp(mean)), label='lognorm, mean: ' + str(mean) + ', var: ' + str(var))
    plt.xlabel('Size')
    plt.savefig('simulated crossectional distribution uniform parameters.png')
    plt.show()

def generate_parameters(a, b):
    parameters = {}
    for i in range(a):
        parameters[i] = {}
        for j in range(b):
            parameters[i][j] = multivariate_normal.rvs([0.001, 0.1], cov=[[0.1, 0], [0, 0.0001]])
            #parameters[i][j] = [(random.random() - 0.5) * 0.01, random.random() * 0.5]
    return parameters

def generate_sizes(parameters, a, b, n):
    sizes = {}
    size_array = []

    for _ in range(n):
        id_1 = random.randint(0, a - 1)
        id_2 = random.randint(0, b - 1)
        #print(parameters[a][b][1])
        size = lognorm.rvs(parameters[id_1 ][id_2][1], scale=np.exp(parameters[id_1][id_2][0]))
        size_array.append(size)

        if id_1 in sizes:
            if id_2 in sizes[id_1]:
                sizes[id_1][id_2].append(size)
            else:
                sizes[id_1][id_2] = [size]
        else:
            sizes[id_1] = {id_2: [size]}

    return sizes, size_array

if __name__ == '__main__':
    main()
