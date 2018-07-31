import csv, math, random, os
from multiprocessing import Process, Pool
#scaling_factors is a csv containing the ratio: (registered companies / companies) for each local authority

EMPLOYMENT_BANDS = ['0-4', '5-9', '10-19', '50-99', '100-249', '250+']
POPULATION = 128
SCALE_REDUCTION = 32

def main():



    companies = get_companies()
    random.shuffle(companies)
    companies = companies[:int(len(companies) / SCALE_REDUCTION)]
    print(companies[1])
    size_distribution = get_size_distribution()
    scaling = get_scaling()
    print('Data Loaded')
    print('Generating models:')
    models = [Model(random.random() * 0.05, random.random() * 0.05, companies) for _ in range(POPULATION)]
    print('Done')
    #print(Model(0.005, 4, companies).fitness(size_distribution, scaling))

def par_fit(x, compaies, size_distribution, scaling):
    return Model(x[0], x[1], companies).fitness

def get_scaling():
    data = {}
    with open('scaling_factors.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            data[line[0]] = float(line[1])
    return data

def get_companies():
    data = []
    #Companies file : no heading just id, la, age(/months)
    with open('2012-Snapshot.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            data.append(line)

    return data

def get_size_distribution():
    data = {}
    with open('la_company_size_dist_by_id.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            data[line['la']] = {band: int(line[band]) for band in EMPLOYMENT_BANDS}
    return data

class Model:
    def __init__(self, age_multiplier, standard_devition, companies):
        self.a = age_multiplier
        self.b = standard_devition
        self.z = lambda : random.gauss(0, 1)
        self.companies = {data[0]: data[1:] + [self.estimate_size(data[2])] for data in companies}


    def estimate_size(self, age, local_authority = None):
        input = self.a * (self.b * self.z() + float(age))
        return math.exp(input)
        #return 1
    def fitness(self, actual_distribution, scaling):
        #generate distribution
        distribution = {}
        for key in actual_distribution:
            distribution[key] = {band: 0 for band in EMPLOYMENT_BANDS}
        fails = 0
        print(len(self.companies.items()))
        for company, data in self.companies.items():
            if len(data[0]) == 0 or data[0][0] == 'N' or data[0][0] == 'L' or data[0][0] == 'M':
                fails += 1
                continue
            for band in EMPLOYMENT_BANDS:
                band_size = 0
                for position, char in enumerate(band):
                    if char == '-':
                        band_size = int(band[position+1:])
                        break
                if data[2] <= band_size:
                    distribution[data[0]][band] += 1
                    break
            else:
                distribution[data[0]][EMPLOYMENT_BANDS[-1]] += 1

        print('Fails: ' + str(fails))

        error = 0
        for la, employment_data in actual_distribution.items():
            scale = scaling[la]
            for band in EMPLOYMENT_BANDS:
                error += (employment_data[band] * scale / SCALE_REDUCTION - distribution[la][band]) ** 2
        return error / len(actual_distribution)

if __name__ == '__main__':
    main()
