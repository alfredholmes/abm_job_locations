import random, csv

PROB = 0.3 #probability that registered company operates in a different local authority
N_CITIES = 200
def main():
    registered_companies = []

    with open('entity_differences.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            registered_companies.append(int(line[2]))

    active_companies = []
    for i in range(len(registered_companies)):
        active_companies.append(registered_companies[i] * (1 - PROB))
        for j in range(N_CITIES):
            if i != j:
                active_companies[i] += 0.3 / (N_CITIES - 1) * registered_companies[j]

    write_output('results.csv', registered_companies, active_companies)


def write_output(file, array_1, array_2):
    with open(file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(len(array_1)):
            writer.writerow([array_1[i], array_2[i]])


if __name__ == '__main__':
    main()
