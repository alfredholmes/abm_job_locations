import csv, math, random, os
from multiprocessing import Process, Array, Manager
#scaling_factors is a csv containing the ratio: (registered companies / companies) for each local authority
# TODO: Multithreading
# TODO: Power law relationship

EMPLOYMENT_BANDS = ['0-4', '5-9', '10-19', '50-99', '100-249', '250+']
POPULATION = 200
SCALE_REDUCTION = 200
#THREADS = os.cpu_count()

def main():

    companies = get_companies()
    random.shuffle(companies)
    companies = companies[:int(len(companies) / SCALE_REDUCTION)]
    size_distribution = get_size_distribution()
    print('Data Loaded')
    print('Generating models:')
    models = load_state(companies, True)
    print('Done')

    for i in range(10):
        print('Running evolution ' + str(i))
        fitness = []
        calculate_fitness(models, companies, size_distribution, fitness)
        evolve(models, companies, size_distribution, fitness)
        #evolve(models, companies, size_distribution)
        print('Done')

    print(calculate_fitness(models, companies, size_distribution, fitness).get_distribution(size_distribution))
    save_state(models)

def generate_models(n, companies, arr):
    for _ in range(n):
        arr.append(Model(random.random() * 0.1, random.random() * 0.1, companies))


def calculate_fitness(models, companies, actual_distribution, fitness):
    i = 0
    top = None
    top_model = None
    for model in models:
        print('Calculating fitness of model ' + str(i))
        fitness.append(model.fitness(actual_distribution))
        print(fitness[i])
        if top is None or fitness[i] < top:
            top = fitness[i]
            top_model = model
        i += 1

    return top_model

def evolve(models, companies, actual_distribution, fitness):
    median = sorted(fitness)[int(len(fitness) / 2)]
    to_delete = []
    fit = []
    for i in range(len(fitness)):
        if fitness[i] >= median:
            to_delete.append(i)
        else:
            fit.append(i)

    for i in range(len(to_delete)):
        models[i] = Model.combine(models[fit[int(random.random() * len(fit))]], models[fit[int(random.random() * len(fit))]], companies)


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


def save_state(models):
    with open('models.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for model in models:
            writer.writerow([model.a, model.b])
def load_state(companies, load_from_file, file=None):
    models = []
    if not load_from_file:
        for i in range(POPULATION):
            m = Model(random.random() * 0.05, random.random() * 0.05, companies)
            models.append(m)
        return models
    if file == None:
        file = 'models.csv'
    with open('models.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            m = Model(float(line[0]), float(line[1]), companies)
            models.append(m)
    return models
class Model:
    def __init__(self, age_multiplier, standard_devition, companies):
        self.a = age_multiplier
        self.b = standard_devition
        #self.z = lambda : random.gauss(0, 1)
        self.companies = {data[0]: data[1:] + [self.estimate_size(float(data[2]))] for data in companies}


    def estimate_size(self, age, local_authority = None):
        #input = (self.a + self.b * random.gauss(0, 1)) * age
        input = self.a * age
        try:
            return math.exp(input)
        except:
            return 300.0

    def get_distribution(self, actual_distribution):
        distribution = {}
        for key in actual_distribution:
            distribution[key] = {band: 0 for band in EMPLOYMENT_BANDS}
        fails = 0
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
        for key, data in distribution.items():
            distribution[key]  = {b: d * SCALE_REDUCTION for b, d in data.items()}
        return distribution

    def fitness(self, actual_distribution):
        #generate distribution
        distribution = self.get_distribution(actual_distribution)
        error = 0
        for la, employment_data in actual_distribution.items():
            total_actual = 0
            total_sim = 0
            for band in EMPLOYMENT_BANDS:
                total_actual += employment_data[band]
                total_sim    += distribution[la][band]
            for band in EMPLOYMENT_BANDS:
                error += (employment_data[band] / total_actual - distribution[la][band] / total_actual) ** 2

        return error / len(actual_distribution)

    def combine(a, b, companies):
        return Model((a.a * ((random.random() * 0.8) + 1) + b.a * ((random.random() * 0.8) + 1)) / 2, (a.b * ((random.random() * 0.8) + 1) + b.b * ((random.random() * 0.8) + 1)) / 2, companies)

if __name__ == '__main__':
    main()
