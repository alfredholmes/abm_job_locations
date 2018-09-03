import parameter_recovery
import matplotlib.pyplot as plt
import numpy as np


def main():
    parameters, sizes, new_sizes, results, random_results, mean_distances, random_mean_distances, variance_distances, random_variance_distances = parameter_recovery.parameter_recovery(50000, 50, 50)

    new_params = calculate_new_params(new_sizes)

    x = []
    y = []

    for i, data in new_params.items():
        for j, d in data.items():
            x.append(d[0])
            y.append(d[1])

    a = []
    b = []

    for i, data in parameters.items():
        for j, d in data.items():
            a.append(d[0])
            b.append(d[1])

    plt.figure(0)
    plt.hist2d(x, y, 40)
    plt.figure(1)
    plt.hist2d(a, b, 40)
    plt.show()

def calculate_new_params(data):
    params = {}
    for i, d in data.items():
        params[i] = {}
        for j, arr in d.items():
            mean = np.mean(np.log(arr))
            var = np.var(np.log(arr))
            params[i][j] = [mean, var]

    return params

if __name__ == '__main__':
    main()
