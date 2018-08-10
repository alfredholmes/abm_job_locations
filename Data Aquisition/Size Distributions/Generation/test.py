import random, csv

def main():
    population = [random.randint(0, 10000) for _ in range(1000)]
    l = 1
    data = []
    for p in population:
        to_remove = 0
        for j in range(p):
            size = random.lognormvariate(0, 1)
            #print(size)
            if size > 3:#check relationship between total number of jobs in LA and difference between ONS and Companies House
                to_remove += 1
            if j > p - to_remove:
                break
        data.append([p, j])
    with open('results.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for l in data:
            writer.writerow(l)

if __name__ == '__main__':
    main()
