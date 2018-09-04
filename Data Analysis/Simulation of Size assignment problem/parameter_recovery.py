import simulation
import numpy as np
from scipy.stats import lognorm, multivariate_normal
import random
import matplotlib.pyplot as plt


def main():
    _, _,_, results, random_results, mean_distances, random_mean_distances, variance_distances, random_variance_distances = parameter_recovery(200000, 50, 50)


    plt.figure(0)
    plt.hist(results, 50, density=True, label='recovery')
    plt.hist(random_results, 50, density=True, alpha=0.5, label='random')
    plt.legend()
    plt.xlabel('Euclidian distance in parameter space')
    plt.savefig('recovery distance histogram 200000 normal with random.png')

    plt.figure(1)
    plt.hist(mean_distances, 50, density=True, label='recovery')
    plt.hist(random_mean_distances, 50, density=True, alpha=0.5, label='random')
    plt.legend()
    plt.plot([0, 0], [0, 1.4])
    plt.xlabel('difference between recovery mean and actual')
    plt.savefig('mean distance histogram normal with random.png')

    plt.figure(2)
    plt.hist(variance_distances, 50, density=True, label='recovery')
    plt.hist(random_variance_distances, 50, density=True, alpha=0.5, label='random')
    plt.legend()
    plt.plot([0, 0], [0, 30])
    plt.xlabel('difference between recovery variance and actual')
    plt.savefig('variance distance histogram normal with random.png')

    plt.show()

def parameter_recovery(n, a, b):
    parameters = simulation.generate_parameters(a, b)
    sizes, _ = simulation.generate_sizes(parameters, a, b, n)

    #assume log norm dist and find params of those distributions
    lognorm_dist_params_by_a, lognorm_dist_params_by_b = get_log_normal_params(sizes, a, b)

    #generate two arrays of possible sizes for each category
    generated_sizes_by_a = {}
    for i in range(a):
        n = 0
        for j in range(b):
            if j not in sizes[i]:
                print(str((i, j)) + ' missing')
                continue
            n += len(sizes[i][j])
        generated_sizes_by_a[i] = lognorm.rvs(np.sqrt(lognorm_dist_params_by_a[i]['var']), scale=np.exp(lognorm_dist_params_by_a[i]['mean']), size=n)
        generated_sizes_by_a[i] = [x for x in generated_sizes_by_a[i]]
    generated_sizes_by_b = {}
    for j in range(b):
        n = 0
        for i in range(a):
            if j not in sizes[i]:
                print(str((i, j)) + ' missing')
                continue
            n += len(sizes[i][j])
        generated_sizes_by_b[j] = lognorm.rvs(np.sqrt(lognorm_dist_params_by_b[i]['var']), scale=np.exp(lognorm_dist_params_by_b[i]['mean']), size=n)
        generated_sizes_by_b[j] = [x for x in generated_sizes_by_b[j]]

    entities = []
    for i in range(a):
        for j in range(b):
            if j not in sizes[i]:
                continue
            for _ in range(len(sizes[i][j])):
                entities.append((i, j))

    random.shuffle(entities)
    x = 0
    new_sizes = {}
    for entity in entities:
        if x % 1000 == 0:
            print(x)
        x += 1
        i, j = find_closest(generated_sizes_by_a[entity[0]], generated_sizes_by_b[entity[1]])
        size = (generated_sizes_by_a[entity[0]][i] + generated_sizes_by_b[entity[1]][j]) / 2
        del generated_sizes_by_a[entity[0]][i]
        del generated_sizes_by_b[entity[1]][j]
        if entity[0] in new_sizes:
            if entity[1] in new_sizes[entity[0]]:
                new_sizes[entity[0]][entity[1]].append(size)
            else:
                new_sizes[entity[0]][entity[1]] = [size]
        else:
            new_sizes[entity[0]] = {entity[1]: [size]}




    results = []
    random_results = []

    mean_distances = []
    random_mean_distances = []

    variance_distances = []
    random_variance_distances = []

    for i in range(a):
        for j in range(b):
            if j not in new_sizes[i]:
                continue
            mean, var = get_log_normal_params_from_array(new_sizes[i][j])
            results.append((parameters[i][j][0] - mean) ** 2 + (parameters[i][j][1] ** 2 - var) ** 2)
            p = multivariate_normal.rvs([0.001, 0.1], cov=[[0.1, 0], [0, 0.0001]])
            random_results.append((parameters[i][j][0] - p[0]) ** 2 + (parameters[i][j][1] ** 2 - p[1]) ** 2)
            mean_distances.append(parameters[i][j][0] - mean)
            random_mean_distances.append(parameters[i][j][0] - p[0])

            variance_distances.append(parameters[i][j][1] - var)
            random_variance_distances.append(parameters[i][j][1] - p[1])

    return parameters, sizes, new_sizes, results, random_results, mean_distances, random_mean_distances, variance_distances, random_variance_distances


def get_log_normal_params(sizes, a, b):
    lognorm_dist_params_by_a = {}
    for i in range(a):
        if i not in sizes:
            continue
        size_array = []
        for j in range(b):
            if j not in sizes[i]:
                print(str((i, j)) + ' missing')
                continue
            size_array += sizes[i][j]
        mean = np.mean(np.log(size_array))
        var = np.var(np.log(size_array), ddof=1)
        lognorm_dist_params_by_a[i] = {'mean': mean, 'var': var}

    lognorm_dist_params_by_b = {}
    for j in range(b):
        size_array = []
        for i in range(a):
            if j not in sizes[i]:
                print(str((i, j)) + ' missing')
                continue
            size_array += sizes[i][j]
        mean = np.mean(np.log(size_array))
        var = np.var(np.log(size_array), ddof=1)
        lognorm_dist_params_by_b[j] = {'mean': mean, 'var': var}

    return lognorm_dist_params_by_a, lognorm_dist_params_by_b

def get_log_normal_params_from_array(arr):
    mean = np.mean(np.log(arr))
    var = np.var(np.log(arr), ddof=1)
    return mean, var

def find_closest(arr_1, arr_2):
    i, j = 0, 0
    min = np.inf
    min_pair = None
    while i < len(arr_1) and j < len(arr_2):
        distance = (arr_1[i] - arr_2[j]) ** 2
        if distance < min:
            min = distance
            min_pair = (i, j)
        if arr_1[i] < arr_2[j]:
            i += 1
        else:
            j += 1
    return min_pair


if __name__ == '__main__':
    main()
